ARG PY_VERSION=3.10

FROM golang:1.19-bookworm AS go

FROM python:${PY_VERSION}-slim-bookworm

ARG PIP_TAG

RUN apt-get update && apt-get install --no-install-recommends -y gcc libc6-dev net-tools procps htop lsof dnsutils pkg-config wget && \
    rm -rf /var/lib/apt/lists/*

RUN if [ "$PY_VERSION" = "3.11" ]; then apt-get update && apt-get install --no-install-recommends -y build-essential && rm -rf /var/lib/apt/lists/*; fi

COPY --from=go /usr/local/go /usr/local/go
ENV PATH="/usr/local/go/bin:${PATH}" \
    GOPATH="/go" \
    GOBIN="/go/bin"

COPY . /gptc/

RUN cd /gptc && pip install --no-cache-dir ."${PIP_TAG}" && \
    useradd --create-home --shell /bin/sh gptc

USER gptc
WORKDIR /home/gptc

ENTRYPOINT ["gptc"]
