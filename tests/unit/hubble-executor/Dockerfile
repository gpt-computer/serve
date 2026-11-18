FROM gptcomputer/gptc:test-pip

ADD *.py *.yml ./

ENTRYPOINT ["gptc", "pod", "--uses", "config.yml"]