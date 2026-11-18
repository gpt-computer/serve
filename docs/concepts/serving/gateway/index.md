(gateway)=

# Gateway

Every {class}`~gptc.Flow` has a Gateway component that receives requests over the network, allowing clients to send data
to the Flow for processing.

The Gateway is the first destination of a client request and its final destination, meaning that all incoming requests
are routed to the Gateway and the Gateway is responsible for handling and responding to those requests. The Gateway
supports multiple protocols and endpoints, such as gRPC, HTTP, WebSocket, and GraphQL, allowing clients to communicate
with the Flow using the protocol of their choice.

In most cases, the Gateway is automatically configured when you initialize a Flow object, so you do not need to
configure it yourself. 

However, you can always explicitly configure the Gateway in Python using the
{meth}`~gptc.Flow.config_gateway` method, or in YAML. The full YAML specification for configuring the Gateway can be
{ref}`found here<gateway-yaml-spec>`.

(flow-protocol)=
## Set protocol in Python

You can use three different protocols to serve the `Flow`: gRPC, HTTP and WebSocket.

````{tab} gRPC

```{code-block} python
---
emphasize-lines: 12, 14
---

from gptc import Client, Executor, Flow, requests
from docarray import DocList
from docarray.documents import TextDoc

class FooExecutor(Executor):
    @requests
    def foo(self, docs: DocList[TextDoc], **kwargs) -> DocList[TextDoc]:
        for doc in docs:
            doc.text = 'foo was called'


f = Flow().config_gateway(protocol='grpc', port=12345).add(uses=FooExecutor)
with f:
    client = Client(port=12345)
    docs = client.post(on='/', inputs=TextDoc(), return_type=DocList[TextDoc])
    print(docs.text)
```

```text
['foo was called']
```
````

````{tab} HTTP
```{code-block} python
---
emphasize-lines: 12, 14
---

from gptc import Client, Executor, Flow, requests
from docarray import DocList
from docarray.documents import TextDoc

class FooExecutor(Executor):
    @requests
    def foo(self, docs: DocList[TextDoc], **kwargs) -> DocList[TextDoc]:
        for doc in docs:
            doc.text = 'foo was called'


f = Flow().config_gateway(protocol='http', port=12345).add(uses=FooExecutor)
with f:
    client = Client(port=12345, protocol='http')
    docs = client.post(on='/', inputs=TextDoc(), return_type=DocList[TextDoc])
    print(docs.text)
```

```text
['foo was called']
```

````

````{tab} WebSocket

```{code-block} python
---
emphasize-lines: 12, 14
---

from gptc import Client, Executor, Flow, requests
from docarray import DocList
from docarray.documents import TextDoc

class FooExecutor(Executor):
    @requests
    def foo(self, docs: DocList[TextDoc], **kwargs) -> DocList[TextDoc]:
        for doc in docs:
            doc.text = 'foo was called'


f = Flow().config_gateway(protocol='websocket', port=12345).add(uses=FooExecutor)
with f:
    client = Client(port=12345, protocol='websocket')
    docs = client.post(on='/', inputs=TextDoc(), return_type=DocList[TextDoc])
    print(docs.text)
```

```text
['foo was called']
```
````

## Set protocol in YAML

To configure the protocol in a YAML file:

````{tab} gRPC
Note that gRPC is the default protocol, so you can just omit it.
```{code-block} yaml
jtype: Flow
gateway:
  protocol: 'grpc'
```

````

````{tab} HTTP
```{code-block} yaml
jtype: Flow
gateway:
  protocol: 'http'
```


````

````{tab} WebSocket

```{code-block} yaml
jtype: Flow
gateway:
  protocol: 'websocket'
```

````

## Enable multiple protocols

You can enable multiple protocols on the Gateway. This allows polyglot clients connect to your Flow with different
protocols.

````{tab} Python
```{code-block} python
---
emphasize-lines: 2
---
from gptc import Flow
flow = Flow().config_gateway(protocol=['grpc', 'http', 'websocket'])
with flow:
    flow.block()
```
````

````{tab} YAML
```yaml
jtype: Flow
gateway:
  protocol:
    - 'grpc'
    - 'http'
    - 'websocket'
```
````

```{figure} multi-protocol-flow.png
:width: 70%
```

```{admonition} Important
:class: important

In case you want to serve a Flow using multiple protocols, make sure to specify as much ports as protocols used. 
```

(custom-http)=

(flow-tls)=

## Enable TLS for client traffics

You can enable TLS encryption between your Gateway and Clients, for any of the protocols supported by Gptc-serve (HTTP, gRPC,
and WebSocket).

