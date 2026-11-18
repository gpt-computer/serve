import datetime as _datetime
import os as _os
import sys as _sys
from pathlib import Path as _Path

__windows__ = _sys.platform == "win32"
__uptime__ = _datetime.datetime.now().isoformat()

# update on MacOS 1. clean this tuple, 2. grep -rohEI --exclude-dir=gptc/hub --exclude-dir=tests --include \*.py
# "\'GPTC_.*?\'" gptc  | sort -u | sed "s/$/,/g" 3. copy all lines EXCEPT the first (which is the grep command in the
# last line)
__gptc_env__ = (
    "GPTC_DEFAULT_HOST",
    "GPTC_DEFAULT_TIMEOUT_CTRL",
    "GPTC_DEPLOYMENT_NAME",
    "GPTC_DISABLE_UVLOOP",
    "GPTC_EARLY_STOP",
    "GPTC_FULL_CLI",
    "GPTC_GATEWAY_IMAGE",
    "GPTC_GRPC_RECV_BYTES",
    "GPTC_GRPC_SEND_BYTES",
    "GPTC_HUB_NO_IMAGE_REBUILD",
    "GPTC_LOG_CONFIG",
    "GPTC_LOG_LEVEL",
    "GPTC_LOG_NO_COLOR",
    "GPTC_MP_START_METHOD",
    "GPTC_OPTOUT_TELEMETRY",
    "GPTC_RANDOM_PORT_MAX",
    "GPTC_RANDOM_PORT_MIN",
    "GPTC_LOCKS_ROOT",
    "GPTC_OPTOUT_TELEMETRY",
    "GPTC_K8S_ACCESS_MODES",
    "GPTC_K8S_STORAGE_CLASS_NAME",
    "GPTC_K8S_STORAGE_CAPACITY",
    "GPTC_STREAMER_ARGS",
)

__default_host__ = _os.getenv(
    "GPTC_DEFAULT_HOST", "127.0.0.1" if __windows__ else "0.0.0.0"
)
__docker_host__ = "host.docker.internal"
__default_executor__ = "BaseExecutor"
__default_gateway__ = "BaseGateway"
__default_http_gateway__ = "HTTPGateway"
__default_composite_gateway__ = "CompositeGateway"
__default_websocket_gateway__ = "WebSocketGateway"
__default_grpc_gateway__ = "GRPCGateway"
__default_endpoint__ = "/default"
__dynamic_base_gateway_hubble__ = "gptcai+docker://gpt-computer/GptcGateway:latest"
__ready_msg__ = "ready and listening"
__stop_msg__ = "terminated"
__unset_msg__ = "(unset)"
__args_executor_func__ = {
    "docs",
    "parameters",
    "docs_matrix",
}
__args_executor_init__ = {"metas", "requests", "runtime_args"}
__resources_path__ = _os.path.join(
    _os.path.dirname(_sys.modules["gptc"].__file__), "resources"
)
__cache_path__ = f'{_os.path.expanduser("~")}/.cache/{__package__}'
if not _Path(__cache_path__).exists():
    _Path(__cache_path__).mkdir(parents=True, exist_ok=True)

_names_with_underscore = [
    "__version__",
    "__proto_version__",
    "__default_host__",
    "__ready_msg__",
    "__stop_msg__",
    "__gptc_env__",
    "__uptime__",
    "__default_endpoint__",
    "__default_executor__",
    "__unset_msg__",
    "__windows__",
]

__all__ = [_s for _s in dir() if not _s.startswith("_")] + _names_with_underscore

RAFT_TO_EXECUTOR_PORT = 100
