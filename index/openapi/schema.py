from copy import deepcopy
from typing import Any, List, Dict, Callable, Optional, Iterable, Mapping

from .models import Model


def replace_definitions(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    replace $ref
    """
    schema = deepcopy(schema)

    if schema.get("definitions") is not None:

        def replace(mapping: Dict[str, Any]) -> None:
            for _name in mapping.keys():
                if _name == "$ref":
                    define_schema = schema
                    for key in mapping["$ref"][2:].split("/"):
                        define_schema = define_schema[key]
                    break
                elif isinstance(mapping[_name], Mapping):
                    replace(mapping[_name])
                elif isinstance(mapping[_name], Iterable) and not isinstance(
                    mapping[_name], str
                ):
                    for value in mapping[_name]:
                        replace(value)
            else:
                return
            # replace ref and del it
            mapping.update(define_schema)
            del mapping["$ref"]

        replace(schema["properties"])
        del schema["definitions"]

    return schema


def schema_parameter(m: Optional[Model], position: str) -> List[Dict[str, Any]]:
    """
    position: "path", "query", "header", "cookie"
    """
    result = []

    if m is not None:
        _schemas = replace_definitions(m.schema())
        properties: Dict[str, Any] = _schemas["properties"]
        _schemas["required"] = _schemas.get("required") or []

        for name, schema in properties.items():
            result.append(
                {
                    "in": position,
                    "name": name,
                    "description": schema.pop("description"),
                    "required": name in _schemas.get("required"),  # type: ignore
                    "schema": schema,
                }
            )
    return result


def schema_parameters(
    path: Model = None, query: Model = None, header: Model = None, cookie: Model = None,
) -> List[Dict[str, Any]]:

    return (
        schema_parameter(path, "path")
        + schema_parameter(query, "query")
        + schema_parameter(header, "header")
        + schema_parameter(cookie, "cookie")
    )


def schema_request_body(body: Model = None) -> Optional[Dict[str, Any]]:
    if body is None:
        return None

    return {
        "required": True,
        "content": {"application/json": {"schema": replace_definitions(body.schema())}},
    }


def schema_response(model: Model) -> Dict[str, Any]:
    return {"application/json": {"schema": replace_definitions(model.schema())}}
