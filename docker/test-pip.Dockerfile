ARG PY_VERSION=3.10

FROM golang:1.19-bookworm AS go

FROM python:${PY_VERSION}-slim-bookworm

ARG DOCARRAY_VERSION
ARG PYDANTIC_VERSION
ARG PIP_TAG

RUN apt-get update && apt-get install --no-install-recommends -y gcc libc6-dev net-tools procps htop lsof dnsutils pkg-config wget && \
    rm -rf /var/lib/apt/lists/*

COPY --from=go /usr/local/go /usr/local/go
ENV PATH="/usr/local/go/bin:${PATH}" \
    GOPATH="/go" \
    GOBIN="/go/bin"

COPY . /gptc/

RUN cd /gptc && pip install --no-cache-dir ."${PIP_TAG}"

RUN if [ -z "$DOCARRAY_VERSION" ]; then echo "DOCARRAY_VERSION is not provided"; else pip install --no-cache-dir "docarray==${DOCARRAY_VERSION}"; fi
RUN if [ -z "$PYDANTIC_VERSION" ]; then echo "PYDANTIC_VERSION is not provided"; else pip install --no-cache-dir "pydantic${PYDANTIC_VERSION}"; fi

RUN useradd --create-home --shell /bin/sh gptc

USER gptc
WORKDIR /home/gptc

ENV GPTC_OPTOUT_TELEMETRY='true' \
    GRPC_ENABLE_FORK_SUPPORT='0' \
    GPTC_LOG_LEVEL='DEBUG'

ENTRYPOINT ["gptc"]
