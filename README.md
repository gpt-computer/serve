# Gptc-Serve
<a href="https://pypi.org/project/gptc/"><img alt="PyPI" src="https://img.shields.io/pypi/v/gptc?label=Release&style=flat-square"></a>
<a href="https://discord.gptc.ai"><img src="https://img.shields.io/discord/1106542220112302130?logo=discord&logoColor=white&style=flat-square"></a>
<a href="https://pypistats.org/packages/gptc"><img alt="PyPI - Downloads from official pypistats" src="https://img.shields.io/pypi/dm/gptc?style=flat-square"></a>
<a href="https://github.com/gpt-computer/gptc/actions/workflows/cd.yml"><img alt="Github CD status" src="https://github.com/gpt-computer/gptc/actions/workflows/cd.yml/badge.svg"></a>

<!-- start gptc-description -->
Gptc-serve is a framework for building and deploying AI services that communicate via gRPC, HTTP and WebSockets. Scale your services from local development to production while focusing on your core logic.
<!-- end gptc-description -->

## Key Features

- Native support for all major ML frameworks and data types
- High-performance service design with scaling, streaming, and dynamic batching
- LLM serving with streaming output
- Built-in Docker integration and Executor Hub
- One-click deployment to GPT::C0MPUTΞR Cloud
- Enterprise-ready with Kubernetes and Docker Compose support

<details>
<summary><strong>Comparison with FastAPI</strong></summary>

Key advantages over FastAPI:

- DocArray-based data handling with native gRPC support
- Built-in containerization and service orchestration
- Seamless scaling of microservices
- One-command cloud deployment
</details>

## Install 

```bash
pip install gptc
```

See guides for [Apple Silicon](https://gpt-computer.github.io/serve/get-started/install/apple-silicon-m1-m2/) and [Windows](https://gpt-computer.github.io/serve/get-started/install/windows/).

## Development

Use [uv](https://docs.astral.sh/uv/) to set up a reproducible development environment:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
uv run pytest -v -s --ignore-glob='tests/integration/hub_usage/dummyhub*' tests
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full contributor guide.

## Core Concepts

Three main layers:
- **Data**: BaseDoc and DocList for input/output
- **Serving**: Executors process Documents, Gateway connects services
- **Orchestration**: Deployments serve Executors, Flows create pipelines

## Build AI Services

<!-- start build-ai-services -->
Let's create a gRPC-based AI service using StableLM:

```python
from gptc import Executor, requests
from docarray import DocList, BaseDoc
from transformers import pipeline


class Prompt(BaseDoc):
    text: str


class Generation(BaseDoc):
    prompt: str
    text: str


class StableLM(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generator = pipeline(
            'text-generation', model='stabilityai/stablelm-base-alpha-3b'
        )

    @requests
    def generate(self, docs: DocList[Prompt], **kwargs) -> DocList[Generation]:
        generations = DocList[Generation]()
        prompts = docs.text
        llm_outputs = self.generator(prompts)
        for prompt, output in zip(prompts, llm_outputs):
            generations.append(Generation(prompt=prompt, text=output))
        return generations
```

Deploy with Python or YAML:

```python
from gptc import Deployment
from executor import StableLM

dep = Deployment(uses=StableLM, timeout_ready=-1, port=12345)

with dep:
    dep.block()
```

```yaml
jtype: Deployment
with:
 uses: StableLM
 py_modules:
   - executor.py
 timeout_ready: -1
 port: 12345
```

Use the client:

```python
from gptc import Client
from docarray import DocList
from executor import Prompt, Generation

prompt = Prompt(text='suggest an interesting image generation prompt')
client = Client(port=12345)
response = client.post('/', inputs=[prompt], return_type=DocList[Generation])
```
<!-- end build-ai-services -->

## Build Pipelines

<!-- start build-pipelines -->
Chain services into a Flow:

```python
from gptc import Flow

flow = Flow(port=12345).add(uses=StableLM).add(uses=TextToImage)

with flow:
    flow.block()
```
<!-- end build-pipelines -->

## Scaling and Deployment

### Local Scaling

Boost throughput with built-in features:
- Replicas for parallel processing
- Shards for data partitioning
- Dynamic batching for efficient model inference

Example scaling a Stable Diffusion deployment:

```yaml
jtype: Deployment
with:
 uses: TextToImage
 timeout_ready: -1
 py_modules:
   - text_to_image.py
 env:
  CUDA_VISIBLE_DEVICES: RR
 replicas: 2
 uses_dynamic_batching:
   /default:
     preferred_batch_size: 10
     timeout: 200
```

### Cloud Deployment

#### Containerize Services

1. Structure your Executor:
```
TextToImage/
├── executor.py
├── config.yml
├── requirements.txt
```

2. Configure:
```yaml
# config.yml
jtype: TextToImage
py_modules:
 - executor.py
metas:
 name: TextToImage
 description: Text to Image generation Executor
```

3. Push to Hub:
```bash
gptc hub push TextToImage
```

#### Deploy to Kubernetes
```bash
gptc export kubernetes flow.yml ./my-k8s
kubectl apply -R -f my-k8s
```

#### Use Docker Compose
```bash
gptc export docker-compose flow.yml docker-compose.yml
docker-compose up
```

#### JCloud Deployment

Deploy with a single command:
```bash
gptc cloud deploy jcloud-flow.yml
```

## LLM Streaming

<!-- start llm-streaming-intro -->
Enable token-by-token streaming for responsive LLM applications:
<!-- end llm-streaming-intro -->

<!-- start llm-streaming-schemas -->
1. Define schemas:
```python
from docarray import BaseDoc


class PromptDocument(BaseDoc):
    prompt: str
    max_tokens: int


class ModelOutputDocument(BaseDoc):
    token_id: int
    generated_text: str
```
<!-- end llm-streaming-schemas -->

<!-- start llm-streaming-init -->
2. Initialize service:
```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel


class TokenStreamingExecutor(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
```
<!-- end llm-streaming-init -->

<!-- start llm-streaming-endpoint -->
3. Implement streaming:
```python
@requests(on='/stream')
async def task(self, doc: PromptDocument, **kwargs) -> ModelOutputDocument:
    input = tokenizer(doc.prompt, return_tensors='pt')
    input_len = input['input_ids'].shape[1]
    for _ in range(doc.max_tokens):
        output = self.model.generate(**input, max_new_tokens=1)
        if output[0][-1] == tokenizer.eos_token_id:
            break
        yield ModelOutputDocument(
            token_id=output[0][-1],
            generated_text=tokenizer.decode(
                output[0][input_len:], skip_special_tokens=True
            ),
        )
        input = {
            'input_ids': output,
            'attention_mask': torch.ones(1, len(output[0])),
        }
```
<!-- end llm-streaming-endpoint -->

<!-- start llm-streaming-serve -->
4. Serve and use:
```python
# Server
with Deployment(uses=TokenStreamingExecutor, port=12345, protocol='grpc') as dep:
    dep.block()


# Client
async def main():
    client = Client(port=12345, protocol='grpc', asyncio=True)
    async for doc in client.stream_doc(
        on='/stream',
        inputs=PromptDocument(prompt='what is the capital of France ?', max_tokens=10),
        return_type=ModelOutputDocument,
    ):
        print(doc.generated_text)
```
<!-- end llm-streaming-serve -->

## Support

<!-- start support-pitch -->
Gptc-serve is backed by [GPT::C0MPUTΞR](https://gptc.ai) and licensed under [Apache-2.0](./LICENSE).
<!-- end support-pitch -->
