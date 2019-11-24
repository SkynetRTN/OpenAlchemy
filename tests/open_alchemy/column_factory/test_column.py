"""Tests for the column factory."""
# pylint: disable=protected-access

import copy

import pytest
import sqlalchemy

from open_alchemy import exceptions
from open_alchemy import types
from open_alchemy.column_factory import column


@pytest.mark.column
def test_spec_to_column_no_type():
    """
    GIVEN column schema without type
    WHEN _spec_to_column is called with the schema
    THEN TypeMissingError is raised.
    """
    with pytest.raises(exceptions.TypeMissingError):
        column._spec_to_column(spec={})


@pytest.mark.column
def test_spec_to_column_type_unsupported():
    """
    GIVEN column schema with type that has not been implemented
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "unsupported"})


@pytest.mark.column
def test_spec_to_column_column_return():
    """
    GIVEN valid schema
    WHEN _spec_to_column is called with the schema
    THEN an instance of SQLAlchemy Column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "number"})

    assert isinstance(returned_column, sqlalchemy.Column)


@pytest.mark.parametrize("primary_key", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_primary_key(primary_key: bool):
    """
    GIVEN valid schema and the value of the primary key property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column primary_key property is set to the input.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-primary-key": primary_key}
    )

    assert returned_column.primary_key == primary_key


@pytest.mark.parametrize("autoincrement", [True, False], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_autoincrement(autoincrement: bool):
    """
    GIVEN valid schema and the value of the autoincrement property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column autoincrement property is set to the input.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-autoincrement": autoincrement}
    )

    assert returned_column.autoincrement == autoincrement


@pytest.mark.parametrize("index", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_index(index: bool):
    """
    GIVEN valid schema and the value of the index property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column index property is set to the input.
    """
    returned_column = column._spec_to_column(spec={"type": "number", "x-index": index})

    assert returned_column.index == index


@pytest.mark.parametrize("unique", [True, None], ids=["set", "reset"])
@pytest.mark.column
def test_spec_to_column_unique(unique: bool):
    """
    GIVEN valid schema and the value of the unique property
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column unique property is set to the input.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-unique": unique}
    )

    assert returned_column.unique == unique


@pytest.mark.column
def test_spec_to_column_foreign_key():
    """
    GIVEN valid schema which has x-foreign-key set
    WHEN _spec_to_column is called with the schema
    THEN the returned SQLAlchemy column foreign key property is set.
    """
    returned_column = column._spec_to_column(
        spec={"type": "number", "x-foreign-key": "foreign.key"}
    )

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
    assert str(foreign_key) == "ForeignKey('foreign.key')"


@pytest.mark.parametrize(
    "required, nullable, expected_result",
    [
        (None, None, True),
        (None, False, False),
        (None, True, True),
        (False, None, True),
        (False, False, False),
        (False, True, True),
        (True, None, False),
        (True, False, False),
        (True, True, True),
    ],
    ids=[
        "required not given nullable not given",
        "required not given nullable reset",
        "required not given nullable set",
        "required reset nullable not given",
        "required reset nullable reset",
        "required reset nullable set",
        "required set nullable not given",
        "required set nullable reset",
        "required set nullable set",
    ],
)
@pytest.mark.column
def test__calculate_nullable(required, nullable, expected_result):
    """
    GIVEN required, nullable and expected result
    WHEN _calculate_nullable is called with nullable and required
    THEN the expected result is returned.
    """
    result = column._calculate_nullable(nullable=nullable, required=required)

    assert result == expected_result


@pytest.mark.column
def test_spec_to_column_number():
    """
    GIVEN schema with number type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "number"})

    assert isinstance(returned_column.type, sqlalchemy.Float)


@pytest.mark.column
def test_spec_to_column_number_float():
    """
    GIVEN schema with number type and float format
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Float column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "number", "format": "float"})

    assert isinstance(returned_column.type, sqlalchemy.Float)


@pytest.mark.column
def test_spec_to_column_number_double():
    """
    GIVEN schema with number type and double format
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "number", "format": "double"})


