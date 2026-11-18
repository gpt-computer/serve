(executor-cookbook)=
# Executor

An {class}`~gptc.Executor` is a self-contained service that performs a task on `Documents`. 

You can create an Executor by extending the `Executor` class and adding logic to endpoint methods.

## Why use Executors?

Once you've learned about `Documents` and `DocList` from [docarray](https://docs.docarray.org/), you can use all its power and expressiveness to build a multimodal application.
But what if you want to go bigger? Organize your code into modules, serve and scale them? That's where Executors come in.

- Executors let you organize functions into logical entities that can share configuration state, following OOP.
- Executors can be easily containerized and shared with your colleagues using `gptc hub push/pull`.
- Executors can be exposed as a service over gRPC or HTTP using `~gptc.Deployment`.
- Executors can be chained together to form a `~gptc.Flow`.

## Minimum working example

```python
from gptc import Executor, requests, Deployment
from docarray import DocList
from docarray.documents import TextDoc


class MyExecutor(Executor):
    @requests
    def foo(self, docs: DocList[TextDoc], **kwargs) -> DocList[TextDoc]:
        for d in docs:
            d.text = 'hello world'
        return docs


with Deployment(uses=MyExecutor) as dep:
    response_docs = dep.post(on='/', inputs=DocList[TextDoc]([TextDoc(text='hello')]), return_type=DocList[TextDoc])
    print(f'Text: {response_docs[0].text}')
```

```text
─────────────────────── 🎉 Deployment is ready to serve! ───────────────────────
╭────────────── 🔗 Endpoint ───────────────╮
│  ⛓     Protocol                    GRPC │
│  🏠       Local           0.0.0.0:55581  │
│  🔒     Private       192.168.0.5:55581  │
│  🌍      Public    158.181.77.236:55581  │
╰──────────────────────────────────────────╯
Text: hello world
```

```{toctree}
:hidden:

create
add-endpoints
serve
dynamic-batching
health-check
hot-reload
file-structure
containerize
instrumentation
yaml-spec
```
