FROM gptcomputer/gptc:test-pip

ADD *.py mwu_encoder.yml ./

ENTRYPOINT ["gptc", "pod", "--uses", "mwu_encoder.yml"]