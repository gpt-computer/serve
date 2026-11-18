FROM gptcomputer/gptc:test-pip

# setup the workspace
COPY . /workspace
WORKDIR /workspace

ENTRYPOINT ["gptc", "executor", "--uses", "default_config.yml"]
