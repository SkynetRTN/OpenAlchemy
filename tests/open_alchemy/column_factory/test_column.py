"""Tests for the column factory."""
# pylint: disable=protected-access

import copy

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import facades
from open_alchemy import types
from open_alchemy.column_factory import column


@pytest.mark.parametrize(
    "schema, expected_exception",
    [
        ({}, exceptions.TypeMissingError),
        ({"type": 1}, exceptions.TypeMissingError),
        ({"type": "type 1", "format": 1}, exceptions.MalformedSchemaError),
        ({"type": "type 1", "maxLength": "1"}, exceptions.MalformedSchemaError),
        ({"type": "type 1", "nullable": "True"}, exceptions.MalformedSchemaError),
        (
            {"type": "type 1", "x-primary-key": "True"},
            exceptions.MalformedExtensionPropertyError,
        ),
        (
            {"type": "type 1", "x-autoincrement": "True"},
            exceptions.MalformedExtensionPropertyError,
        ),
        (
            {"type": "type 1", "x-index": "True"},
            exceptions.MalformedExtensionPropertyError,
        ),
        (
            {"type": "type 1", "x-unique": "True"},
            exceptions.MalformedExtensionPropertyError,
        ),
        (
            {"type": "type 1", "x-foreign-key": True},
            exceptions.MalformedExtensionPropertyError,
        ),
    ],
    ids=[
        "type missing",
        "type not string",
        "format not string",
        "maxLength not integer",
        "nullable not boolean",
        "primary key not boolean",
        "autoincrement not boolean",
        "index not boolean",
        "unique not boolean",
        "foreign key not string",
    ],
)
@pytest.mark.column
def test_check_schema_invalid(schema, expected_exception):
    """
    GIVEN invalid schema
    WHEN check_schema is called with the schema
    THEN given exception is raised.
    """
    with pytest.raises(expected_exception):
        column.check_schema(schema=schema)


@pytest.mark.parametrize(
    "artifacts, nullable, dict_ignore, expected_schema",
    [
        (types.ColumnArtifacts(type="type 1"), None, None, {"type": "type 1"}),
        (
            types.ColumnArtifacts(type="type 1", format="format 1"),
            None,
            None,
            {"type": "type 1", "format": "format 1"},
        ),
        (
            types.ColumnArtifacts(type="type 1", max_length=1),
            None,
            None,
            {"type": "type 1", "maxLength": 1},
        ),
        (
            types.ColumnArtifacts(type="type 1", nullable=False),
            None,
            None,
            {"type": "type 1"},
        ),
        (
            types.ColumnArtifacts(type="type 1", autoincrement=True),
            None,
            None,
            {"type": "type 1", "x-generated": True},
        ),
        (
            types.ColumnArtifacts(type="type 1"),
            False,
            None,
            {"type": "type 1", "nullable": False},
        ),
        (
            types.ColumnArtifacts(type="type 1"),
            None,
            True,
            {"type": "type 1", "x-dict-ignore": True},
        ),
    ],
    ids=[
        "type only",
        "type with format",
        "type with maxLength",
        "type with nullable",
        "type with autoincrement",
        "nullable input not None",
        "dict_ignore input not None",
    ],
)
@pytest.mark.column
def test_calculate_schema(artifacts, expected_schema, nullable, dict_ignore):
    """
    GIVEN schema
    WHEN check_schema is called with the schema
    THEN the schema is returned.
    """
    returned_schema = column.calculate_schema(
        artifacts=artifacts, nullable=nullable, dict_ignore=dict_ignore
    )

    assert returned_schema == expected_schema


@pytest.mark.parametrize(
    "artifacts, expected_schema",
    [
        (types.ColumnArtifacts(type="type 1"), {"type": "type 1"}),
        (types.ColumnArtifacts(type="type 1"), {"type": "type 1", "nullable": True}),
        (
            types.ColumnArtifacts(type="type 1"),
            {"type": "type 1", "x-dict-ignore": True},
        ),
    ],
    ids=["type only", "type with nullable", "type with x-dict-ignore"],
)
@pytest.mark.column
def test_calculate_column_schema(artifacts, expected_schema):
    """
    GIVEN schema
    WHEN _calculate_column_schema is called with the schema
    THEN the schema is returned.
    """
    returned_schema = column._calculate_column_schema(
        artifacts=artifacts, schema=copy.deepcopy(expected_schema)
    )

    assert returned_schema == expected_schema


@pytest.mark.column
def test_calculate_column_schema_dict_ignore_invalid():
    """
    GIVEN schema with invalid x-dict-ignore
    WHEN _calculate_column_schema is called with the schema
    THEN MalformedExtensionPropertyError is raised.
    """
    with pytest.raises(exceptions.MalformedExtensionPropertyError):
        column._calculate_column_schema(
            artifacts=types.ColumnArtifacts("type 1"),
            schema={"type": "type 1", "x-dict-ignore": "True"},
        )


