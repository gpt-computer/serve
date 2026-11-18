from docarray import DocumentArray

from gptc import requests
from gptc.serve.executors import BaseExecutor


class DummyExternalIndexer(BaseExecutor):
    @requests
    def index(self, docs: DocumentArray, **kwargs):
        for doc in docs:
            doc.text = "indexed"
