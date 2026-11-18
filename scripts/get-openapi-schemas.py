import json

from gptc.logging.logger import GptcLogger
from gptc.parsers import set_gateway_parser
from gptc.serve.runtimes.gateway.http_fastapi_app import get_fastapi_app
from gptc.serve.runtimes.gateway.streamer import GatewayStreamer

GPTC_LOGO_URL = "https://schemas.gpt-computer.github.io/logo/logo-product/gptc-core/horizontal-layout/colored/Product%20logo_Core_vertical_colorful%402x-margin.png"
GATEWAY_SCHEMA_FILENAME = "gateway.json"


args = set_gateway_parser().parse_args([])
logger = GptcLogger("")

graph_description = json.loads(args.graph_description)
graph_conditions = json.loads(args.graph_conditions)
deployments_addresses = json.loads(args.deployments_addresses)
deployments_no_reduce = json.loads(args.deployments_no_reduce)

streamer = GatewayStreamer(
    graph_representation=graph_description,
    executor_addresses=deployments_addresses,
    graph_conditions=graph_conditions,
    deployments_no_reduce=deployments_no_reduce,
    timeout_send=args.timeout_send,
    retries=args.retries,
    compression=args.compression,
    runtime_name=args.name,
    prefetch=args.prefetch,
    logger=logger,
)

gateway_app = get_fastapi_app(
    streamer=streamer,
    title=args.title,
    description=args.description,
    no_debug_endpoints=args.no_debug_endpoints,
    no_crud_endpoints=args.no_crud_endpoints,
    expose_endpoints=args.expose_endpoints,
    expose_graphql_endpoint=args.expose_graphql_endpoint,
    cors=args.cors,
    logger=logger,
)
gateway_schema = gateway_app.openapi()
gateway_schema["info"]["x-logo"] = {"url": GPTC_LOGO_URL}
gateway_schema["servers"] = []
gateway_schema["servers"].append(
    {"url": f"http://localhost:{args.port}", "description": "Local Gptc gateway"}
)
with open(GATEWAY_SCHEMA_FILENAME, "w", encoding="utf-8") as f:
    json.dump(gateway_schema, f)
