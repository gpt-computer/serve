FROM gptcomputer/gptc:test-pip

COPY . /executor_root/

WORKDIR /executor_root/SampleExecutor

ENTRYPOINT ["gptc", "executor", "--uses", "config.yml"]
