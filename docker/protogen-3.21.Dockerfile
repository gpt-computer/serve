FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential git autoconf libtool wget unzip zlib1g-dev pkg-config cmake && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /builder

RUN wget -q https://github.com/protocolbuffers/protobuf/releases/download/v21.5/protoc-21.5-linux-x86_64.zip -O protobuf.zip && \
    unzip protobuf.zip && rm protobuf.zip && \
    cp bin/protoc /usr/local/bin/ && \
    cp -r include/* /usr/local/include/ && \
    git clone --depth 1 --branch v1.48.0 https://github.com/grpc/grpc.git && \
    cd grpc && git submodule update --depth 1 --init && \
    mkdir -p cmake/build && cd cmake/build && cmake ../.. && make -j4

COPY gptc/proto/docarray_v2 /gptc/proto
COPY gptc/__init__.py /gptc/__init__.py

WORKDIR /gptc/proto

ENTRYPOINT ["bash", "./build-proto.sh", "/builder/grpc/cmake/build/grpc_python_plugin", "pb"]
