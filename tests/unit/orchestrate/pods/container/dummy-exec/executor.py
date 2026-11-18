import os

from gptc import Executor, requests


class DummyExec(Executor):
    @requests
    def foo(self, **kwargs):
        pass
