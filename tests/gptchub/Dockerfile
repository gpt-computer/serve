FROM gptcomputer/gptc:test-pip

WORKDIR /

COPY app.py flow.yml /
ENV GPTC_LOG_LEVEL=DEBUG
ENTRYPOINT ["python", "app.py"]
