# Packaging inventory and ownership map

This document records which file owns each packaging concern for the `gptc`
project, so dependency declarations, package metadata, versioning, and
source-file inclusion rules do not drift apart. It corresponds to PR #1 of the
repository structure improvement plan.

## Source of truth

| Concern | Owner file | Notes |
|---|---|---|
| Build backend | `pyproject.toml` `[build-system]` | `setuptools.build_meta`; requires `setuptools>=18.0`, `wheel` |
| Project name / requires-python / readme | `pyproject.toml` `[project]` | `name = "gptc"`, `requires-python = ">=3.8,<3.13"` |
| Version | `gptc/__init__.py` (`__version__`) | Read by `setup.py`; `conda/meta.yaml` must match (verified by `scripts/check-metadata.py`) |
| Description / author / license / urls / classifiers / entry points | `setup.py` `setup()` call | `pyproject.toml` marks these `dynamic`, so `setup.py` is the real source |
| Runtime dependencies + extras tags | `extra-requirements.txt` | Parsed by `setup.py` `get_extra_requires()` into `install_requires` / `extras_require` |
| Console script entry point | `setup.py` `entry_points` | `gptc=gptc_cli:main` (also declared in `conda/meta.yaml`) |
| Native extension (`jraft`) | `setup.py` `build_golang` + `ext_modules` | Built from `gptc/serve/consensus/run.go` only when `go` is available and not Windows |
| Shell autocomplete registration | `setup.py` post-install commands | Runs on `develop`, `install`, `egg_info` |
| Package discovery | `setup.py` `packages=find_packages()` | |
| Package / non-Python data inclusion | `MANIFEST.in` + `setup.py include_package_data=True` | `MANIFEST.in` includes `gptc/resources`, `docarray/resources`, `gptc/serve/consensus`, `LICENSE`, etc. |
| Locked dev/CI environment | `uv.lock` | Refreshed with `uv lock`; `[tool.uv]` in `pyproject.toml` sets default groups/constraints |
| Exported pip requirements | `requirements.txt` | Single `.` — installs the local project |
| Documentation build deps | `docs/requirements.txt` | Separate audience; pinned for reproducible docs builds |
| Conda packaging | `conda/meta.yaml` | Three outputs (`gptc-core`, `gptc-perf`, `gptc`); version hardcoded, must sync with `gptc/__init__.py` |
| Docker images | `docker/*.Dockerfile` | Shared project images; test-specific Dockerfiles live next to their fixtures |

## Duplicate / generated files

- `extra-requirements.txt` (root) is the source of truth.
- `gptc/resources/extra-requirements.txt` is a byte-for-byte duplicate of the root file. It is included in sdists via `MANIFEST.in` but is not parsed by `setup.py`. Keep the two in sync; prefer removing the duplicate once nothing references it.
- `requirements.txt` contains only `.` and exists for `pip install .` compatibility.
- `uv.lock` and exported `requirements*.txt` files describe an environment, not package metadata; do not edit them by hand to declare dependencies — edit `extra-requirements.txt` (and `pyproject.toml` dependency groups) instead, then regenerate.

## Verification commands

- `make check_metadata` — runs `scripts/check-metadata.py`; asserts version/Python/entry-point/tag consistency across `gptc/__init__.py`, `pyproject.toml`, `setup.py`, `conda/meta.yaml`, `extra-requirements.txt`, and CI workflows.
- `make build` — builds sdist (`setup.py sdist`) and wheel (`setup.py bdist_wheel`) into `dist/`.
- `make install_local` — installs the freshly built wheel with `uv pip install --force-reinstall dist/*.whl`.
- `make verify-dist` — clean-environment check: builds sdist+wheel into a temp directory, installs the wheel into a fresh venv, and smoke-tests `import gptc` and `import jraft` (PR #1 addition).
- `make clean_build` / `make clean_all` — remove `build/`, `dist/`, `*.egg-info`, caches, and docs output.

## Rules

1. Declare dependency changes in `extra-requirements.txt`, not in `uv.lock` or `requirements.txt` by hand.
2. Keep `conda/meta.yaml` version in sync with `gptc/__init__.py`; `make check_metadata` enforces this.
3. Keep `setup.py` console script and `conda/meta.yaml` entry point in sync (`gptc_cli:main`).
4. Run `make check_metadata` and `make verify-dist` in CI before any release.
5. Do not commit `build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `*.pyc`, or `*.so` (see `.gitignore` and CONTRIBUTING.md "Repository Hygiene").