````{admonition} Caution
:class: caution
Enabling TLS will encrypt the data that is transferred between the Flow and the Client.
Data that is passed between the microservices configured by the Flow, such as Executors, will **not** be encrypted.
````

To enable TLS encryption, you need to pass a valid *keyfile* and *certfile* to the Flow, using
the `ssl_keyfile` `ssl_certfile`
parameters:

```python
from gptc import Flow

Flow().config_gateway(
    port=12345,
    ssl_certfile='path/to/certfile.crt',
    ssl_keyfile='path/to/keyfile.crt',
)
```

If both of these are provided, the Flow will automatically configure itself to use TLS encryption for its communication
with any Client.

(server-compress)=

## Enable in-Flow compression

The communication between {class}`~gptc.Executor`s inside a {class}`~gptc.Flow` is done via gRPC. To optimize the
performance and the bandwidth of these connections, you can
enable [compression](https://grpc.github.io/grpc/python/grpc.html#compression) by specifying `compression` argument to
the Gateway.

The supported methods are: none, `gzip` and `deflate`.

```python
from gptc import Flow

f = Flow().config_gateway(compression='gzip').add(...)
```

Note that this setting is only effective the internal communication of the Flow.
One can also specify the compression between client and gateway {ref}`as described here<client-compress>`.

## Get environment information

Gateway provides an endpoint that exposes environment information where it runs.

It is a dict-like structure with the following keys:

- `gptc`: A dictionary containing information about the system and the versions of several packages including gptc
  package itself
- `envs`: A dictionary containing all the values if set of the {ref}`environment variables used in Gptc-serve <gptc-serve-env-vars>`

### Use gRPC

To see how this works, first instantiate a Flow with an Executor exposed to a specific port and block it for serving:

```python
from gptc import Flow

with Flow().config_gateway(protocol=['grpc'], port=12345) as f:
    f.block()
```

Then, you can use [grpcurl](https://github.com/fullstorydev/grpcurl)  sending status check request to the Gateway.

```shell
docker pull fullstorydev/grpcurl:latest
docker run --network='host' fullstorydev/grpcurl -plaintext 127.0.0.1:12345 gptc.GptcInfoRPC/_status
```

The error-free output below signifies a correctly running Gateway:

```json
{
  "gptc": {
    "architecture": "######",
    "ci-vendor": "######",
    "docarray": "######",
    "grpcio": "######",
    "gptc": "######",
    "gptc-proto": "######",
    "gptc-vcs-tag": "######",
    "platform": "######",
    "platform-release": "######",
    "platform-version": "######",
    "processor": "######",
    "proto-backend": "######",
    "protobuf": "######",
    "python": "######",
    "pyyaml": "######",
    "session-id": "######",
    "uid": "######",
    "uptime": "######"
  },
  "envs": {
    "GPTC_AUTH_TOKEN": "(unset)",
    "GPTC_DEFAULT_HOST": "(unset)",
    "GPTC_DEFAULT_TIMEOUT_CTRL": "(unset)",
    "GPTC_DEPLOYMENT_NAME": "(unset)",
    "GPTC_DISABLE_HEALTHCHECK_LOGS": "(unset)",
    "GPTC_DISABLE_UVLOOP": "(unset)",
    "GPTC_EARLY_STOP": "(unset)",
    "GPTC_FULL_CLI": "(unset)",
    "GPTC_GATEWAY_IMAGE": "(unset)",
    "GPTC_GRPC_RECV_BYTES": "(unset)",
    "GPTC_GRPC_SEND_BYTES": "(unset)",
    "GPTC_HUBBLE_REGISTRY": "(unset)",
    "GPTC_HUB_NO_IMAGE_REBUILD": "(unset)",
    "GPTC_LOCKS_ROOT": "(unset)",
    "GPTC_LOG_CONFIG": "(unset)",
    "GPTC_LOG_LEVEL": "(unset)",
    "GPTC_LOG_NO_COLOR": "(unset)",
    "GPTC_MP_START_METHOD": "(unset)",
    "GPTC_RANDOM_PORT_MAX": "(unset)",
    "GPTC_RANDOM_PORT_MIN": "(unset)"
  }
}
```

```{tip}
You can also use it to check Executor status, as Executor's communication protocol is gRPC.
```

(gateway-grpc-server-options)=
### Configure Gateway gRPC options

The {class}`~gptc.Gateway` supports the `grpc_server_options` parameter which allows more customization of the **gRPC**
server. The `grpc_server_options` parameter accepts a dictionary of **gRPC** configuration options which will be
used to overwrite the default options. The **gRPC** channel used for server to server communication can also be
customized using the `grpc_channel_options` parameter.

The default **gRPC** options are:

```
('grpc.max_send_message_length', -1),
('grpc.max_receive_message_length', -1),
('grpc.keepalive_time_ms', 9999),
# send keepalive ping every 9 second, default is 2 hours.
('grpc.keepalive_timeout_ms', 4999),
# keepalive ping time out after 4 seconds, default is 20 seconds
('grpc.keepalive_permit_without_calls', True),
# allow keepalive pings when there's no gRPC calls
('grpc.http1.max_pings_without_data', 0),
# allow unlimited amount of keepalive pings without data
('grpc.http1.min_time_between_pings_ms', 10000),
# allow grpc pings from client every 9 seconds
('grpc.http1.min_ping_interval_without_data_ms', 5000),
# allow grpc pings from client without data every 4 seconds
```

Refer to the [channel_arguments](https://grpc.github.io/grpc/python/glossary.html#term-channel_arguments) section for
the full list of available **gRPC** options.

```{hint}
:class: seealso
Refer to the {ref}`Configure gRPC Client options <client-grpc-channel-options>` section for configuring the `Client` **gRPC** channel options.
Refer to the {ref}`Configure Executor gRPC options <executor-grpc-channel-options>` section for configuring the `Executor` **gRPC** options.
```

### Use HTTP/WebSocket

When using HTTP or WebSocket as the Gateway protocol, you can use curl to target the `/status` endpoint and get the Gptc-serve
info.

```shell
curl http://localhost:12345/status
```

```json
{
  "gptc": {
    "gptc": "######",
    "docarray": "######",
    "gptc-proto": "######",
    "gptc-vcs-tag": "(unset)",
    "protobuf": "######",
    "proto-backend": "######",
    "grpcio": "######",
    "pyyaml": "######",
    "python": "######",
    "platform": "######",
    "platform-release": "######",
    "platform-version": "######",
    "architecture": "######",
    "processor": "######",
    "uid": "######",
    "session-id": "######",
    "uptime": "######",
    "ci-vendor": "(unset)"
  },
  "envs": {
    "GPTC_AUTH_TOKEN": "(unset)",
    "GPTC_DEFAULT_HOST": "(unset)",
    "GPTC_DEFAULT_TIMEOUT_CTRL": "(unset)",
    "GPTC_DEPLOYMENT_NAME": "(unset)",
    "GPTC_DISABLE_UVLOOP": "(unset)",
    "GPTC_EARLY_STOP": "(unset)",
    "GPTC_FULL_CLI": "(unset)",
    "GPTC_GATEWAY_IMAGE": "(unset)",
    "GPTC_GRPC_RECV_BYTES": "(unset)",
    "GPTC_GRPC_SEND_BYTES": "(unset)",
    "GPTC_HUBBLE_REGISTRY": "(unset)",
    "GPTC_HUB_NO_IMAGE_REBUILD": "(unset)",
    "GPTC_LOG_CONFIG": "(unset)",
    "GPTC_LOG_LEVEL": "(unset)",
    "GPTC_LOG_NO_COLOR": "(unset)",
    "GPTC_MP_START_METHOD": "(unset)",
    "GPTC_RANDOM_PORT_MAX": "(unset)",
    "GPTC_RANDOM_PORT_MIN": "(unset)",
    "GPTC_DISABLE_HEALTHCHECK_LOGS": "(unset)",
    "GPTC_LOCKS_ROOT": "(unset)"
  }
}
```

(gateway-logging-configuration)=
## Custom logging configuration

The {ref}`Custom logging configuration <logging-configuration>` section describes customizing the logging configuration for all entities of the `Flow`.
The `Gateway` logging can also be individually configured using a custom `logging.json.yml` file as in the below example. The custom logging file
`logging.json.yml` is described in more detail in the {ref}`Custom logging configuration <logging-configuration>` section.

````{tab} Python
```python
from gptc import Flow

f = Flow().config_gateway(log_config='./logging.json.yml')
```
````

````{tab} YAML
```yaml
jtype: Flow
gateway:
  log_config: './logging.json.yml'
```
````


## See also

- {ref}`Access the Flow with the Client <client>`
- {ref}`Deployment with Kubernetes <kubernetes>`
- {ref}`Deployment with Docker Compose <docker-compose>`

```{toctree}
:hidden:

health-check
rate-limit
customize-http-endpoints
customization
yaml-spec
```