@pytest.mark.column
def test_spec_to_column_number_unsupported_format():
    """
    GIVEN schema with number type and format that has not been implemented
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "number", "format": "unsupported"})


@pytest.mark.column
def test_spec_to_column_integer():
    """
    GIVEN schema with integer type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "integer"})

    assert isinstance(returned_column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_spec_to_column_integer_int32():
    """
    GIVEN schema with integer type and int32 format
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy Integer column is returned.
    """
    returned_column = column._spec_to_column(
        spec={"type": "integer", "format": "int32"}
    )

    assert isinstance(returned_column.type, sqlalchemy.Integer)


@pytest.mark.column
def test_spec_to_column_integer_int64():
    """
    GIVEN schema with integer type and int64 format
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy BigInteger column is returned.
    """
    returned_column = column._spec_to_column(
        spec={"type": "integer", "format": "int64"}
    )

    assert isinstance(returned_column.type, sqlalchemy.BigInteger)


@pytest.mark.column
def test_spec_to_column_integer_unsupported_format():
    """
    GIVEN schema with integer type and unsupported format
    WHEN _spec_to_column is called with the schema
    THEN FeatureNotImplementedError is raised.
    """
    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._spec_to_column(spec={"type": "integer", "format": "unsupported"})


@pytest.mark.column
def test_spec_to_column_string():
    """
    GIVEN schema with string type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy String column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "string"})

    assert isinstance(returned_column.type, sqlalchemy.String)


@pytest.mark.column
def test_spec_to_column_string_length():
    """
    GIVEN schema with string type and maxLength property
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy String column is returned with the length set to the maxLength.
    """
    returned_column = column._spec_to_column(spec={"type": "string", "maxLength": 1})

    assert returned_column.type.length == 1


@pytest.mark.column
def test_spec_to_column_boolean():
    """
    GIVEN schema with boolean type
    WHEN _spec_to_column is called with the schema
    THEN SQLAlchemy boolean column is returned.
    """
    returned_column = column._spec_to_column(spec={"type": "boolean"})

    assert isinstance(returned_column.type, sqlalchemy.Boolean)


@pytest.mark.column
def test_integration():
    """
    GIVEN schema and logical name
    WHEN handle_column is called with the schema
    THEN the logical name and an instance of SQLAlchemy Column is returned.
    """
    returned_column = column.handle_column(spec={"type": "number"})

    assert isinstance(returned_column, sqlalchemy.Column)


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
    THEN MalformedSchemaError is raised.
    """
    with pytest.raises(expected_exception):
        column.check_schema(schema=schema)


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "type 1"},
        {"type": "type 1", "format": "format 1"},
        {"type": "type 1", "maxLength": 1},
        {"type": "type 1", "nullable": True},
    ],
    ids=["type only", "type with format", "type with maxLength", "type with nullable"],
)
@pytest.mark.column
def test_check_schema_schema(schema):
    """
    GIVEN schema
    WHEN check_schema is called with the schema
    THEN the schema is returned.
    """
    returned_schema, _ = column.check_schema(schema=copy.deepcopy(schema))

    assert returned_schema == schema


@pytest.mark.column
def test_check_schema_schema_other():
    """
    GIVEN schema with an extra key
    WHEN check_schema is called with the schema
    THEN the schema without the extra key is returned.
    """
    schema = {"type": "type 1", "extra_key": "extra value"}

    returned_schema, _ = column.check_schema(schema=copy.deepcopy(schema))

    assert returned_schema == {"type": "type 1"}


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
            types.ColumnArtifacts("type 1", autoincrement=True),
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
    _, artifacts = column.check_schema(schema=schema)

    assert artifacts == expected_artifacts


@pytest.mark.column
def test_check_schema_required():
    """
    GIVEN schema
    WHEN check_schema is called with the schema and required True
    THEN nullable is False.
    """
    schema = {"type": "type 1"}

    returned_schema, artifacts = column.check_schema(
        schema=copy.deepcopy(schema), required=True
    )

    assert returned_schema == schema
    assert artifacts.nullable is False


@pytest.mark.parametrize(
    "type_, expected_type",
    [
        ("integer", sqlalchemy.Integer),
        ("number", sqlalchemy.Float),
        ("string", sqlalchemy.String),
        ("boolean", sqlalchemy.Boolean),
    ],
    ids=["integer", "number", "string", "boolean"],
)
@pytest.mark.column
def test_construct_column(type_, expected_type):
    """
    GIVEN artifacts for a type
    WHEN _construct_column is called with the artifacts
    THEN a column with the expected type is returned.
    """
    artifacts = types.ColumnArtifacts(type_)

    returned_column = column._construct_column(artifacts=artifacts)

    assert isinstance(returned_column, sqlalchemy.Column)
    assert isinstance(returned_column.type, expected_type)
    assert len(returned_column.foreign_keys) == 0
    assert returned_column.nullable is True


@pytest.mark.column
def test_construct_column_foreign_key():
    """
    GIVEN artifacts with foreign key
    WHEN _construct_column is called with the artifacts
    THEN a column with a foreign key is returned.
    """
    artifacts = types.ColumnArtifacts("integer", foreign_key="table.column")

    returned_column = column._construct_column(artifacts=artifacts)

    assert len(returned_column.foreign_keys) == 1
    foreign_key = returned_column.foreign_keys.pop()
    assert str(foreign_key) == "ForeignKey('table.column')"


