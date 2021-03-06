Many to One
===========

A many to one relationship associates many children with a single parent. For
example, a company can have many employees working in the same division (for
example engineering, legal, marketing, ...) but a particular employee can only
work in one division.

.. seealso::

    :ref:`many-to-one`
      OpenAlchemy documentation for many to one relationships.

    `SQLAlchemy Many to One <https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-one>`_
      SQLAlchemy documentation for many to one relationships.

The following example defines a many to one relationship between *Employee*
and *Division*:

.. literalinclude:: ../../../../examples/relationship/many_to_one/example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/models.py
    :language: python
    :linenos:

The SQLAlchemy models generated by OpenAlchemy are equivalent to the following
traditional models file:

.. literalinclude:: ../../../../examples/relationship/many_to_one/models_traditional.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/models_auto.py
    :language: python
    :linenos:

Nullable
--------

The OpenAPI *nullable* directive can be used to control the nullability of the
many to one relationship.

.. seealso::

    :ref:`many-to-one-nullable`
      OpenAlchemy documentation for the nullability of many to one
      relationships.

The following example defines a many to one relationship between *Employee* and
*Division* that is not nullable:

.. literalinclude:: ../../../../examples/relationship/many_to_one/not-nullable-example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/not_nullable_models.py
    :language: python
    :linenos:

The SQLAlchemy models generated by OpenAlchemy are equivalent to the following
traditional models file:

.. literalinclude:: ../../../../examples/relationship/many_to_one/not_nullable_models_traditional.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/not_nullable_models_auto.py
    :language: python
    :linenos:

Backref
-------

SQLAlchemy allows for back references so that the on the child side of the
relationship the parent model is also accessible.

.. seealso::

    :ref:`backref`
      OpenAlchemy documentation for back references.

The following example defines a many to one relationship between *Employee* and
*Division* that includes a back reference on *Division* to *Employee*:

.. literalinclude:: ../../../../examples/relationship/many_to_one/backref-example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/backref_models.py
    :language: python
    :linenos:

The SQLAlchemy models generated by OpenAlchemy are equivalent to the following
traditional models file:

.. literalinclude:: ../../../../examples/relationship/many_to_one/backref_models_traditional.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/backref_models_auto.py
    :language: python
    :linenos:

Custom Foreign Key Column
-------------------------

By default, OpenAlchemy will pick the *id* property to construct the underlying
foreign key constraint for a relationship. This can be changed using the
*x-foreign-key-column* extension property.

.. seealso::

    :ref:`custom-foreign-key`
      OpenAlchemy documentation for custom foreign key columns.

The following example defines a many to one relationship between *Employee* and
*Division* where the *name* column is used instead of the *id* column to
construct the foreign key:

.. literalinclude:: ../../../../examples/relationship/many_to_one/custom-foreign-key-example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/custom_foreign_key_models.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/custom_foreign_key_models_auto.py
    :language: python
    :linenos:

Relationship kwargs
-------------------

There are a range of keyword arguments for the *relationship* in SQLAlchemy for
a range of use cases. OpenAlchemy supports these using the *x-kwargs* extension
property that can be defined along with an object or array reference.

.. seealso::

    :ref:`relationship-kwargs`
      OpenAlchemy documentation for relationship keyword arguments.

    `SQLAlchemy Relationship API <https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#relationships-api>`_
      Documentation of the SQLAlchemy relationship API.

The following example defines the *order_by* keyword argument for the
relationship between *Employee* and *Division*:

.. literalinclude:: ../../../../examples/relationship/many_to_one/kwargs-example-spec.yml
    :language: yaml
    :linenos:

The following file uses OpenAlchemy to generate the SQLAlchemy models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/kwargs_models.py
    :language: python
    :linenos:

The SQLAlchemy models generated by OpenAlchemy are equivalent to the following
traditional models file:

.. literalinclude:: ../../../../examples/relationship/many_to_one/kwargs_models_traditional.py
    :language: python
    :linenos:

OpenAlchemy will generate the following typed models:

.. literalinclude:: ../../../../examples/relationship/many_to_one/kwargs_models_auto.py
    :language: python
    :linenos:
