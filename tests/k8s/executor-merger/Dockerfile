# TODO use fixed gptc version for deterministic execution
FROM gptcomputer/gptc:test-pip

COPY . /workspace
WORKDIR /workspace

ENTRYPOINT ["gptc", "executor", "--uses", "config.yml"]
