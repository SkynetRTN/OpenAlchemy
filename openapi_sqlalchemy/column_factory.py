"""Generate columns based on openapi schema property."""

import re
import typing

import sqlalchemy

from openapi_sqlalchemy import exceptions
from openapi_sqlalchemy import types

_REF_PATTER = re.compile(r"^#\/components\/schemas\/(\w+)$")


def resolve_ref(func: typing.Callable) -> typing.Callable:
    """Resolve $ref schemas."""

    def inner(
        *,
        schema: types.Schema,
        schemas: typing.Optional[typing.Dict[str, types.Schema]] = None,
        **kwargs,
    ) -> sqlalchemy.Column:
        """Replace function."""
        # Checking for $ref
        ref = schema.get("$ref")
        if ref is None:
            return func(schema=schema, **kwargs)

        # Checking for schemas
        if schemas is None:
            raise exceptions.MissingArgumentError(
                "schemas is required for $ref schemas."
            )

        # Checking value of $ref
        match = _REF_PATTER.match(ref)
        if not match:
            raise exceptions.SchemaNotFoundError(
                f"{ref} format incorrect, expected #/components/schemas/<SchemaName>"
            )

        # Retrieving new schema
        schema_name = match.group(1)
        ref_schema = schemas.get(schema_name)
        if ref_schema is None:
            raise exceptions.SchemaNotFoundError(
                f"{schema_name} was not found in schemas."
            )

        # Recursively resolving any more $ref
        return inner(schema=ref_schema, schemas=schemas, **kwargs)

    return inner


@resolve_ref
def column_factory(
    *, schema: types.Schema, required: typing.Optional[bool] = None
) -> sqlalchemy.Column:
    """
    Generate column based on openapi schema property.

    Args:
        schema: The schema for the column.
        required: Whether the object property is required.

    Returns:
        The SQLAlchemy column based on the schema.

    """
    if "type" not in schema:
        raise exceptions.TypeMissingError("Every property requires a type.")

    # Keep track of column arguments
    type_: typing.Optional[sqlalchemy.sql.type_api.TypeEngine] = None
    args: typing.Tuple[typing.Any, ...] = ()
    kwargs: typing.Dict[str, typing.Any] = {}

    # Calculate column modifiers
    kwargs["nullable"] = _calculate_nullable(schema=schema, required=required)
    if schema.get("x-primary-key"):
        kwargs["primary_key"] = True
    if schema.get("x-index"):
        kwargs["index"] = True
    if schema.get("x-unique"):
        kwargs["unique"] = True

    # Calculating type of column
    if schema.get("type") == "integer":
        type_ = _handle_integer(schema=schema)
    elif schema.get("type") == "number":
        type_ = _handle_number(schema=schema)
    elif schema.get("type") == "string":
        type_ = _handle_string(schema=schema)
    elif schema.get("type") == "boolean":
        type_ = sqlalchemy.Boolean

    if type_ is None:
        raise exceptions.FeatureNotImplementedError(
            f"{schema['type']} has not been implemented"
        )

    return sqlalchemy.Column(type_, *args, **kwargs)


def _handle_object(*, schema: types.Schema):
    """
    Determine the relationship and foreign key combination for an object reference.

    Args:
        schema: The schema of the object reference.

    """
    tablename = schema.get("x-tablename")
    if not tablename:
        raise exceptions.MalformedObjectSchemaError(
            "Referenced object is missing x-tablename property."
        )
    properties = schema.get("properties")
    if properties is None:
        raise exceptions.MalformedObjectSchemaError(
            "Referenced object does not have any properties."
        )
    if "id" not in properties:
        raise exceptions.MalformedObjectSchemaError(
            "Referenced object does not have id property."
        )


def _calculate_nullable(
    *, schema: types.Schema, required: typing.Optional[bool]
) -> bool:
    """
    Calculate the value of the nullable field.

    The following is the truth table for the nullable property.
    required  | schema nullable | returned nullable
    --------------------------------------------------------
    None      | not given       | True
    None      | False           | False
    None      | True            | True
    False     | not given       | True
    False     | False           | False
    False     | True            | True
    True      | not given       | False
    True      | False           | False
    True      | True            | True

    To summarize, if nullable is the schema the value for it is used. Otherwise True
    is returned unless required is True.

    Args:
        schema: The schema for the column.
        required: Whether the property is required.

    Returns:
        The nullable value for the column.

    """
    nullable = schema.get("nullable")
    if nullable is None:
        if required:
            return False
        return True
    if nullable:
        return True
    return False


def _handle_integer(
    *, schema: types.Schema
) -> typing.Union[sqlalchemy.Integer, sqlalchemy.BigInteger]:
    """
    Determine the type of integer to use for the schema.

    Args:
        schema: The schema for the integer column.

    Returns:
        Integer or BigInteger depending on the format.

    """
    if schema.get("format", "int32") == "int32":
        return sqlalchemy.Integer
    if schema.get("format") == "int64":
        return sqlalchemy.BigInteger
    raise exceptions.FeatureNotImplementedError(
        f"{schema.get('format')} format for integer is not supported."
    )


def _handle_number(*, schema: types.Schema) -> sqlalchemy.Float:
    """
    Determine the type of number to use for the schema.

    Args:
        schema: The schema for the number column.

    Returns:
        Float.

    """
    if schema.get("format", "float") == "float":
        return sqlalchemy.Float
    raise exceptions.FeatureNotImplementedError(
        f"{schema.get('format')} format for number is not supported."
    )


def _handle_string(*, schema: types.Schema) -> sqlalchemy.String:
    """
    Determine the setup of the string to use for the schema.

    Args:
        schema: The schema for the string column.

    Returns:
        String.

    """
    return sqlalchemy.String(length=schema.get("maxLength"))
