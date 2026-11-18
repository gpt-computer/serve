FROM gptcomputer/gptc:latest-py38-standard

COPY . /workdir/
WORKDIR /workdir

ENTRYPOINT ["gptc", "gateway", "--uses", "config.yml"]