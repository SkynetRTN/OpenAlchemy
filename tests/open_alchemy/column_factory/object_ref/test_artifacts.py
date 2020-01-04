"""Tests for object reference artifacts."""

import pytest

from open_alchemy import exceptions
from open_alchemy.column_factory.object_ref import artifacts


@pytest.mark.parametrize(
    "schemas",
    [
        {
            "RefSchema": {
                "x-tablename": "ref_schema",
                "properties": {"id": {"type": "integer"}},
            }
        },
        {
            "RefSchema": {
                "type": "notObject",
                "x-tablename": "ref_schema",
                "properties": {"id": {"type": "integer"}},
            }
        },
    ],
    ids=["no type", "not object type"],
)
@pytest.mark.column
def test_ref_error(schemas):
    """
    GIVEN referenced schema that is not valid and schema
    WHEN _handle_schema is called with the schema and schemas
    THEN MalformedRelationshipError is raised.
    """
    # pylint: disable=protected-access
    schema = {"$ref": "#/components/schemas/RefSchema"}

    with pytest.raises(exceptions.MalformedRelationshipError):
        artifacts._handle_schema(logical_name="", schema=schema, schemas=schemas)


@pytest.mark.parametrize(
    "schema",
    [
        [{"type": "object"}],
        [
            {"$ref": "#/components/schemas/Schema1"},
            {"$ref": "#/components/schemas/Schema2"},
        ],
        [
            {"$ref": "#/components/schemas/Schema1"},
            {"x-backref": "backSchema1"},
            {"x-backref": "backSchema2"},
        ],
        [
            {"$ref": "#/components/schemas/Schema1"},
            {"x-secondary": "secondary 1"},
            {"x-secondary": "secondary 2"},
        ],
        [
            {"$ref": "#/components/schemas/Schema1"},
            {"x-foreign-key-column": "column 1"},
            {"x-foreign-key-column": "column 2"},
        ],
        [
            {"$ref": "#/components/schemas/Schema1"},
            {"x-uselist": True},
            {"x-uselist": False},
        ],
        [
            {"$ref": "#/components/schemas/Schema1"},
            {"nullable": True},
            {"nullable": False},
        ],
    ],
    ids=[
        "object",
        "multiple ref",
        "multiple x-backref",
        "multiple x-secondary",
        "multiple x-foreign-key-column",
        "multiple x-uselist",
        "multiple nullable",
    ],
)
@pytest.mark.column
def test_all_of_error(schema):
    """
    GIVEN schema
    WHEN _handle_schema is called with the schema
    THEN MalformedRelationshipError is raised.
    """
    # pylint: disable=protected-access
    schema = {"allOf": schema}
    schemas = {"Schema1": {"type": "object"}, "Schema2": {"type": "object"}}

    with pytest.raises(exceptions.MalformedRelationshipError):
        artifacts._handle_schema(logical_name="", schema=schema, schemas=schemas)


@pytest.mark.column
def test_gather_no_ref_all_of():
    """
    GIVEN empty schema
    WHEN gather is called with the schema
    THEN MalformedRelationshipError is raised.
    """
    with pytest.raises(exceptions.MalformedRelationshipError):
        artifacts.gather(schema={}, logical_name="", schemas={})


@pytest.mark.parametrize(
    "schema, schemas, expected_spec",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            {"type": "object"},
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"allOf": [{"type": "object"}]}},
            {"type": "object"},
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            {"type": "object"},
        ),
    ],
    ids=["$ref", "$ref to allOf", "allOf"],
)
@pytest.mark.column
def test_gather_object_artifacts_spec(schema, schemas, expected_spec):
    """
    GIVEN schema, schemas and expected schema
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN the expected schema is returned.
    """
    obj_artifacts = artifacts.gather(schema=schema, logical_name="", schemas=schemas)

    assert obj_artifacts.spec == expected_spec


@pytest.mark.parametrize(
    "schema, schemas",
    [
        ({"$ref": "#/components/schemas/RefSchema"}, {"RefSchema": {"type": "object"}}),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
        ),
    ],
    ids=["$ref", "allOf"],
)
@pytest.mark.column
def test_gather_object_artifacts_ref_logical_name(schema, schemas):
    """
    GIVEN schema and schemas
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN the referenced schema name is returned as the ref logical name.
    """
    obj_artifacts = artifacts.gather(schema=schema, logical_name="", schemas=schemas)

    assert obj_artifacts.relationship.model_name == "RefSchema"


