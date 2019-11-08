"""Create table args such as UniqueConstraints and Index."""

import functools
import json
import os
import typing

import jsonschema

from open_alchemy import exceptions
from open_alchemy import types

_DIRECTORY = os.path.dirname(__file__)
_PATHS = ("..", "helpers", "get_ext_prop")
_COMMON_SCHEMAS_FILE = os.path.join(_DIRECTORY, *_PATHS, "common-schemas.json")
with open(_COMMON_SCHEMAS_FILE) as in_file:
    _COMMON_SCHEMAS = json.load(in_file)
_resolver = jsonschema.RefResolver.from_schema(  # pylint: disable=invalid-name
    _COMMON_SCHEMAS
)


def _spec_to_schema_name(
    *,
    spec: types.AnyUniqueConstraint,
    schema_names: typing.Optional[typing.List[str]] = None,
) -> str:
    """
    Convert a specification to the name of the matched schema.

    Use the schema names defined in common-schemas.json to find the first matching
    schema.

    Args:
        spec: The specification to convert.
        schema_names: The names of the schemas to check.

    Returns:
        The name of the specification.

    """
    if schema_names is None:
        schema_names = _COMMON_SCHEMAS.keys()

    for name in schema_names:
        try:
            jsonschema.validate(
                instance=spec, schema=_COMMON_SCHEMAS[name], resolver=_resolver
            )
            return name
        except jsonschema.ValidationError:
            continue
    raise exceptions.SchemaNotFoundError("Specification did not match any schemas.")


def _handle_column_list(
    spec: typing.List[str], property_name: str
) -> types.UniqueConstraint:
    """
    Convert ColumnList specification to UniqueConstraint.

    Args:
        spec: The specification to convert.
        property_name: The property name under which to store the column list.

    Returns:
        The UniqueConstraint.

    """
    return {property_name: spec}


# Handling for column lists for unique constraints and index
_uq_handle_column_list = functools.partial(  # pylint: disable=invalid-name
    _handle_column_list, property_name="columns"
)
_ix_handle_column_list = functools.partial(  # pylint: disable=invalid-name
    _handle_column_list, property_name="expressions"
)

# Schema names for unique constraints and index
_SCHEMAS_FILE = os.path.join(_DIRECTORY, *_PATHS, "extension-schemas.json")
with open(_SCHEMAS_FILE) as in_file:
    _SCHEMAS = json.load(in_file)
_UNIQUE_SCHEMA_NAMES: typing.List[str] = list(
    map(
        lambda schema: schema["$ref"].split("/")[-1],
        _SCHEMAS["x-unique-constraint"]["oneOf"],
    )
)
_INDEX_SCHEMA_NAMES: typing.List[str] = list(
    map(
        lambda schema: schema["$ref"].split("/")[-1],
        _SCHEMAS["x-composite-index"]["oneOf"],
    )
)

# Unique and index name to conversion function
_UNIQUE_MAPPING: typing.Dict[str, typing.Callable[..., types.UniqueConstraintList]] = {
    "ColumnList": lambda spec: [_uq_handle_column_list(spec=spec)],
    "ColumnListList": lambda spec: list(map(_uq_handle_column_list, spec)),
    "UniqueConstraint": lambda spec: [spec],
    "UniqueConstraintList": lambda spec: spec,
}
_INDEX_MAPPING: typing.Dict[str, typing.Callable[..., types.IndexList]] = {
    "ColumnList": lambda spec: [_ix_handle_column_list(spec=spec)],
    "ColumnListList": lambda spec: list(map(_ix_handle_column_list, spec)),
    "Index": lambda spec: [spec],
    "IndexList": lambda spec: spec,
}


def _handle_unique(*, spec: types.AnyUniqueConstraint) -> types.UniqueConstraintList:
    """
    Convert any unique constraint to UniqueConstraintList.

    Args:
        spec: The specification to convert.

    Returns:
        The UniqueConstraintList.

    """
    name = _spec_to_schema_name(spec=spec, schema_names=_UNIQUE_SCHEMA_NAMES)
    return _UNIQUE_MAPPING[name](spec)


def _handle_index(*, spec: types.AnyIndex) -> types.IndexList:
    """
    Convert any composite index to IndexList.

    Args:
        spec: The specification to convert.

    Returns:
        The IndexList.

    """
    name = _spec_to_schema_name(spec=spec, schema_names=_INDEX_SCHEMA_NAMES)
    return _INDEX_MAPPING[name](spec)
