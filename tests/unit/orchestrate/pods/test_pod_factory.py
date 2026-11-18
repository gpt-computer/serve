import pytest
from hubble.executor.hubio import HubIO

from gptc.orchestrate.pods.factory import PodFactory
from gptc.parsers import set_pod_parser


@pytest.mark.skip("gptchub not available")
@pytest.mark.parametrize("uses", ["gptcai+docker://gpt-computer/DummyExecutor"])
def test_container_pod(mocker, monkeypatch, uses):
    mock = mocker.Mock()

    def _mock_pull(self):
        return "docker://gptchub/dummy_executor"

    monkeypatch.setattr(HubIO, "pull", _mock_pull)

    args = set_pod_parser().parse_args(["--uses", uses])
    pod = PodFactory.build_pod(args)
    assert pod.args.uses == "docker://gptchub/dummy_executor"
    assert pod.name == "ContainerPod"
