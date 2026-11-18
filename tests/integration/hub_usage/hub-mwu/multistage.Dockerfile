FROM gptcomputer/gptc:test-pip as base

ADD *.py mwu_encoder.yml ./

FROM base

ADD README.md ./

FROM base

ENTRYPOINT ["gptc", "pod", "--uses", "mwu_encoder.yml"]