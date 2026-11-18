FROM gptcomputer/gptc:test-pip

ADD executor.py executor.yml ./

ENTRYPOINT ["gptc", "executor", "--uses", "executor.yml"]