@pytest.mark.parametrize(
    "schema, expected_artifacts",
    [
        ({"type": "type 1"}, types.ColumnArtifacts("type 1")),
        (
            {"type": "type 1", "format": "format 1"},
            types.ColumnArtifacts("type 1", format="format 1"),
        ),
        (
            {"type": "type 1", "maxLength": 1},
            types.ColumnArtifacts("type 1", max_length=1),
        ),
        (
            {"type": "type 1", "nullable": True},
            types.ColumnArtifacts("type 1", nullable=True),
        ),
        (
            {"type": "type 1", "x-primary-key": True},
            types.ColumnArtifacts("type 1", primary_key=True),
        ),
        (
            {"type": "type 1", "x-autoincrement": True},
            types.ColumnArtifacts("type 1", autoincrement=True, nullable=False),
        ),
        (
            {"type": "type 1", "x-index": True},
            types.ColumnArtifacts("type 1", index=True),
        ),
        (
            {"type": "type 1", "x-unique": True},
            types.ColumnArtifacts("type 1", unique=True),
        ),
        (
            {"type": "type 1", "x-foreign-key": "table.column"},
            types.ColumnArtifacts("type 1", foreign_key="table.column"),
        ),
    ],
    ids=[
        "type only",
        "type with format",
        "type with maxLength",
        "type with nullable",
        "type with primary key",
        "type with autoincrement",
        "type with index",
        "type with unique",
        "type with foreign key",
    ],
)
@pytest.mark.column
def test_check_schema_artifacts(schema, expected_artifacts):
    """
    GIVEN schema and expected artifacts
    WHEN check_schema is called with the schema
    THEN the expected artifacts are returned.
    """
    artifacts = column.check_schema(schema=schema)

    assert artifacts == expected_artifacts


@pytest.mark.column
def test_check_schema_required():
    """
    GIVEN schema
    WHEN check_schema is called with the schema and required True
    THEN nullable is False.
    """
    schema = {"type": "type 1"}

    artifacts = column.check_schema(schema=copy.deepcopy(schema), required=True)

    assert artifacts.nullable is False


@pytest.mark.column
def test_integration():
    """
    GIVEN schema and logical name
    WHEN handle_column is called with the schema
    THEN the logical name and an instance of SQLAlchemy Column is returned.
    """
    returned_schema, returned_column = column.handle_column(
        schema={"$ref": "#/components/schemas/Column"},
        schemas={"Column": {"type": "number"}},
    )

    assert isinstance(returned_column, sqlalchemy.Column)
    assert isinstance(returned_column.type, sqlalchemy.Float)
    assert returned_schema == {"type": "number"}


class TestCheckArtifacts:
    """Tests for _check_artifacts."""

    # pylint: disable=protected-access

    @staticmethod
    @pytest.mark.parametrize(
        "type_, format_, max_length, autoincrement",
        [
            ("integer", None, 1, None),
            ("number", None, 1, None),
            ("boolean", None, 1, None),
            ("string", "date", 1, None),
            ("string", "date-time", 1, None),
            ("number", None, None, True),
            ("string", None, None, True),
            ("boolean", None, None, True),
            ("boolean", "format1", None, None),
        ],
        ids=[
            "maxLength     integer",
            "maxLength     number",
            "maxLength     boolean",
            "maxLength     string  date",
            "maxLength     string  date-time",
            "autoincrement number",
            "autoincrement string",
            "autoincrement boolean",
            "format        boolean",
        ],
    )
    @pytest.mark.column
    def test_invalid(type_, format_, max_length, autoincrement):
        """
        GIVEN type, format, maxLength and autoincrement
        WHEN _check_artifacts is called with the artifacts
        THEN MalformedSchemaError is raised.
        """
        artifacts = types.ColumnArtifacts(
            type=type_,
            format=format_,
            max_length=max_length,
            autoincrement=autoincrement,
        )

        with pytest.raises(exceptions.MalformedSchemaError):
            column._check_artifacts(artifacts=artifacts)

    @staticmethod
    @pytest.mark.parametrize(
        "type_, format_, max_length, autoincrement",
        [
            ("string", None, 1, None),
            ("string", "byte", 1, None),
            ("string", "password", 1, None),
            ("string", "binary", 1, None),
            ("integer", None, None, True),
            ("integer", "int32", None, None),
            ("number", "float", None, None),
            ("string", "password", None, None),
        ],
        ids=[
            "maxLength     string",
            "maxLength     string  byte",
            "maxLength     string  password",
            "maxLength     string  binary",
            "autoincrement integer",
            "format        integer",
            "format        number",
            "format        string",
        ],
    )
    @pytest.mark.column
    def test_valid(type_, format_, max_length, autoincrement):
        """
        GIVEN valid artifacts
        WHEN _check_artifacts is called
        THEN MalformedSchemaError is not raised.
        """
        artifacts = types.ColumnArtifacts(
            type=type_,
            format=format_,
            max_length=max_length,
            autoincrement=autoincrement,
        )

        column._check_artifacts(artifacts=artifacts)


@pytest.mark.column
def test_construct_column_invalid():
    """
    GIVEN artifacts that are not valid
    WHEN construct_column is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = types.ColumnArtifacts(type="string", autoincrement=True)

    with pytest.raises(exceptions.MalformedSchemaError):
        column.construct_column(artifacts=artifacts)


@pytest.mark.column
def test_construct_column_valid():
    """
    GIVEN artifacts that are not valid
    WHEN construct_column is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = types.ColumnArtifacts(type="string")

    return_column = column.construct_column(artifacts=artifacts)

    assert isinstance(return_column, facades.sqlalchemy.Column)
    assert isinstance(return_column.type, facades.sqlalchemy.column.String)