@pytest.mark.parametrize("nullable", [True, False], ids=["true", "false"])
@pytest.mark.column
def test_construct_column_nullable(nullable):
    """
    GIVEN value for nullable
    WHEN _construct_column is called with the artifacts with nullable
    THEN the returned column nullable property is equal to nullable.
    """
    artifacts = types.ColumnArtifacts("integer", nullable=nullable)

    returned_column = column._construct_column(artifacts=artifacts)

    assert returned_column.nullable == nullable


@pytest.mark.parametrize(
    "primary_key", [None, True, False], ids=["none", "true", "false"]
)
@pytest.mark.column
def test_construct_column_primary_key(primary_key):
    """
    GIVEN value for primary_key
    WHEN _construct_column is called with the artifacts with primary_key
    THEN the returned column primary_key property is equal to primary_key.
    """
    artifacts = types.ColumnArtifacts("integer", primary_key=primary_key)

    returned_column = column._construct_column(artifacts=artifacts)

    assert returned_column.primary_key == primary_key


@pytest.mark.parametrize(
    "autoincrement", [None, True, False], ids=["none", "true", "false"]
)
@pytest.mark.column
def test_construct_column_autoincrement(autoincrement):
    """
    GIVEN value for autoincrement
    WHEN _construct_column is called with the artifacts with autoincrement
    THEN the returned column autoincrement property is equal to autoincrement.
    """
    artifacts = types.ColumnArtifacts("integer", autoincrement=autoincrement)

    returned_column = column._construct_column(artifacts=artifacts)

    assert returned_column.autoincrement == autoincrement


@pytest.mark.parametrize("index", [None, True, False], ids=["none", "true", "false"])
@pytest.mark.column
def test_construct_column_index(index):
    """
    GIVEN value for index
    WHEN _construct_column is called with the artifacts with index
    THEN the returned column index property is equal to index.
    """
    artifacts = types.ColumnArtifacts("integer", index=index)

    returned_column = column._construct_column(artifacts=artifacts)

    assert returned_column.index == index


@pytest.mark.parametrize("unique", [None, True, False], ids=["none", "true", "false"])
@pytest.mark.column
def test_construct_column_unique(unique):
    """
    GIVEN value for unique
    WHEN _construct_column is called with the artifacts with unique
    THEN the returned column unique property is equal to unique.
    """
    artifacts = types.ColumnArtifacts("integer", unique=unique)

    returned_column = column._construct_column(artifacts=artifacts)

    assert returned_column.unique == unique


@pytest.mark.column
def test_determine_type_unsupported():
    """
    GIVEN artifacts with an unsupported type
    WHEN _determine_type is called with the artifacts
    THEN FeatureNotImplementedError is raised.
    """
    artifacts = types.ColumnArtifacts("unsupported")

    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._determine_type(artifacts=artifacts)


@pytest.mark.parametrize(
    "type_, expected_type",
    [
        ("integer", sqlalchemy.Integer),
        ("number", sqlalchemy.Float),
        ("string", sqlalchemy.String),
        ("boolean", sqlalchemy.Boolean),
    ],
    ids=["integer", "number", "string", "boolean"],
)
@pytest.mark.column
def test_determine_type(type_, expected_type):
    """
    GIVEN type
    WHEN _determine_type is called with the artifacts with the type
    THEN the expected type is returned.
    """
    artifacts = types.ColumnArtifacts(type_)

    returned_type = column._determine_type(artifacts=artifacts)

    assert returned_type == expected_type


@pytest.mark.parametrize("artifacts_kwargs", [{"max_length": 1}], ids=["max_length"])
@pytest.mark.column
def test_handle_integer_invalid(artifacts_kwargs):
    """
    GIVEN artifacts with an artifact that is not supported
    WHEN _handle_integer is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = types.ColumnArtifacts("integer", **artifacts_kwargs)

    with pytest.raises(exceptions.MalformedSchemaError):
        column._handle_integer(artifacts=artifacts)


@pytest.mark.column
def test_handle_integer_invalid_format():
    """
    GIVEN artifacts with format that is not supported
    WHEN _handle_integer is called with the artifacts
    THEN FeatureNotImplementedError is raised.
    """
    artifacts = types.ColumnArtifacts("integer", format="unsupported")

    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._handle_integer(artifacts=artifacts)


@pytest.mark.parametrize(
    "format_, expected_integer",
    [
        (None, sqlalchemy.Integer),
        ("int32", sqlalchemy.Integer),
        ("int64", sqlalchemy.BigInteger),
    ],
    ids=["None", "int32", "int64"],
)
@pytest.mark.column
def test_handle_integer(format_, expected_integer):
    """
    GIVEN artifacts and expected SQLALchemy type
    WHEN _handle_integer is called with the artifacts
    THEN the expected type is returned.
    """
    artifacts = types.ColumnArtifacts("integer", format=format_)

    integer = column._handle_integer(artifacts=artifacts)

    assert integer == expected_integer


@pytest.mark.parametrize(
    "artifacts_kwargs",
    [{"max_length": 1}, {"autoincrement": True}],
    ids=["max_length", "autoincrement"],
)
@pytest.mark.column
def test_handle_number_invalid(artifacts_kwargs):
    """
    GIVEN artifacts with an artifact that is not supported
    WHEN _handle_number is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = types.ColumnArtifacts("number", **artifacts_kwargs)

    with pytest.raises(exceptions.MalformedSchemaError):
        column._handle_number(artifacts=artifacts)


