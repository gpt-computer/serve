from jsonschema import Draft7Validator

from gptc.schemas import get_full_schema


def test_full_schema():
    schema = get_full_schema()
    Draft7Validator.check_schema(schema)
    # assert gptc concepts exist in definitions
    for concept in ["gateway", "flow", "metas", "deployment"]:
        assert f"Gptc::{concept.capitalize()}" in schema["definitions"]
