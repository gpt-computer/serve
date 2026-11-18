# !!! An ARG declared before a FROM is outside of a build stage, so it can’t be used in any instruction after a FROM
ARG PY_VERSION=3.10

FROM python:${PY_VERSION}-slim-bookworm AS gptc_dep

ARG PIP_TAG
ARG APT_PACKAGES="gcc libc-dev"
ARG VCS_REF
ARG PY_VERSION
ARG BUILD_DATE
ARG GPTC_VERSION
ARG TARGETPLATFORM
ARG PIP_EXTRA_INDEX_URL=""
ARG PIP_INSTALL_CORE
ARG PIP_INSTALL_PERF

LABEL org.opencontainers.image.vendor="GPT::C0MPUTΞR" \
      org.opencontainers.image.licenses="Apache 2.0" \
      org.opencontainers.image.title="Gptc" \
      org.opencontainers.image.description="Build multimodal AI services via cloud native technologies" \
      org.opencontainers.image.authors="hello@khulnasoft.com" \
      org.opencontainers.image.url="https://github.com/gpt-computer/gptc" \
      org.opencontainers.image.documentation="https://gpt-computer.github.io/serve"

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GPTC_PIP_INSTALL_CORE=${PIP_INSTALL_CORE} \
    GPTC_PIP_INSTALL_PERF=${PIP_INSTALL_PERF}

COPY extra-requirements.txt setup.py /tmp/

RUN cd /tmp/ && \
    if [ -n "${APT_PACKAGES}" ]; then apt-get update && \
    apt-get install --no-install-recommends -y ${APT_PACKAGES}; fi && \
    if [ "$PY_VERSION" = "3.11" ]; then apt-get install --no-install-recommends -y build-essential ; fi && \
    if [ -n "${PIP_TAG}" ]; then pip install --default-timeout=1000 --compile --extra-index-url "${PIP_EXTRA_INDEX_URL}" ".[${PIP_TAG}]" ; fi && \
    pip install --default-timeout=1000 --compile --extra-index-url "${PIP_EXTRA_INDEX_URL}" . && \
    if [ -n "${APT_PACKAGES}" ]; then apt-get remove -y --auto-remove ${APT_PACKAGES} && apt-get clean && rm -rf /var/lib/apt/lists/*; fi && \
    rm -rf /tmp/*

FROM gptc_dep AS gptc

ARG VCS_REF
ARG BUILD_DATE
ARG GPTC_VERSION

LABEL org.opencontainers.image.created=${BUILD_DATE} \
      org.opencontainers.image.source="https://github.com/gpt-computer/gptc/commit/${VCS_REF}" \
      org.opencontainers.image.version=${GPTC_VERSION} \
      org.opencontainers.image.revision=${VCS_REF}

ENV GPTC_VERSION=${GPTC_VERSION} \
    GPTC_VCS_VERSION=${VCS_REF} \
    GPTC_BUILD_DATE=${BUILD_DATE}

COPY . /gptc/

RUN cd /gptc && \
    pip install --no-deps --compile . && \
    rm -rf /tmp/* /gptc && \
    useradd --create-home --shell /bin/sh gptc

USER gptc
WORKDIR /home/gptc

ENTRYPOINT ["gptc"]
