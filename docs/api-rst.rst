======================
:fab:`python` Python API
======================

This section includes the API documentation from the `gptc` codebase, as extracted from the `docstrings <https://peps.python.org/pep-0257/>`_ in the code.

For further details, please refer to the full :ref:`user guide <executor-cookbook>`.


:mod:`gptc.orchestrate.deployments` - Deployment
--------------------

.. currentmodule:: gptc.orchestrate.deployments

.. autosummary::
   :nosignatures:
   :template: class.rst

   __init__.Deployment


:mod:`gptc.orchestrate.flow` - Flow
--------------------

.. currentmodule:: gptc.orchestrate.flow

.. autosummary::
   :nosignatures:
   :template: class.rst

   base.Flow
   asyncio.AsyncFlow


:mod:`gptc.serve.executors` - Executor
--------------------

.. currentmodule:: gptc.serve.executors

.. autosummary::
   :nosignatures:
   :template: class.rst

   Executor
   BaseExecutor
   decorators.requests
   decorators.monitor


:mod:`gptc.clients` - Clients
--------------------

.. currentmodule:: gptc.clients

.. autosummary::
   :nosignatures:
   :template: class.rst

   Client
   grpc.GRPCClient
   grpc.AsyncGRPCClient
   http.HTTPClient
   http.AsyncHTTPClient
   websocket.WebSocketClient
   websocket.AsyncWebSocketClient


:mod:`gptc.types.request` - Networking messages
--------------------

.. currentmodule:: gptc.types.request

.. autosummary::
   :nosignatures:
   :template: class.rst

   Request
   data.DataRequest
   data.Response
   status.StatusMessage



:mod:`gptc.serve.runtimes` - Flow internals
--------------------

.. currentmodule:: gptc.serve.runtimes

.. autosummary::
   :nosignatures:
   :template: class.rst

   asyncio.AsyncNewLoopRuntime
   gateway.GatewayRuntime
   gateway.grpc.GRPCGatewayRuntime
   gateway.http.HTTPGatewayRuntime
   gateway.websocket.WebSocketGatewayRuntime
   worker.WorkerRuntime
   head.HeadRuntime
