"""Construct the link (foreign key or association table) between models."""

from open_alchemy import facades
from open_alchemy import types

from . import association_table as _association_table
from . import foreign_key as _foreign_key


def construct(
    *,
    artifacts: types.ObjectArtifacts,
    model_schema: types.Schema,
    schemas: types.Schemas,
) -> None:
    """
    Construct the link between the tables for a reference between models in an array.

    For a one to many relationship, a foreign key is added to the referenced table. For
    a many to many relationship, an association table is constructed.

    Args:
        artifacts: The object reference artifacts.
        model_schema: The schema of the model in which the array reference is embedded.
        schemas: Used to retrieve the referenced schema and to resolve any $ref.

    """
    if artifacts.relationship.secondary is None:
        _foreign_key.set_(
            ref_model_name=artifacts.relationship.model_name,
            logical_name=artifacts.logical_name,
            model_schema=model_schema,
            schemas=schemas,
            fk_column=artifacts.fk_column,
        )
    else:
        table = _association_table.construct(
            parent_schema=model_schema,
            child_schema=artifacts.spec,
            schemas=schemas,
            tablename=artifacts.relationship.secondary,
        )
        facades.models.set_association(
            table=table, name=artifacts.relationship.secondary
        )
