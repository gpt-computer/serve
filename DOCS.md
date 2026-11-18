# Documentation build and generated-output ownership

This document records which files under `docs/` are hand-authored, which are generated, and where build output goes. It corresponds to PR #6 of the repository structure improvement plan. It is descriptive only — no docs files are moved or deleted here, and existing URLs are preserved.

## Generated vs hand-authored

### Generated (regenerated on every docs build)

| Path | Generator | Notes |
|---|---|---|
| `docs/api/*.rst` | `sphinxcontrib.apidoc` (conf.py:140-143) | One `automodule` page per `gptc` module, generated from docstrings. `apidoc_module_dir = ../`, `apidoc_output_dir = api`, `apidoc_separate_modules = True`. Regenerated in place during `sphinx-multiversion` build. |
| `docs/proto/docs.md` | `protoc-gen-doc` (`ghcr.io/gpt-computer/protoc-gen-doc`) | Generated from `gptc/proto/docarray_v1/` (local-only) or `gptc/proto/docarray_v2/` (full build) via `docs/makedoc.sh`. |
| `docs/_build/`, `docs/build/` | Sphinx (`sphinx-multiversion ... -b dirhtml`) | Build output. Primary output path is `docs/_build/dirhtml`. |

### Hand-authored

| Path | Role |
|---|---|
| `docs/api-rst.rst` | Hand-written index/overview using `autosummary` to point at key `gptc` classes. |
| `docs/index.md`, `docs/get-started/`, `docs/concepts/`, `docs/tutorials/`, `docs/cli/`, `docs/cloud-nativeness/`, `docs/envs/`, `docs/telemetry.md`, `docs/yaml-spec.md`, `docs/docarray-support.md`, `docs/Using_Gptc_on_Colab.ipynb` | User-authored guides, tutorials, and notebooks. |
| `docs/conf.py`, `docs/Makefile`, `docs/makedoc.sh`, `docs/redirects.txt`, `docs/_templates/`, `docs/_static/` | Sphinx configuration, build scripts, templates, and static assets. |

## Build workflow

`docs/makedoc.sh` is the entry point:

```bash
# local-only (fast, no multiversion)
cd docs
bash makedoc.sh local-only   # output in _build/dirhtml

# full multiversion build
export NUM_RELEASES=10
bash makedoc.sh              # output in _build/dirhtml
```

Steps (full build):
1. `rm -rf api && rm -rf _build/dirhtml` — clears generated API pages and build output.
2. `curl` GitHub release tags to build the `SMV_TAG_WHITELIST`.
3. `protoc-gen-doc` generates `docs/proto/docs.md` from proto sources.
4. `sphinx-multiversion . _build/dirhtml -b dirhtml` — builds HTML and runs `sphinxcontrib.apidoc` to (re)generate `docs/api/*.rst`.
5. Moves ` _build/dirhtml/<LATEST_VERSION>/*` into `_build/dirhtml`.

Local serving:
```bash
cd _build/dirhtml
python -m http.server
# http://localhost:8000
```

## Build output and Git

- `docs/_build/` and `docs/build/` are ignored by `.gitignore` (lines 73-74).
- A docs build regenerates `docs/api/*.rst` **in place**. If `docs/api/` is ever tracked, a build would dirty tracked files; keep `docs/api/` untracked or add a CI check that the build does not modify checked-in API pages.
- Never commit `_build/`, `build/`, or `docs/api/*.rst` unless there is a deliberate publication requirement.

## Media assets inventory

`docs/_static/` contains media with generic, hard-to-audit names (plan #4.6):

| Generic name | Suggested action |
|---|---|
| `download.wav`, `download (1).wav` … `download (5).wav` | Rename to descriptive names; add attribution/license notes |
| `hello.wav`, `olleh.wav` | Rename to descriptive names |
| `similar-audio-search-*.mp3`, `similar-audio-search-*.wav` | Keep descriptive; add attribution/license notes |
| `*.svg`, `*.png`, `*.gif`, `*.mp4`, `*.mp3` | Inventory third-party assets and licenses |

Create a lightweight asset attribution/licensing inventory (e.g. `docs/_static/ASSETS.md`) listing each media file, its source, and license.

## Rules

1. Treat `docs/api/*.rst` and `docs/proto/docs.md` as generated output — do not hand-edit them; edits will be overwritten on the next build.
2. Hand-authored content lives in `docs/api-rst.rst` and the guide/tutorial directories.
3. Build output goes to `docs/_build/dirhtml` (and `docs/build/`); both are gitignored.
4. Run `make clean_docs` (Makefile:118) to remove `docs/_build` and `docs/build` locally.
5. Preserve published URLs (`https://gpt-computer.github.io/serve/...`). Before moving any docs page, add a redirect in `docs/redirects.txt` (Sphinx `sphinxcontrib.redirects` is enabled, conf.py:108).
6. Do not reorganize the docs tree wholesale if existing URLs depend on its paths.