@pytest.mark.column
def test_handle_number_invalid_format():
    """
    GIVEN artifacts with format that is not supported
    WHEN _handle_number is called with the artifacts
    THEN FeatureNotImplementedError is raised.
    """
    artifacts = types.ColumnArtifacts("number", format="unsupported")

    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._handle_number(artifacts=artifacts)


@pytest.mark.parametrize(
    "format_, expected_number",
    [(None, sqlalchemy.Float), ("float", sqlalchemy.Float)],
    ids=["None", "float"],
)
@pytest.mark.column
def test_handle_number(format_, expected_number):
    """
    GIVEN artifacts and expected SQLALchemy type
    WHEN _handle_integer is called with the artifacts
    THEN the expected type is returned.
    """
    artifacts = types.ColumnArtifacts("number", format=format_)

    number = column._handle_number(artifacts=artifacts)

    assert number == expected_number


@pytest.mark.parametrize(
    "artifacts_kwargs", [{"autoincrement": True}], ids=["autoincrement"]
)
@pytest.mark.column
def test_handle_string_invalid(artifacts_kwargs):
    """
    GIVEN artifacts with an artifact that is not supported
    WHEN _handle_string is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = types.ColumnArtifacts("string", **artifacts_kwargs)

    with pytest.raises(exceptions.MalformedSchemaError):
        column._handle_string(artifacts=artifacts)


@pytest.mark.column
def test_handle_string_invalid_format():
    """
    GIVEN artifacts with format that is not supported
    WHEN _handle_string is called with the artifacts
    THEN FeatureNotImplementedError is raised.
    """
    artifacts = types.ColumnArtifacts("string", format="unsupported")

    with pytest.raises(exceptions.FeatureNotImplementedError):
        column._handle_string(artifacts=artifacts)


@pytest.mark.parametrize(
    "format_, expected_type", [(None, sqlalchemy.String)], ids=["None"]
)
@pytest.mark.column
def test_handle_string(format_, expected_type):
    """
    GIVEN artifacts and expected SQLALchemy type
    WHEN _handle_integer is called with the artifacts
    THEN the expected type is returned.
    """
    artifacts = types.ColumnArtifacts("string", format=format_)

    string = column._handle_string(artifacts=artifacts)

    assert string == expected_type


@pytest.mark.column
def test_handle_string_max_length():
    """
    GIVEN artifacts with max_length
    WHEN _handle_string is called with the artifacts
    THEN a string with a maximum length is returned.
    """
    length = 1
    artifacts = types.ColumnArtifacts("string", max_length=length)

    string = column._handle_string(artifacts=artifacts)

    assert isinstance(string, sqlalchemy.String)
    assert string.length == length


@pytest.mark.parametrize(
    "artifacts_kwargs",
    [{"format": "format 1"}, {"max_length": 1}, {"autoincrement": True}],
    ids=["format", "max_length", "autoincrement"],
)
@pytest.mark.column
def test_handle_boolean_invalid(artifacts_kwargs):
    """
    GIVEN artifacts with an artifact that is not supported
    WHEN _handle_boolean is called with the artifacts
    THEN MalformedSchemaError is raised.
    """
    artifacts = types.ColumnArtifacts("boolean", **artifacts_kwargs)

    with pytest.raises(exceptions.MalformedSchemaError):
        column._handle_boolean(artifacts=artifacts)


@pytest.mark.column
def test_handle_boolean():
    """
    GIVEN artifacts
    WHEN _handle_integer is called with the artifacts
    THEN the boolean type is returned.
    """
    artifacts = types.ColumnArtifacts("boolean")

    boolean = column._handle_boolean(artifacts=artifacts)

    assert boolean == sqlalchemy.Boolean
