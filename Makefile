.PHONY: all help check_tools check_metadata typecheck audit init install reinstall setup_uv add format format_check lint codespell fix_codespell tests unit_tests integration_tests coverage test_quick test_k8s test_docker_compose clean_python_cache clean_build clean_docs clean_all build build_sdist build_wheel install_local verify-dist proto verify-proto cli flow gateway docker_build docker_dev docs docs_install docs_build docs_serve help_test help_docker help_docs help_advanced

# Configurations
PKG_NAME=gptc
VERSION=$(shell grep '^__version__' gptc/__init__.py | sed -n "s/.*=[[:space:]]*['\"]\([^'\"]*\)['\"].*/\1/p")
PYTHON_REQUIRED=$(shell grep '^requires-python[[:space:]]*=' pyproject.toml | sed -n 's/.*"\([^"]*\)".*/\1/p')
DOCKER=docker
DOCKER_DIR=docker
SPHINXBUILD=.venv/bin/sphinx-build
RED=\033[0;31m
NC=\033[0m # No Color
GREEN=\033[0;32m
YELLOW=\033[1;33m
BLUE=\033[0;34m

test_path ?= tests/unit
args ?=
port ?= 8080
protocol ?= http
docs_port ?= 8000
all: help

######################
# UTILITIES
######################

# Clear directory contents in place (mount points in devcontainers must not be removed).
CLEAR_DIRS = $(foreach dir,$1,$(shell mkdir -p $(dir) && find $(dir) -mindepth 1 -delete))

check_tools: ## verify required tools are available
	@command -v uv >/dev/null 2>&1 || { echo >&2 "$(RED)uv is not installed. Aborting.$(NC)"; exit 1; }
	@command -v python >/dev/null 2>&1 || { echo >&2 "$(RED)python is not installed. Aborting.$(NC)"; exit 1; }
	@echo "$(GREEN)All required tools are installed.$(NC)"

check_metadata: ## verify packaging metadata is consistent
	@python scripts/check-metadata.py

typecheck: ## run scoped static type checks
	@uvx mypy gptc/types

audit: ## audit locked dependencies for known vulnerabilities
	@uv export --frozen --no-dev --no-emit-project --format requirements-txt -o /tmp/gptc-requirements.txt
	@uvx pip-audit -r /tmp/gptc-requirements.txt \
		--ignore-vuln PYSEC-2026-1308 \
		--ignore-vuln PYSEC-2026-1325 \
		--ignore-vuln PYSEC-2026-3447 \
		--ignore-vuln GHSA-xmj3-9gf7-h52w \
		--ignore-vuln PYSEC-2026-4298

help: ## show basic help message with common commands
	@echo ''
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)                GPT::C0MPUTΞR MAKE COMMANDS                        $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''
	@echo "$(GREEN)Basic Commands:$(NC)"
	@echo "  $(GREEN)make init$(NC)                - Initialize the project (install dependencies + hooks)"
	@echo "  $(GREEN)make cli$(NC)                 - Run the gptc CLI"
	@echo "  $(GREEN)make format$(NC)              - Format Python code with black"
	@echo "  $(GREEN)make lint$(NC)                - Run linters and pre-commit hooks"
	@echo "  $(GREEN)make typecheck$(NC)           - Run scoped mypy checks"
	@echo "  $(GREEN)make tests$(NC)               - Run unit and integration tests"
	@echo "  $(GREEN)make build$(NC)               - Build source and wheel distributions"
	@echo "  $(GREEN)make docs$(NC)                - Start the documentation server"
	@echo "  $(GREEN)make clean_all$(NC)           - Clean caches and build artifacts"
	@echo ''
	@echo "$(GREEN)Specialized Help Commands:$(NC)"
	@echo "  $(GREEN)make help_test$(NC)           - Show testing commands"
	@echo "  $(GREEN)make help_docker$(NC)         - Show Docker commands"
	@echo "  $(GREEN)make help_docs$(NC)           - Show documentation commands"
	@echo "  $(GREEN)make help_advanced$(NC)       - Show advanced/miscellaneous commands"
	@echo ''
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''

######################
# INSTALL PROJECT
######################

install: ## install project dependencies from the lockfile
	@echo 'Installing dependencies'
	@uv sync --frozen $(EXTRA_ARGS)

reinstall: ## force a clean reinstall of all dependencies
	@echo 'Reinstalling dependencies'
	@uv sync --frozen --reinstall

setup_uv: ## install uv using pipx
	pipx install uv

add: ## add a dependency (make add main="pkg" or dev="pkg")
	@echo 'Adding dependency'
ifdef main
	@uv add $(main)
endif
ifdef dev
	@uv add --group dev $(dev)
endif

init: check_tools ## initialize the project
	@$(MAKE) install
	@uvx pre-commit install
	@echo "$(GREEN)All requirements are installed.$(NC)"

######################
# CLEAN PROJECT
######################

clean_python_cache: ## remove Python cache files
	@echo "Cleaning Python cache..."
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.py[cod]' -exec rm -f {} +
	find . -type f -name '*~' -exec rm -f {} +
	$(call CLEAR_DIRS,.pytest_cache .mypy_cache .ruff_cache htmlcov cover)
	rm -f .darglint .coverage coverage.xml .coverage.*
	@echo "$(GREEN)Python cache cleaned.$(NC)"

clean_build: ## remove build distributions and egg-info
	@echo "Cleaning build artifacts..."
	$(call CLEAR_DIRS,build dist gptc.egg-info .eggs)
	@echo "$(GREEN)Build artifacts cleaned.$(NC)"

clean_docs: ## remove built documentation
	@echo "Cleaning documentation build..."
	$(call CLEAR_DIRS,docs/_build docs/build)
	@echo "$(GREEN)Documentation build cleaned.$(NC)"

clean_all: clean_python_cache clean_build clean_docs ## clean all caches and build artifacts
	@echo "$(GREEN)All caches and temporary directories cleaned.$(NC)"

######################
# CODE TESTS
######################

unit_tests: ## run unit tests (override with test_path=... args=...)
	@echo 'Running unit tests...'
	uv run pytest $(test_path) -ra $(args)

integration_tests: ## run integration tests
	@echo 'Running integration tests...'
	uv run pytest tests/integration -ra $(args)

tests: unit_tests integration_tests ## run unit and integration tests
	@echo "$(GREEN)All tests finished.$(NC)"

coverage: ## run unit tests and generate a coverage report
	@echo 'Running tests with coverage...'
	uv run pytest $(test_path) --cov=gptc --cov-report=term-missing --cov-report=xml

test_quick: ## run tests excluding slow ones
	uv run pytest $(test_path) -ra -m "not slow" $(args)

test_k8s: ## run Kubernetes integration tests
	uv run pytest tests/k8s -ra $(args)

test_docker_compose: ## run docker compose integration tests
	uv run pytest tests/docker_compose -ra $(args)

######################
# CODE QUALITY
######################

format: ## format Python code with black
	@echo 'Formatting Python code...'
	uv run black --config pyproject.toml gptc gptc_cli tests scripts

format_check: ## check formatting without modifying files
	@echo 'Checking Python formatting...'
	uv run black --check --config pyproject.toml gptc gptc_cli tests scripts

lint: ## run pre-commit hooks and docstring lint on changed files
	@echo 'Running linters...'
	uvx pre-commit run --all-files
	@CHANGED_FILES="$$(git diff --name-only --diff-filter=ACM $$(git merge-base HEAD origin/master 2>/dev/null || echo HEAD)..HEAD 2>/dev/null)"; \
		CHANGED_FILES="$$CHANGED_FILES" bash scripts/docstrings_lint.sh

codespell: ## check spelling
	@uvx codespell --skip="*.lock,*.json,gptc/proto/*,docs/proto/*"

fix_codespell: ## fix spelling errors automatically
	@uvx codespell --write --skip="*.lock,*.json,gptc/proto/*,docs/proto/*"

######################
# DEV / RUN
######################

cli: install ## run the gptc CLI
	uv run gptc $(args)

flow: install ## serve a flow with gptc (uses=flow.yml)
	uv run gptc flow --uses $(uses) --port $(port) --protocol $(protocol) $(args)

gateway: install ## start a standalone gateway
	uv run gptc gateway --port $(port) --protocol $(protocol) $(args)

######################
# BUILD
######################

build: build_sdist build_wheel ## build source and wheel distributions

build_sdist: ## build a source distribution
	@echo 'Building source distribution...'
	uv build --sdist

build_wheel: ## build a wheel distribution
	@echo 'Building wheel distribution...'
	uv build --wheel

install_local: build ## install the freshly built wheel locally
	uv pip install --force-reinstall dist/*.whl

verify-dist: build ## clean-environment check: build sdist+wheel, install wheel into a fresh venv, smoke-test imports
	@echo 'Verifying distributions in a clean environment...'
	@tmp_dir=$$(mktemp -d); \
	uv venv $$tmp_dir/venv --seed; \
	uv pip install --python $$tmp_dir/venv/bin/python --quiet dist/*.whl; \
	$$tmp_dir/venv/bin/python -c "import gptc; print('gptc', gptc.__version__)"; \
	$$tmp_dir/venv/bin/python -c "import jraft; print('jraft ok')"; \
	rm -rf $$tmp_dir; \
	echo "$(GREEN)Distribution verification passed.$(NC)"

######################
# DOCKER
######################
# Override the image with e.g. make docker_build FILE=dev.Dockerfile DOCKER=podman

FILE ?= debianx.Dockerfile
IMAGE ?= gptc:$(VERSION)

docker_build: ## build a Docker image from docker/
	@echo 'BUILDING IMAGE: $(DOCKER_DIR)/$(FILE) -> $(IMAGE)'
	@command -v $(DOCKER) >/dev/null 2>&1 || { echo "Error: $(DOCKER) is not installed. Try 'make docker_build DOCKER=docker'."; exit 1; }
	@$(DOCKER) build --rm -f $(DOCKER_DIR)/$(FILE) -t $(IMAGE) .

docker_dev: ## start a shell in the development container
	@echo 'Starting development container...'
	@$(DOCKER) build --rm -f $(DOCKER_DIR)/dev.Dockerfile -t gptc-dev .
	@$(DOCKER) run -it --rm --entrypoint sh -v "$(CURDIR):/gptc" gptc-dev

######################
# PROTOBUF
######################

PROTOC_IMAGE ?= gptcomputer/protogen

proto: ## regenerate protobuf Python modules using the published protogen images
	@echo 'Regenerating protobuf modules...'
	@command -v $(DOCKER) >/dev/null 2>&1 || { echo "$(RED)Error: $(DOCKER) is not installed.$(NC)"; exit 1; }
	@$(DOCKER) run --rm -v "$(CURDIR)/gptc/proto/docarray_v1:/gptc/proto" $(PROTOC_IMAGE)
	@$(DOCKER) run --rm -v "$(CURDIR)/gptc/proto/docarray_v2:/gptc/proto" $(PROTOC_IMAGE):v21

verify-proto: proto ## regenerate protobuf modules and fail if checked-in output differs (CI check)
	@git diff --quiet -- gptc/proto/ || { echo "$(RED)Protobuf bindings are out of date; run 'make proto' and commit the regenerated changes.$(NC)"; exit 1; }
	@echo "$(GREEN)Protobuf bindings are up to date.$(NC)"

######################
# DOCUMENTATION
######################

docs_install: ## install documentation dependencies
	@echo "$(GREEN)Installing documentation dependencies...$(NC)"
	@uv pip install -r docs/requirements.txt

docs: docs_build ## start the Sphinx documentation server
	@echo "$(GREEN)Starting documentation server at http://localhost:$(docs_port)$(NC)"
	@cd docs && python -m http.server $(docs_port) --directory _build/html

docs_build: docs_install ## build the documentation for production
	@echo "$(GREEN)Building documentation...$(NC)"
	@cd docs && ../$(SPHINXBUILD) -M html . _build
	@echo "$(GREEN)Documentation built in docs/_build/html$(NC)"

docs_serve: docs_build ## serve the built documentation locally
	@cd docs && python -m http.server $(docs_port) --directory _build/html

######################
# HELP COMMANDS
######################

help_test: ## show testing commands
	@echo ''
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)                      TESTING COMMANDS                              $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''
	@echo "  $(GREEN)make unit_tests$(NC)        - Run unit tests (default: tests/unit)"
	@echo "  $(GREEN)make integration_tests$(NC) - Run integration tests"
	@echo "  $(GREEN)make tests$(NC)             - Run all tests"
	@echo "  $(GREEN)make coverage$(NC)          - Run tests and generate a coverage report"
	@echo "  $(GREEN)make test_quick$(NC)        - Skip tests marked slow"
	@echo "  $(GREEN)make test_k8s$(NC)          - Run Kubernetes tests"
	@echo "  $(GREEN)make test_docker_compose$(NC) - Run docker compose tests"
	@echo ''
	@echo "$(YELLOW)Options:$(NC) test_path=tests/unit args=\"-x -v\""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''

help_docker: ## show Docker commands
	@echo ''
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)                      DOCKER COMMANDS                               $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''
	@echo "  $(GREEN)make docker_build$(NC)      - Build a Docker image from docker/"
	@echo "  $(GREEN)make docker_dev$(NC)        - Start the development container"
	@echo "  $(GREEN)make proto$(NC)             - Regenerate protobuf modules"
	@echo "  $(GREEN)make verify-proto$(NC)      - Regenerate protobuf modules and fail if checked-in output differs"
	@echo ''
	@echo "$(YELLOW)Options:$(NC) DOCKER=docker|podman FILE=dev.Dockerfile IMAGE=gptc:dev"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''

help_docs: ## show documentation commands
	@echo ''
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)                  DOCUMENTATION COMMANDS                            $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''
	@echo "  $(GREEN)make docs_install$(NC)      - Install documentation requirements"
	@echo "  $(GREEN)make docs$(NC)              - Build and serve documentation"
	@echo "  $(GREEN)make docs_build$(NC)        - Build documentation with Sphinx"
	@echo "  $(GREEN)make docs_serve$(NC)        - Serve built documentation"
	@echo "  $(GREEN)make clean_docs$(NC)        - Remove built documentation"
	@echo ''
	@echo "$(YELLOW)Options:$(NC) docs_port=8000"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''

help_advanced: ## show advanced and miscellaneous commands
	@echo ''
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)                    ADVANCED COMMANDS                               $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''
	@echo "$(GREEN)Cleanup:$(NC)"
	@echo "  $(GREEN)make clean_python_cache$(NC)  - Remove Python cache files"
	@echo "  $(GREEN)make clean_build$(NC)        - Remove distributions and egg-info"
	@echo "  $(GREEN)make clean_docs$(NC)         - Remove documentation build"
	@echo ''
	@echo "$(GREEN)Dependencies:$(NC)"
	@echo "  $(GREEN)make install$(NC)            - Install from uv.lock"
	@echo "  $(GREEN)make reinstall$(NC)          - Force reinstall dependencies"
	@echo "  $(GREEN)make add main=\"pkg\"$(NC)    - Add a runtime dependency"
	@echo "  $(GREEN)make add dev=\"pkg\"$(NC)     - Add a development dependency"
	@echo ''
	@echo "$(GREEN)Quality & metadata:$(NC)"
	@echo "  $(GREEN)make check_metadata$(NC)     - Validate packaging metadata consistency"
	@echo "  $(GREEN)make verify-dist$(NC)        - Build sdist+wheel, install wheel into a fresh venv, smoke-test imports"
	@echo "  $(GREEN)make typecheck$(NC)          - Run scoped mypy checks"
	@echo "  $(GREEN)make audit$(NC)              - Audit locked dependencies"
	@echo ''
	@echo "$(GREEN)Project info:$(NC)"
	@echo "  Package: $(PKG_NAME)  Version: $(VERSION)  Requires: $(PYTHON_REQUIRED)"
	@echo ''
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ''
