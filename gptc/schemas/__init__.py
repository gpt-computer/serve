def get_full_schema() -> dict:
    """Get full schema
    :return: the full schema for Gptc core as a dict.
    """
    from gptc import __version__
    from gptc.importer import IMPORTED
    from gptc.schemas.deployment import schema_deployment
    from gptc.schemas.executor import schema_all_executors
    from gptc.schemas.flow import schema_flow
    from gptc.schemas.gateway import schema_gateway
    from gptc.schemas.meta import schema_metas

    definitions = {}
    for s in [
        schema_gateway,
        schema_all_executors,
        schema_flow,
        schema_metas,
        schema_deployment,
        IMPORTED.schema_executors,
    ]:
        definitions.update(s)

    return {
        "$id": f"https://schemas.gpt-computer.github.io/schemas/{__version__}.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
        "description": "The YAML schema of Gptc objects (Flow, Executor).",
        "type": "object",
        "oneOf": [{"$ref": "#/definitions/Gptc::Flow"}]
        + [{"$ref": f"#/definitions/{k}"} for k in IMPORTED.schema_executors.keys()],
        "definitions": definitions,
    }
