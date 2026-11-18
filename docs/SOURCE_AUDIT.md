# Source-level audit: import, plugin, and resource loading constraints

This document records what the source code actually does at import/package/runtime level. It corresponds to plan §9 ("Areas requiring a follow-up source-level audit") and gates every structural move (proto reorganization, `native/consensus/` relocation, `src/` migration). It is read-only analysis — no files moved.

## 1. `gptc.proto` bindings are active and must stay importable at the current path

`gptc/proto/gptc_pb2.py` and `gptc_pb2_grpc.py` are **dispatch shims**, not orphaned legacy files:

```python
# gptc/proto/gptc_pb2.py
from gptc._docarray import docarray_v2 as is_docarray_v2
if __pb__version__.startswith("4"):
    if is_docarray_v2:
        from gptc.proto.docarray_v2.pb.gptc_pb2 import *
    else:
        from gptc.proto.docarray_v1.pb.gptc_pb2 import *
else:
    if is_docarray_v2:
        from gptc.proto.docarray_v2.pb2.gptc_pb2 import *
    else:
        from gptc.proto.docarray_v1.pb2.gptc_pb2 import *
```

They select between `docarray_v1`/`docarray_v2` and `pb`/`pb2` based on the installed protobuf version and whether docarray_v2 is available. They are imported by **~25 modules** across `gptc/clients`, `gptc/serve/runtimes`, `gptc/serve/networking`, `gptc/types`, `gptc/jaml`.

**Constraint:** `gptc.proto.gptc_pb2` and `gptc.proto.gptc_pb2_grpc` must remain importable at exactly this path. Any proto reorganization must keep these shims (or thin re-export shims) in place. Do not delete `gptc/proto/gptc_pb2.py` / `gptc_pb2_grpc.py`.

## 2. `gptc/resources/` location is coupled to the `gptc` package path

`gptc/constants.py:59-61`:

```python
__resources_path__ = os.path.join(
    os.path.dirname(sys.modules["gptc"].__file__), "resources"
)
```

Resources are resolved relative to the **installed `gptc` package directory**, not a fixed repo path.

**Constraint:** `gptc/resources/` must be physically adjacent to the `gptc` package in the installed layout. A `src/` migration (`src/gptc`) is safe only if `gptc/resources/` moves with it AND `MANIFEST.in`/`include_package_data` keep shipping `resources`. Verify `MANIFEST.in:2` (`recursive-include gptc/resources *`) covers it (it does).

## 3. Plugin discovery is minimal; no `entry_points`-based plugin loader

The only registered entry point is the console script:

```python
# setup.py:215-218
entry_points={
    'console_scripts': ['gptc=gptc_cli:main'],
},
```

No `pkg_resources.iter_entry_points` / `importlib.metadata.entry_points` plugin discovery exists in `gptc/`. "Plugin" references are:
- `gptc/jaml/__init__.py` YAML `py_modules` (user-specified modules loaded by path, not entry points)
- `gptc/orchestrate/deployments/config/k8slib/*.py` Kubernetes `device_plugins` (config-only)

**Constraint:** `src/` migration won't break a plugin entry-point mechanism (none exists beyond the console script). But the console script target `gptc_cli:main` must remain importable — `gptc_cli` must stay on the install path alongside `gptc`.

## 4. Native extension `jraft` is lazily imported, only for stateful executors

`gptc/serve/executors/run.py:29` does `import jraft` inside `run_raft()`, called only by stateful executor flows (`run_stateful`). Non-stateful flows never import `jraft`.

**Constraint:** `jraft` must be importable as a top-level module (`import jraft`) from the installed environment. CI smoke test is `python -c "import gptc; import jraft"`. Any move of the Go implementation must keep `setup.py`'s `build_golang.root='jraft'` and `ext_modules` source path pointing at `gptc/serve/consensus/run.go`, and must preserve the installed module name `jraft`.

## 5. Package discovery and data inclusion

- `setup.py` uses `packages=find_packages()` + `include_package_data=True`.
- `MANIFEST.in` includes `gptc/resources`, `docarray/resources`, `gptc/serve/consensus`, `extra-requirements.txt`, `fastentrypoints.py`, `LICENSE`; prunes `tests/`.
- Wheel data inclusion depends on `include_package_data=True` reading `MANIFEST.in` (setuptools behavior) — confirm with a clean wheel build (`make verify-dist`) that `gptc/resources`, `gptc/proto`, and `gptc/serve/consensus` are present in the wheel.

## 6. Version source

`setup.py` reads `__version__` from `gptc/__init__.py:79` (`"3.34.1"`). `pyproject.toml` marks `version` as `dynamic`. `conda/meta.yaml` hardcodes `3.34.1` and is checked against `__init__.py` by `scripts/check-metadata.py`.

**Constraint:** Keep `gptc/__init__.py`, `conda/meta.yaml`, and CI in sync. `make check_metadata` enforces this.

## Move-safety summary

| Proposed move | Safe? | Condition |
|---|---|---|
| `gptc/serve/consensus/` → `native/consensus/` (Go only) | Conditional | Keep `setup.py` `build_golang.root`/`ext_modules` path in sync; keep Python wrappers at `gptc/serve/consensus/__init__.py` until import tests pass; installed `import jraft` must keep working |
| `gptc/proto/` → elsewhere | Unsafe without shims | `gptc.proto.gptc_pb2` imported by ~25 modules; keep shims or aliases |
| `src/gptc` + `src/gptc_cli` layout | Conditional | `constants.py` `__resources_path__` depends on `gptc` package dirname; `gptc/resources` must move with `gptc`; wheel must still include resources + proto bindings |
| Rename test dirs (`tests/unit/test/`, kebab fixtures) | Conditional | Confirm pytest discovery/import assumptions first; kebab names fine for non-imported fixtures |
| `gptc_cli/` → merge into `gptc/` | Unsafe without packaging change | Console script entry point `gptc_cli:main`; CLI is deliberately separate (plan §3.2) |
