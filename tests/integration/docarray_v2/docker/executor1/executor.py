from typing import Optional

import numpy as np
from docarray import BaseDoc, DocList
from docarray.typing import NdArray

from gptc import Executor, requests


class MyDoc(BaseDoc):
    text: str
    embedding: Optional[NdArray] = None


class Encoder(Executor):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

    @requests
    def encode(self, docs: DocList[MyDoc], **kwargs) -> DocList[MyDoc]:
        for doc in docs:
            doc.embedding = np.random.random(128)
