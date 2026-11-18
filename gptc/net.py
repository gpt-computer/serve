"""Networking helpers: port allocation and host/IP discovery."""

import os
import random
import socket
import urllib.request
from socket import AF_INET, SOCK_STREAM
from typing import List, Optional, Union

assigned_ports: set = set()
unassigned_ports: List[int] = []
DEFAULT_MIN_PORT = 49153
MAX_PORT = 65535


def reset_ports():
    """Reset the pool of available (random) ports."""

    def _get_unassigned_ports():
        # if we are running out of ports, lower default minimum port
        if MAX_PORT - DEFAULT_MIN_PORT - len(assigned_ports) < 100:
            min_port = int(os.environ.get("GPTC_RANDOM_PORT_MIN", "16384"))
        else:
            min_port = int(
                os.environ.get("GPTC_RANDOM_PORT_MIN", str(DEFAULT_MIN_PORT))
            )
        max_port = int(os.environ.get("GPTC_RANDOM_PORT_MAX", str(MAX_PORT)))
        return set(range(min_port, max_port + 1)) - set(assigned_ports)

    unassigned_ports.clear()
    assigned_ports.clear()
    unassigned_ports.extend(_get_unassigned_ports())
    random.shuffle(unassigned_ports)


def random_port() -> Optional[int]:
    """Get a random available port number."""

    def _random_port():
        def _check_bind(port):
            with socket.socket() as s:
                try:
                    s.bind(("", port))
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    return port
                except OSError:
                    return None

        _port = None
        if len(unassigned_ports) == 0:
            reset_ports()
        for idx, _port in enumerate(unassigned_ports):
            if _check_bind(_port) is not None:
                break
        else:
            raise OSError(
                f"can not find an available port in {len(unassigned_ports)} unassigned ports, "
                f"assigned already {len(assigned_ports)} ports"
            )
        int_port = int(_port)
        unassigned_ports.pop(idx)
        assigned_ports.add(int_port)
        return int_port

    try:
        return _random_port()
    except OSError:
        assigned_ports.clear()
        unassigned_ports.clear()
        return _random_port()


def random_ports(n_ports):
    return [random_port() for _ in range(n_ports)]


def get_internal_ip():
    """
    Return the private IP address of the gateway for connecting from other machine in the same network.

    :return: Private IP address.
    """
    ip = "127.0.0.1"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # doesn't even have to be reachable
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
    except Exception:
        pass
    return ip


def get_public_ip(timeout: float = 0.3):
    """
    Return the public IP address of the gateway for connecting from other machine in the public network.

    :param timeout: the seconds to wait until return None.

    :return: Public IP address.

    .. warn::
        Set `timeout` to a large number will block the Flow.

    """

    def _get_ip(url):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as fp:
                _ip = fp.read().decode().strip()
                return _ip

        except:
            pass  # intentionally ignored, public ip is not showed

    ip_server_list = [
        "https://api.ipify.org",
        "https://ident.me",
        "https://checkip.amazonaws.com/",
    ]

    for idx, ip in enumerate(ip_server_list):
        r = _get_ip(ip)
        if r:
            return r


def _single_port_free(host: str, port: int) -> bool:
    with socket.socket(AF_INET, SOCK_STREAM) as session:
        if session.connect_ex((host, port)) == 0:
            return False
        else:
            return True


def is_port_free(host: Union[str, List[str]], port: Union[int, List[int]]) -> bool:
    if isinstance(port, list):
        if isinstance(host, str):
            return all([_single_port_free(host, _p) for _p in port])
        else:
            return all([all([_single_port_free(_h, _p) for _p in port]) for _h in host])
    else:
        if isinstance(host, str):
            return _single_port_free(host, port)
        else:
            return all([_single_port_free(_h, port) for _h in host])
