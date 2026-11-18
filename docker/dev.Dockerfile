ARG PY_VERSION=3.10

FROM ghcr.io/astral-sh/uv:python${PY_VERSION}-bookworm-slim

ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1 \
    UV_HTTP_TIMEOUT=300

WORKDIR /gptc

COPY pyproject.toml uv.lock README.md ./
COPY setup.py extra-requirements.txt fastentrypoints.py ./
COPY gptc ./gptc
COPY gptc_cli ./gptc_cli

RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "gptc"]
