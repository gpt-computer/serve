import traceback
from typing import Optional

from gptc.proto import gptc_pb2
from gptc.serve.executors import BaseExecutor
from gptc.types.mixin import ProtoTypeMixin


class Request(ProtoTypeMixin):
    """
    :class:`Request` is one of the primitive data types in Gptc, and serves as a base for
    :class:`~data.DataRequest` and :class:`~data.Response`.

    It offers a Pythonic interface to allow users access and manipulate
    :class:`gptc.gptc_pb2.RequestProto` object without working with Protobuf itself.

    It serves as a container for serialized :class:`gptc_pb2.RequestProto` that only triggers deserialization
    and decompression when receives the first read access to its member.

    It overrides :meth:`__getattr__` to provide the same get/set interface as an
    :class:`gptc_pb2.RequestProto` object.

    """

    def __getattr__(self, name: str):
        return getattr(self.proto, name)

    def add_exception(
        self, ex: Optional["Exception"] = None, executor: "BaseExecutor" = None
    ) -> None:
        """Add exception to the last route in the envelope
        :param ex: Exception to be added
        :param executor: Executor related to the exception
        """
        d = self.header.status
        d.code = gptc_pb2.StatusProto.ERROR
        d.description = repr(ex)

        if ex is None:
            return

        if executor:
            d.exception.executor = executor.__class__.__name__
        d.exception.name = ex.__class__.__name__
        d.exception.args.extend([str(v) for v in ex.args])
        d.exception.stacks.extend(
            traceback.format_exception(type(ex), value=ex, tb=ex.__traceback__)
        )
