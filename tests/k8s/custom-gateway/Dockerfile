FROM gptcomputer/gptc:test-pip

COPY . /workdir/
WORKDIR /workdir

ENTRYPOINT ["gptc", "gateway", "--uses", "config.yml"]