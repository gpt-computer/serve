FROM gptcomputer/gptc:test-pip

ADD runtime.py ./
ENV GPTC_LOG_LEVEL=DEBUG

ENTRYPOINT ["python", "runtime.py"]