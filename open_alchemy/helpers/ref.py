"""Used to resolve schema references."""

import functools
import json
import os
import re
import typing

from open_alchemy import exceptions
from open_alchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


NameSchema = typing.Tuple[str, types.Schema]


def resolve(*, name: str, schema: types.Schema, schemas: types.Schemas) -> NameSchema:
    """
    Resolve reference to another schema.

    Recursively resolves $ref until $ref key is no longer found. On each step, the name
    of the schema is recorded.

    Raises SchemaNotFound is a $ref resolution fails.

    Args:
        name: The name of the schema from the last step.
        schema: The specification of the schema from the last step.
        schemas: Dictionary with all defined schemas used to resolve $ref.

    Returns:
        The first schema that no longer has the $ref key and the name of that schema.

    """
    # Checking whether schema is a reference schema
    ref = schema.get("$ref")
    if ref is None:
        return name, schema

    ref_name, ref_schema = get_ref(ref=ref, schemas=schemas)

    return resolve(name=ref_name, schema=ref_schema, schemas=schemas)


def get_ref(*, ref: str, schemas: types.Schemas) -> NameSchema:
    """
    Get the schema referenced by ref.

    Raises SchemaNotFound is a $ref resolution fails.

    Args:
        ref: The reference to the schema.
        schemas: The schemas to use to resolve the ref.

    Returns:
        The schema referenced by ref.

    """
    # Checking value of $ref
    match = _REF_PATTER.match(ref)
    if not match:
        raise exceptions.SchemaNotFoundError(
            f"{ref} format incorrect, expected #/components/schemas/<SchemaName>"
        )

    # Retrieving new schema
    ref_name = match.group(1)
    ref_schema = schemas.get(ref_name)
    if ref_schema is None:
        raise exceptions.SchemaNotFoundError(f"{ref_name} was not found in schemas.")

    return ref_name, ref_schema


def _norm_context(*, context: str) -> str:
    """
    Normalize the path and case of a context.

    Args:
        context: The context to normalize.

    Returns:
        The normalized context.

    """
    norm_context = os.path.normpath(context)
    return os.path.normcase(norm_context)


def _add_remote_context(*, context: str, ref: str) -> str:
    """
    Add remote context to any $ref within a schema retrieved from a remote reference.

    There are 3 cases:
    1. The $ref value starts with # in which case the context is prepended.
    2. The $ref starts with a filename in which case only the file portion of the
        context is prepended.
    3. The $ref starts with a relative path and ends with a file in which case the file
        portion of the context is prepended and merged so that the shortest possible
        relative path is used.

    After the paths are merged the following operations are done:
    1. a normalized relative path is calculated (eg. turning ./dir1/../dir2 to ./dir2)
        and
    2. the case is normalized.

    Args:
        context: The context of the document from which the schema was retrieved which
            is the relative path to the file on the system from the base OpenAPI
            specification.
        ref: The value of a $ref within the schema.

    Returns:
        The $ref value with the context of the document included.

    """
    # Check reference value
    try:
        ref_context, ref_schema = ref.split("#")
    except ValueError:
        raise exceptions.MalformedSchemaError(
            f"A reference must contain exactly one #. Actual reference: {ref}"
        )
    context_head, _ = os.path.split(context)

    # Handle reference within document
    if not ref_context:
        return f"{context}{ref}"

    # Handle reference outside document
    new_ref_context = os.path.join(context_head, ref_context)
    norm_new_ref_context = _norm_context(context=new_ref_context)
    return f"{norm_new_ref_context}#{ref_schema}"


def _handle_match(match: typing.Match, *, context: str) -> str:
    """
    Map a match to the updated value.

    Args:
        match: The match to the regular expression for the reference.
        context: The context to use to update the reference.

    Returns:
        The updated reference.

    """
    ref = match.group(1)
    mapped_ref = _add_remote_context(context=context, ref=ref)
    return match.group(0).replace(ref, mapped_ref)


_REF_VALUE_PATTERN = r'"\$ref": "(.*?)"'


def _map_remote_schema_ref(*, schema: types.Schema, context: str) -> types.Schema:
    """
    Update and $ref within the schema with the remote context.

    Serialize the schema, look for $ref and update value to include context.

    Args:
        schema: The schema to update.
        context: The con text of the schema.

    Returns:
        The schema with any $ref mapped to include the context.

    """
    # Define context for mapping
    handle_match_context = functools.partial(_handle_match, context=context)

    str_schema = json.dumps(schema)
    mapped_str_schema = re.sub(_REF_VALUE_PATTERN, handle_match_context, str_schema)
    mapped_schema = json.loads(mapped_str_schema)
    return mapped_schema


class _RemoteSchemaStore:
    """Store remote schemas in memory to speed up use."""

    _schemas: typing.Dict[str, types.Schemas]
    spec_path: typing.Optional[str]

    def __init__(self) -> None:
        """Construct."""
        self._schemas = {}
        self.spec_path = None

    def reset(self):
        """Reset the state of the schema store."""
        self._schemas = {}
        self.spec_path = None
