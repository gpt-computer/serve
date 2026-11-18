import argparse

from gptc.helper import parse_host_scheme
from gptc.logging.predefined import default_logger

CORE_DEPENDENCIES = {
    "numpy": "numpy",
    "protobuf": "google.protobuf",
    "grpc": "grpc",
    "grpc reflection": "grpc_reflection",
    "grpc health check": "grpc_health",
    "yaml": "yaml",
    "packaging": "packaging",
    "docarray": "docarray",
    "hubble": "hubble",
    "cloud": "jcloud",
    "opentelemetry": "opentelemetry",
    "opentelemetry grpc": "opentelemetry.instrumentation.grpc",
    "pydantic": "pydantic",
    "urllib3": "urllib3",
}

OPTIONAL_DEPENDENCIES = {
    "uvloop": "uvloop",
    "prometheus client": "prometheus_client",
    "opentelemetry sdk": "opentelemetry.sdk",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "docker": "docker",
    "pathspec": "pathspec",
    "filelock": "filelock",
    "requests": "requests",
    "websockets": "websockets",
    "multipart": "multipart",
    "aiofiles": "aiofiles",
    "aiohttp": "aiohttp",
    "watchfiles": "watchfiles",
    "pytest": "pytest",
    "black": "black",
    "kubernetes": "kubernetes",
    "tensorflow": "tensorflow",
    "torch": "torch",
}


def check_dependencies(include_all=False):
    """Check which dependencies are importable and print a status table.

    :param include_all: also check the optional dependencies.
    """
    import importlib
    import sys

    from rich import box
    from rich.table import Table

    from gptc.helper import get_rich_console

    dependencies = dict(CORE_DEPENDENCIES)
    if include_all:
        dependencies.update(OPTIONAL_DEPENDENCIES)

    table = Table(title="Gptc dependencies", box=box.ROUNDED)
    table.add_column("Component")
    table.add_column("Module")
    table.add_column("Status")

    failed = []
    for component, module in dependencies.items():
        try:
            importlib.import_module(module)
            status = "[green]OK[/green]"
        except Exception as ex:
            status = f"[red]MISSING[/red] ({type(ex).__name__})"
            failed.append(component)
        table.add_row(component, module, status)

    console = get_rich_console()
    console.print(table)
    if failed:
        console.print(f'[red]Unavailable: {", ".join(failed)}[/red]')
    sys.exit(1 if failed else 0)


class NetworkChecker:
    """Check if a Deployment is running or not."""

    def __init__(self, args: "argparse.Namespace"):
        """
        Create a new :class:`NetworkChecker`.

        :param args: args provided by the CLI.
        """

        import time

        from gptc.clients import Client
        from gptc.logging.profile import TimeContext
        from gptc.serve.runtimes.servers import BaseServer

        try:
            total_time = 0
            total_success = 0
            timeout = args.timeout / 1000 if args.timeout != -1 else None
            for j in range(args.attempts):
                with TimeContext(
                    f"ping {args.target} on {args.host} at {j} round", default_logger
                ) as tc:
                    if args.target == "flow":
                        r = Client(host=args.host).is_flow_ready(timeout=timeout)
                    else:
                        hostname, port, protocol, _ = parse_host_scheme(args.host)
                        r = BaseServer.is_ready(
                            ctrl_address=f"{hostname}:{port}",
                            timeout=timeout,
                            protocol=protocol,
                        )
                    if not r:
                        default_logger.warning(
                            "not responding, attempt (%d/%d) in 1s"
                            % (j + 1, args.attempts)
                        )
                    else:
                        total_success += 1
                total_time += tc.duration
                if args.attempts > 0:
                    time.sleep(1)
            if total_success < args.attempts:
                default_logger.debug(
                    "message lost %.0f%% (%d/%d) "
                    % (
                        (1 - total_success / args.attempts) * 100,
                        args.attempts - total_success,
                        args.attempts,
                    )
                )
            if total_success > 0:
                default_logger.debug(
                    "avg. latency: %.0f ms" % (total_time / total_success * 1000)
                )

            if total_success >= args.min_successful_attempts:
                default_logger.debug(
                    f"readiness check succeeded {total_success} times!!!"
                )
                exit(0)
            else:
                default_logger.debug(
                    f"readiness check succeeded {total_success} times, less than {args.min_successful_attempts}"
                )
        except KeyboardInterrupt:
            pass

        # returns 1 (anomaly) when it comes to here
        exit(1)
