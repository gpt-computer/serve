import requests

import gptc.helper
from gptc import Flow


def test_extend_fastapi():
    def extend_rest_function(app):
        @app.get("/hello", tags=["My Extended APIs"])
        async def foo():
            return {"msg": "hello world"}

        return app

    gptc.helper.extend_rest_interface = extend_rest_function
    f = Flow(protocol="http")

    with f:
        response = requests.get(f"http://localhost:{f.port}/hello")
        assert response.status_code == 200
        assert response.json() == {"msg": "hello world"}
