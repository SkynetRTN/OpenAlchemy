"""SQLAlchemy column generation."""

import typing

import sqlalchemy

from ... import exceptions
from ... import types

# Remapping SQLAlchemy classes
Column: sqlalchemy.Column = sqlalchemy.Column
Type: sqlalchemy.sql.type_api.TypeEngine = sqlalchemy.sql.type_api.TypeEngine
ForeignKey: sqlalchemy.ForeignKey = sqlalchemy.ForeignKey
Integer: sqlalchemy.Integer = sqlalchemy.Integer
BigInteger: sqlalchemy.BigInteger = sqlalchemy.BigInteger
Number: sqlalchemy.Float = sqlalchemy.Float
String: sqlalchemy.String = sqlalchemy.String
Binary: sqlalchemy.LargeBinary = sqlalchemy.LargeBinary
Date: sqlalchemy.Date = sqlalchemy.Date
DateTime: sqlalchemy.DateTime = sqlalchemy.DateTime
Boolean: sqlalchemy.Boolean = sqlalchemy.Boolean


def construct(*, artifacts: types.ColumnArtifacts) -> Column:
    """
    Construct column from artifacts.

    Args:
        artifacts: The artifacts of the column.

    Returns:
        The SQLAlchemy column.

    """
    type_ = _determine_type(artifacts=artifacts)
    foreign_key: typing.Optional[ForeignKey] = None
    if artifacts.foreign_key is not None:
        foreign_key = ForeignKey(artifacts.foreign_key)
    return Column(
        type_,
        foreign_key,
        nullable=artifacts.nullable,
        primary_key=artifacts.primary_key,
        autoincrement=artifacts.autoincrement,
        index=artifacts.index,
        unique=artifacts.unique,
    )


def _determine_type(*, artifacts: types.ColumnArtifacts) -> Type:
    """
    Determine the type for a specification.

    Raise FeatureNotImplementedError for unsupported types.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The type for the column.

    """
    # Determining the type
    type_: typing.Optional[Type] = None
    if artifacts.type == "integer":
        type_ = _handle_integer(artifacts=artifacts)
    elif artifacts.type == "number":
        type_ = _handle_number(artifacts=artifacts)
    elif artifacts.type == "string":
        type_ = _handle_string(artifacts=artifacts)
    elif artifacts.type == "boolean":
        type_ = _handle_boolean(artifacts=artifacts)

    if type_ is None:
        raise exceptions.FeatureNotImplementedError(
            f"{artifacts.type} has not been implemented"
        )

    return type_


def _handle_integer(
    *, artifacts: types.ColumnArtifacts
) -> typing.Union[Integer, BigInteger]:
    """
    Handle artifacts for an integer type.

    Raises MalformedSchemaError if max length is defined.
    Raise FeatureNotImplementedError is a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy integer type of the column.

    """
    if artifacts.max_length is not None:
        raise exceptions.MalformedSchemaError(
            "The integer type does not support a maximum length."
        )
    if artifacts.format is None or artifacts.format == "int32":
        return Integer
    if artifacts.format == "int64":
        return BigInteger
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for integer is not supported."
    )


def _handle_number(*, artifacts: types.ColumnArtifacts) -> Number:
    """
    Handle artifacts for an number type.

    Raises MalformedSchemaError if max length or autoincrement is defined.
    Raise FeatureNotImplementedError is a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy number type of the column.

    """
    if artifacts.max_length is not None:
        raise exceptions.MalformedSchemaError(
            "The number type does not support a maximum length."
        )
    if artifacts.autoincrement is not None:
        raise exceptions.MalformedSchemaError(
            "The number type does not support autoincrement."
        )
    if artifacts.format is None or artifacts.format == "float":
        return Number
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for number is not supported."
    )


def _handle_string(
    *, artifacts: types.ColumnArtifacts
) -> typing.Union[String, Binary, Date, DateTime]:
    """
    Handle artifacts for an string type.

    Raises MalformedSchemaError if autoincrement is defined.
    Raise FeatureNotImplementedError is a format that is not supported is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy string type of the column.

    """
    if artifacts.autoincrement is not None:
        raise exceptions.MalformedSchemaError(
            "The string type does not support autoincrement."
        )
    if artifacts.format in {None, "byte", "password"}:
        if artifacts.max_length is None:
            return String
        return String(length=artifacts.max_length)
    if artifacts.format == "binary":
        if artifacts.max_length is None:
            return Binary
        return Binary(length=artifacts.max_length)
    if artifacts.format == "date":
        return Date
    if artifacts.format == "date-time":
        return DateTime
    raise exceptions.FeatureNotImplementedError(
        f"{artifacts.format} format for string is not supported."
    )


def _handle_boolean(*, artifacts: types.ColumnArtifacts) -> Boolean:
    """
    Handle artifacts for an boolean type.

    Raises MalformedSchemaError if format, autoincrement or max length is defined.

    Args:
        artifacts: The artifacts for the column.

    Returns:
        The SQLAlchemy boolean type of the column.

    """
    if artifacts.format is not None:
        raise exceptions.MalformedSchemaError(
            "The boolean type does not support format."
        )
    if artifacts.autoincrement is not None:
        raise exceptions.MalformedSchemaError(
            "The boolean type does not support autoincrement."
        )
    if artifacts.max_length is not None:
        raise exceptions.MalformedSchemaError(
            "The boolean type does not support a maximum length."
        )
    return Boolean
