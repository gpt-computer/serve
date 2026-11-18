# Testing tiers and markers

This document describes how Gptc tests are organized, how to select the right tier locally and in CI, and which infrastructure each suite requires. It corresponds to PR #5 of the repository structure improvement plan. It is descriptive only — no test files are moved or renamed here.

## Test tiers

| Tier | Directory | Speed | Infrastructure | pytest selection |
|---|---|---|---|---|
| **unit** | `tests/unit` | fast | none (hermetic) | `uv run pytest tests/unit` |
| **integration** | `tests/integration` | medium | none by default; some need Docker images built first | `uv run pytest tests/integration` |
| **system** | `tests/docker_compose`, `tests/k8s`, `tests/k8s_otel`, `tests/gptchub` | slow | Docker Compose / Kubernetes cluster / Hub | `uv run pytest tests/docker_compose` (etc.) |

`tests/` also contains top-level modules and a `tests/unit/test/` subdirectory; these are discovered under `tests/unit` per `pytest.ini testpaths`.

### How tests are assigned to tiers

`tests/conftest.py` (`pytest_collection_modifyitems`) auto-applies infrastructure markers based on the top-level suite directory:

- `tests/k8s/` and `tests/k8s_otel/` → `k8s` marker (require a Kubernetes cluster)
- `tests/docker_compose/` → `docker_compose` marker (require Docker Compose)

Tests in `tests/unit/` and `tests/integration/` carry no infrastructure marker by default; individual tests may add `@pytest.mark.slow`, `@pytest.mark.timeout(...)`, `@pytest.mark.asyncio`, or `@pytest.mark.repeat`.

## Markers (defined in `pytest.ini`)

| Marker | Meaning | Deselect with |
|---|---|---|
| `slow` | slow-running test | `-m "not slow"` |
| `k8s` | requires a Kubernetes cluster | `-m "not k8s"` |
| `docker_compose` | requires Docker Compose | `-m "not docker_compose"` |
| `timeout(n)` | per-test timeout duration | n/a |
| `asyncio` | async test (strict asyncio mode) | n/a |
| `repeat` | test runs n times | n/a |
| `ignore` | legacy no-op, kept for compatibility | n/a |

`pytest.ini` also sets `testpaths = tests/unit tests/integration` and `asyncio_mode=strict`, so `uv run pytest` with no path runs only unit + integration by default.

## Running tests locally

```bash
# install dev/test dependencies
uv sync

# fast tier: unit tests only, no external infrastructure
uv run pytest tests/unit

# fast tier, skipping slow tests
uv run pytest tests/unit -m "not slow"

# integration tier (may build/pull Docker images)
uv run pytest tests/integration

# full fast tier (unit + integration)
uv run pytest

# system tiers (require the named infrastructure)
uv run pytest tests/docker_compose   # Docker Compose
uv run pytest tests/k8s              # Kubernetes cluster
uv run pytest tests/k8s_otel         # Kubernetes + OpenTelemetry
uv run pytest tests/gptchub          # Executor Hub
```

Makefile equivalents:

```bash
make unit_tests        # tests/unit (overridable: test_path=...)
make integration_tests # tests/integration
make tests             # unit + integration
make test_quick        # skip slow tests (-m "not slow")
make test_k8s          # tests/k8s
make test_docker_compose # tests/docker_compose
```

## CI jobs

CI (`.github/workflows/ci.yml`) runs the fast tier (`unit_tests` + `integration_tests`) from the built wheel, ignoring `tests/integration/docarray_v2`, `tests/integration/stateful`, and `tests/integration/hub_usage/dummyhub`:

```bash
pytest --cov=gptc --cov-report=xml --timeout=600 -v -s \
  --ignore-glob='tests/integration/docarray_v2/*' \
  --ignore-glob='tests/integration/stateful/*' \
  --ignore-glob='tests/integration/hub_usage/dummyhub*' \
  ${{ matrix.test-path }}
```

Separate CI jobs build wheels (Linux/macOS, Python 3.8–3.11) with the Go toolchain and smoke-test `import gptc; import jraft`. The `k8s`, `docker_compose`, and `k8s_otel` system suites are not part of the default fast CI path; they run in dedicated jobs that provision the required infrastructure.

## Test output and cleanup

- Test workspaces use `tmpdir`/`tmp_path` (conftest `test_metas`, `tmpfile` fixtures) — no state is written into source directories.
- Coverage output (`coverage.xml`, `.coverage`) is written at the repo root and ignored by `.gitignore`.
- `.pytest_cache/` and `.mypy_cache/` are ignored by `.gitignore`.
- Run `make clean_python_cache` to remove `__pycache__/` and `.pyc` files locally.

## Rules

1. Keep fast tests hermetic: no Docker, Kubernetes, GPU, or network service dependencies. Mark anything slower with `@pytest.mark.slow`.
2. Mark Docker Compose suites with `docker_compose` and Kubernetes suites with `k8s` (conftest does this automatically by directory).
3. Do not add new top-level test modules under `tests/`; place them in the appropriate tier directory.
4. Use underscore names for importable Python test packages; kebab-case directory names are acceptable only for external fixtures (e.g. `test-executor-torch`, `replica-exec`, `needs-merge`) that are not imported as Python modules.
5. CI smoke-test for the native extension is `python -c "import gptc; import jraft"` — stateful-executor tests require `jraft` to be importable.
