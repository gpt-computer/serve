(gptc-env-vars)=
# {octicon}`list-unordered` Environment Variables

Gptc-serve uses environment variables to determine different behaviours. To see all supported environment variables and their current values, run:

```bash
gptc -vf
```

If you use containerized Executors (including {ref}`Kubernetes <kubernetes>` and {ref}`Docker Compose <docker-compose>`), you can pass separate environment variables to each Executor in the following way:


`````{tab} FLow YAML

```yaml
jtype: Flow
with: {}
executors:
- name: executor0
  port: 49583
  env:
    GPTC_LOG_LEVEL: DEBUG
    MYSECRET: ${{ ENV.MYSECRET }}
- name: executor1
  port: 62156
  env:
    GPTC_LOG_LEVEL: INFO
    CUDA_VISIBLE_DEVICES: 1
```
`````
`````{tab} Deployment YAML

```yaml
jtype: Deployment
with:
  name: executor0
  port: 49583
  env:
    GPTC_LOG_LEVEL: DEBUG
    MYSECRET: ${{ ENV.MYSECRET }}
```
`````
````{tab} Python API

```python
from gptc import Flow
import os

secret = os.environ['MYSECRET']
f = (
    Flow()
    .add(env={'GPTC_LOG_LEVEL': 'DEBUG', 'MYSECRET': secret})
    .add(env={'GPTC_LOG_LEVEL': 'INFO', 'CUDA_VISIBLE_DEVICES': 1})
)
f.save_config("envflow.yml")
```
````

The following environment variables are used internally in Gptc:

| Environment variable          | Description                                                                                                                                                                                     |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `GPTC_AUTH_TOKEN`             | Authentication token of Gptc Cloud                                                                                                                                                              |
| `GPTC_DEFAULT_HOST`           | Default host where server is exposed                                                                                                                                                    |
| `GPTC_DEFAULT_TIMEOUT_CTRL`   | Default timeout time used by Flow to check readiness of Executors                                                                                                                       |
| `GPTC_DEPLOYMENT_NAME`        | Name of deployment, used by Head Runtime in Kubernetes to connect to different deployments                                                                                          |
| `GPTC_DISABLE_UVLOOP`         | If set, Gptc will not use uvloop event loop for concurrent execution                                                                                                                            |
| `GPTC_FULL_CLI`               | If set, all CLI options will be shown in help                                                                                                                                                                                                                                                            |
| `GPTC_GATEWAY_IMAGE`          | Used when exporting a Flow to Kubernetes or Docker Compose to override default gateway image                                                                                                                                                                                                             |
| `GPTC_GRPC_RECV_BYTES`        | Set by gRPC service to keep track of received bytes                                                                                                                                     |
| `GPTC_GRPC_SEND_BYTES`        | Set by gRPC service to keep track of sent bytes                                                                                                                                         |
| `GPTC_K8S_ACCESS_MODES`       | Configures access modes for `PersistentVolumeClaim` attached to `StatefulSet`, when creating a `StatefulSet` in Kubernetes for an Executor using volumes. Defaults to '["ReadWriteOnce"]' |
| `GPTC_K8S_STORAGE_CAPACITY`   | Configures capacity for `PersistentVolumeClaim` attached to `StatefulSet`, when creating a `StatefulSet` in Kubernetes for an Executor using volumes. Defaults to '10G'                   |
| `GPTC_K8S_STORAGE_CLASS_NAME` | Configures storage class for `PersistentVolumeClaim` attached to `StatefulSet`, when creating a `StatefulSet` in Kubernetes for an Executor using volumes. Defaults to 'standard'         |
| `GPTC_LOCKS_ROOT`             | Root folder where file locks for concurrent Executor initialization                                                                                                                         |
| `GPTC_LOG_CONFIG`             | Configuration used for logger                                                                                                                                                           |
| `GPTC_LOG_LEVEL`              | Logging level used: INFO, DEBUG, WARNING                                                                                                                                                    |
| `GPTC_LOG_NO_COLOR`           | If set, disables color from rich console                                                                                                                                                        |
| `GPTC_MP_START_METHOD`        | Sets multiprocessing start method used by Gptc                                                                                                                                              |
| `GPTC_OPTOUT_TELEMETRY`       | If set, disables telemetry                                                                                                                                                                                                                                                                                            |
| `GPTC_RANDOM_PORT_MAX`        | Maximum port number used when selecting random ports to apply for Executors or Gateway                                                                                                                                                                                                                                                                                                                                                                                   |
| `GPTC_RANDOM_PORT_MIN`        | Minimum port number used when selecting random ports to apply for Executors or Gateway                                                                                                                                                                                                                                                                                                                                                                                   |
| `GPTC_STREAMER_ARGS`          | Gptc uses this variable to inject `GatewayStreamer` arguments into host environment running a Gateway                                                                                         |
