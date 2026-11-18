import pytest

from gptc.logging.logger import GptcLogger
from gptc.serve.networking import _NetworkingMetrics


@pytest.fixture()
def logger():
    return GptcLogger("test networking")


@pytest.fixture()
def metrics():
    sending_requests_time_metrics = None
    received_response_bytes = None
    send_requests_bytes_metrics = None

    return _NetworkingMetrics(
        sending_requests_time_metrics,
        received_response_bytes,
        send_requests_bytes_metrics,
    )
