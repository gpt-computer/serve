from gptc.serve.runtimes.gateway.gateway import BaseGateway
from gptc.serve.runtimes.servers.load_balancer import LoadBalancingServer

__all__ = ["LoadBalancerGateway"]


class LoadBalancerGateway(LoadBalancingServer, BaseGateway):
    """
    :class:`LoadBalancerGateway`
    """

    pass
