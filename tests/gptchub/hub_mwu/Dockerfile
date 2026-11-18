FROM gptcomputer/gptc:test-pip

ADD *.py mwu_encoder.yml ./
ENV GPTC_LOG_LEVEL=DEBUG
ENTRYPOINT ["gptc", "executor", "--uses", "mwu_encoder.yml"]