@pytest.mark.parametrize(
    "schema, schemas, expected_backref",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-backref": "backref 1"}},
            "backref 1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                    {"x-uselist": False},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2", "x-uselist": False},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "backref 2",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object", "x-backref": "backref 1"}},
            "backref 1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object", "x-backref": "backref 1"}},
            "backref 2",
        ),
    ],
    ids=[
        "$ref no backref",
        "$ref backref",
        "allOf no backref",
        "allOf backref",
        "allOf backref before other",
        "allOf backref after other",
        "allOf backref with uselist",
        "allOf $ref backref",
        "allOf backref $ref backref",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_backref(schema, schemas, expected_backref):
    """
    GIVEN schema and schemas and expected backref
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN the expected backref is returned.
    """
    obj_artifacts = artifacts.gather(schema=schema, logical_name="", schemas=schemas)

    if expected_backref is None:
        assert obj_artifacts.relationship.back_reference is None
    else:
        returned_backref = obj_artifacts.relationship.back_reference.property_name
        assert returned_backref == expected_backref


@pytest.mark.column
def test_gather_object_artifacts_uselist_no_backref():
    """
    GIVEN schema with uselist but not backref and schemas
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN MalformedRelationshipError is raised.
    """
    schema = {"$ref": "#/components/schemas/RefSchema"}
    schemas = {"RefSchema": {"type": "object", "x-uselist": False}}

    with pytest.raises(exceptions.MalformedRelationshipError):
        artifacts.gather(schema=schema, logical_name="", schemas=schemas)


@pytest.mark.parametrize(
    "schema, schemas, expected_uselist",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {
                "RefSchema": {
                    "type": "object",
                    "x-backref": "backref 1",
                    "x-uselist": True,
                }
            },
            True,
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            False,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-uselist": False, "x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            False,
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {
                "RefSchema": {
                    "type": "object",
                    "x-backref": "backref 1",
                    "x-uselist": True,
                }
            },
            True,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                    {"x-uselist": False},
                ]
            },
            {
                "RefSchema": {
                    "type": "object",
                    "x-backref": "backref 1",
                    "x-uselist": True,
                }
            },
            False,
        ),
    ],
    ids=[
        "$ref no uselist",
        "$ref uselist",
        "allOf no uselist",
        "allOf uselist",
        "allOf uselist with backref",
        "allOf $ref uselist",
        "allOf uselist $ref uselist",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_uselist(schema, schemas, expected_uselist):
    """
    GIVEN schema and schemas and expected uselist
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN the expected uselist is returned.
    """
    obj_artifacts = artifacts.gather(schema=schema, logical_name="", schemas=schemas)

    if expected_uselist is None:
        assert obj_artifacts.relationship.back_reference is None
    else:
        assert obj_artifacts.relationship.back_reference.uselist == expected_uselist


@pytest.mark.parametrize(
    "schema, schemas, expected_secondary",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-secondary": "secondary 1"}},
            "secondary 1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "secondary 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "secondary 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "secondary 2"},
                    {"x-backref": "backref 1"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "secondary 2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 1"},
                    {"x-secondary": "secondary 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "secondary 2",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object", "x-secondary": "secondary 1"}},
            "secondary 1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-secondary": "secondary 2"},
                ]
            },
            {"RefSchema": {"type": "object", "x-secondary": "secondary 1"}},
            "secondary 2",
        ),
    ],
    ids=[
        "$ref no secondary",
        "$ref secondary",
        "allOf no secondary",
        "allOf secondary",
        "allOf secondary before other",
        "allOf secondary after other",
        "allOf $ref secondary",
        "allOf secondary $ref secondary",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_secondary(schema, schemas, expected_secondary):
    """
    GIVEN schema and schemas and expected secondary
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN the expected secondary is returned.
    """
    obj_artifacts = artifacts.gather(schema=schema, logical_name="", schemas=schemas)

    assert obj_artifacts.relationship.secondary == expected_secondary


@pytest.mark.parametrize(
    "schema, schemas, expected_fk_column",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            "id",
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "x-foreign-key-column": "fk_column_1"}},
            "fk_column_1",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            "id",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "fk_column_2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "fk_column_2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "fk_column_2"},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "fk_column_2",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                    {"x-foreign-key-column": "fk_column_2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            "fk_column_2",
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object", "x-foreign-key-column": "fk_column_1"}},
            "fk_column_1",
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-foreign-key-column": "fk_column_2"},
                ]
            },
            {"RefSchema": {"type": "object", "x-foreign-key-column": "fk_column_1"}},
            "fk_column_2",
        ),
    ],
    ids=[
        "$ref no fk",
        "$ref fk",
        "allOf no fk",
        "allOf fk",
        "allOf fk before other",
        "allOf fk after other",
        "allOf $ref fk",
        "allOf fk $ref fk",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_fk_column(schema, schemas, expected_fk_column):
    """
    GIVEN schema and schemas and expected foreign key column
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN the expected foreign key column is returned.
    """
    obj_artifacts = artifacts.gather(schema=schema, logical_name="", schemas=schemas)

    assert obj_artifacts.fk_column == expected_fk_column


@pytest.mark.parametrize(
    "schema, schemas, expected_nullable",
    [
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {"$ref": "#/components/schemas/RefSchema"},
            {"RefSchema": {"type": "object", "nullable": True}},
            True,
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object"}},
            None,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"nullable": False},
                ]
            },
            {"RefSchema": {"type": "object"}},
            False,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"nullable": False},
                    {"x-backref": "backref 2"},
                ]
            },
            {"RefSchema": {"type": "object"}},
            False,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"x-backref": "backref 2"},
                    {"nullable": False},
                ]
            },
            {"RefSchema": {"type": "object"}},
            False,
        ),
        (
            {"allOf": [{"$ref": "#/components/schemas/RefSchema"}]},
            {"RefSchema": {"type": "object", "nullable": True}},
            True,
        ),
        (
            {
                "allOf": [
                    {"$ref": "#/components/schemas/RefSchema"},
                    {"nullable": False},
                ]
            },
            {"RefSchema": {"type": "object", "nullable": True}},
            False,
        ),
    ],
    ids=[
        "$ref no fk",
        "$ref fk",
        "allOf no fk",
        "allOf fk",
        "allOf fk before other",
        "allOf fk after other",
        "allOf $ref fk",
        "allOf fk $ref fk",
    ],
)
@pytest.mark.column
def test_gather_object_artifacts_nullable(schema, schemas, expected_nullable):
    """
    GIVEN schema and schemas and expected nullable value
    WHEN gather_object_artifacts is called with the schema and schemas
    THEN the expected nullable value is returned.
    """
    obj_artifacts = artifacts.gather(schema=schema, logical_name="", schemas=schemas)

    assert obj_artifacts.nullable == expected_nullable