from docarray import DocList
from docarray.documents import TextDoc

from gptc import Executor, requests


class WrongSchemaExec(Executor):
    @requests
    def foo(self, docs: TextDoc, **kwargs) -> DocList[TextDoc]:
        pass
