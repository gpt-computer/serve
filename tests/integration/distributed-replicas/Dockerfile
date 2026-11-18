FROM gptcomputer/gptc:test-pip

COPY . /executor_root/

WORKDIR /executor_root

ENTRYPOINT ["gptc", "executor", "--uses", "config.yml"]