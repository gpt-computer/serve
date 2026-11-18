# Native component (`jraft`) build documentation

This document records how the Go/native consensus extension `jraft` is built, loaded, and packaged. It corresponds to PR #3 of the repository structure improvement plan. It is intentionally descriptive only — no files are moved or deleted here.

## Source layout

All Go/native sources live under `gptc/serve/consensus/`:

| Path | Role |
|---|---|
| `run.go` | cgo entry point; exports `run`, `add_voter`, `get_configuration` to Python |
| `jraft.go` | Python C extension module definition (`PyModuleDef jraft`, `PyInit_jraft`) |
| `jraft.h` | cgo-generated header (do not edit) |
| `gptc_raft/` | Go raft FSM / RPC implementation |
| `gptc-go-proto/` | generated Go protobuf bindings (`gptc.pb.go`, `gptc_grpc.pb.go`) |
| `docarray-go-proto/` | generated Go protobuf bindings (`docarray.pb.go`) |
| `gptc.proto`, `docarray.proto` | canonical `.proto` sources for the Go bindings |
| `go.mod` (`module jraft`, `go 1.19`), `go.sum` | Go module definition and lock |
| `scripts/protogen.sh` | regenerates Go protobuf bindings from `.proto` |
| `scripts/fetch-protos.sh` | fetches `docarray.proto` from the docarray repo |
| `add_voter/` | separate admin proto + Python gRPC client (`add_voter_pb2.py`, etc.) |

The Go module path is `jraft`; generated Go bindings use package `jraft/gptc-go-proto` and `jraft/docarray-go-proto`.

## Build mechanism

`setup.py` builds the extension through the `setuptools-golang` `build_golang` hook:

```python
extra_golang_kw = {
    'build_golang': {'root': 'jraft', 'strip': False},
    'ext_modules': [
        Extension(
            'jraft',
            ['gptc/serve/consensus/run.go'],
            py_limited_api=True,
            define_macros=[('Py_LIMITED_API', None)],
        )
    ],
    'setup_requires': ['setuptools-golang'],
}
```

Conditions (setup.py:185): the hook only activates when `go` is on `PATH`, the OS is not Windows, and it is not (macOS + Python 3.7). When inactive, no `jraft` extension is built and `import jraft` will fail at runtime.

- `py_limited_api=True` + `Py_LIMITED_API` → the wheel is tagged `abi3` and produces `jraft.abi3.so`.
- `build_golang.root = 'jraft'` tells setuptools-golang the Go module root is the `jraft` module (i.e. `go.mod`).
- The single compiled source listed is `run.go`; cgo pulls in `jraft.go` and the rest of the package transitively.

## CI build and release path

CI workflows (`.github/workflows/ci.yml`, `cd.yml`, `force-release.yml`) build the extension with:

1. `actions/setup-go@v2` with `go-version: 1.19.5`
2. `pip install git+https://github.com/gpt-computer/setuptools-golang.git@feat-align-with-alaeddine-code`
3. `pip install cibuildwheel`
4. On Linux: `setuptools-golang-build-manylinux-wheels --pythons <tag>`
5. On macOS: `python -m cibuildwheel --output-dir dist` with `CIBW_TEST_COMMAND: python -c "import gptc; import jraft"`

The built `jraft.abi3.so` is bundled inside the `gptc` wheel (not shipped as a standalone file). Wheels are uploaded as CI artifacts (`dist/*.whl`).

## Python loading path

`gptc/serve/executors/run.py` loads the extension lazily inside `run_raft()` (run.py:29):

```python
import jraft

...
persisted_address = jraft.get_configuration(raft_id, raft_dir)
...
jraft.run(address, raft_id, raft_dir, args.name, executor_target, **raft_configuration)
```

The import is deliberate: modules that do not use stateful executors never need `jraft`. Because the import is unqualified (`import jraft`), the `jraft` extension module must be importable from the installed environment — i.e. `jraft.abi3.so` must be installed on `sys.path` alongside `gptc`. This is why CI's smoke test is `python -c "import gptc; import jraft"`.

## The root-level `jraft.abi3.so`

`jraft.abi3.so` (≈19 MB) at the repository root is a local build artifact, not a source file. It is produced when `python setup.py bdist_wheel` (or `make build`) runs with the Go toolchain present. It is ignored by `.gitignore` (`*.so`) and must never be committed.

Do not delete or relocate it until the loader and release process are inspected (done here). If a developer has a stale root `jraft.abi3.so`, `make clean_build` does not remove it; remove it manually or rebuild from a clean checkout.

## Go proto generation (separate from Python proto)

The Go bindings are generated from `gptc.proto` / `docarray.proto` via `scripts/protogen.sh`, which invokes `protoc --go_out ... --go-grpc_out`. This is **independent** of the Python protobuf bindings under `gptc/proto/` (docarray_v1/docarray_v2). Pin `protoc` and the `protoc-gen-go` / `protoc-gen-go-grpc` plugin versions and regenerate in CI to detect drift — see PR #4 (protocol generation).

## Supported platform / ABI matrix

| OS | Python | Go | Builds `jraft`? | Wheel tag |
|---|---|---|---|---|
| Linux | 3.8–3.12 | 1.19.5 | yes | manylinux + abi3 |
| macOS | 3.8–3.12 (not 3.7) | 1.19.5 | yes | macosx + abi3 |
| Windows | any | any | **no** | `jraft` unavailable |

Stateful executors (which require `jraft`) are therefore Linux/macOS only.

## Rules

1. Do not edit `jraft.h` — it is cgo-generated.
2. Do not commit `jraft.abi3.so`, `build/`, `dist/`, or `*.egg-info` (`.gitignore` covers them).
3. Keep `go.mod` Go version (1.19) and CI `setup-go` version (1.19.5) in sync.
4. Keep the `setuptools-golang` fork reference stable across CI workflows (`ci.yml`, `cd.yml`, `force-release.yml`).
5. `import jraft` is lazy and only used by stateful executors; non-stateful flows must not depend on it.
6. Any future move of the Go implementation (e.g. to `native/consensus/`) must keep `setup.py`'s `build_golang.root` and `ext_modules` source path in sync, and must preserve the installed import name `jraft`.
