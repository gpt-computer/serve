FROM gptcomputer/gptc:test-pip

ADD *.py mwu_encoder.yml ./

ENTRYPOINT ["gptc", "executor", "--uses", "mwu_encoder.yml"]
