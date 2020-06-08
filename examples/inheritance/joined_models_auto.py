"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""
# pylint: disable=no-member,super-init-not-called,unused-argument

import typing

import sqlalchemy
from sqlalchemy import orm

from open_alchemy import models


class EmployeeDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    name: typing.Optional[str]
    type: typing.Optional[str]


class TEmployee(typing.Protocol):
    """
    SQLAlchemy model protocol.

    Person that works for a company.

    Attrs:
        id: Unique identifier for the employee.
        name: The name of the employee.
        type: The type of the employee.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: "sqlalchemy.Column[typing.Optional[int]]"
    name: "sqlalchemy.Column[typing.Optional[str]]"
    type: "sqlalchemy.Column[typing.Optional[str]]"

    def __init__(
        self,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        type: typing.Optional[str] = None,
    ) -> None:
        """
        Construct.

        Args:
            id: Unique identifier for the employee.
            name: The name of the employee.
            type: The type of the employee.

        """
        ...

    @classmethod
    def from_dict(
        cls,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        type: typing.Optional[str] = None,
    ) -> "TEmployee":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: Unique identifier for the employee.
            name: The name of the employee.
            type: The type of the employee.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TEmployee":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> EmployeeDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Employee: typing.Type[TEmployee] = models.Employee  # type: ignore


class ManagerDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    name: typing.Optional[str]
    type: typing.Optional[str]
    manager_data: typing.Optional[str]


class TManager(typing.Protocol):
    """
    SQLAlchemy model protocol.

    Person that works for a company.

    Attrs:
        id: Unique identifier for the manager.
        name: The name of the employee.
        type: The type of the employee.
        manager_data: Data for the manager.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: "sqlalchemy.Column[typing.Optional[int]]"
    name: "sqlalchemy.Column[typing.Optional[str]]"
    type: "sqlalchemy.Column[typing.Optional[str]]"
    manager_data: "sqlalchemy.Column[typing.Optional[str]]"

    def __init__(
        self,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        type: typing.Optional[str] = None,
        manager_data: typing.Optional[str] = None,
    ) -> None:
        """
        Construct.

        Args:
            id: Unique identifier for the manager.
            name: The name of the employee.
            type: The type of the employee.
            manager_data: Data for the manager.

        """
        ...

    @classmethod
    def from_dict(
        cls,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        type: typing.Optional[str] = None,
        manager_data: typing.Optional[str] = None,
    ) -> "TManager":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: Unique identifier for the manager.
            name: The name of the employee.
            type: The type of the employee.
            manager_data: Data for the manager.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TManager":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> ManagerDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Manager: typing.Type[TManager] = models.Manager  # type: ignore


class EngineerDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    name: typing.Optional[str]
    type: typing.Optional[str]
    engineer_info: typing.Optional[str]


class TEngineer(typing.Protocol):
    """
    SQLAlchemy model protocol.

    Person that works for a company.

    Attrs:
        id: Unique identifier for the engineer.
        name: The name of the employee.
        type: The type of the employee.
        engineer_info: Information for the manager.

    """

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: "sqlalchemy.Column[typing.Optional[int]]"
    name: "sqlalchemy.Column[typing.Optional[str]]"
    type: "sqlalchemy.Column[typing.Optional[str]]"
    engineer_info: "sqlalchemy.Column[typing.Optional[str]]"

    def __init__(
        self,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        type: typing.Optional[str] = None,
        engineer_info: typing.Optional[str] = None,
    ) -> None:
        """
        Construct.

        Args:
            id: Unique identifier for the engineer.
            name: The name of the employee.
            type: The type of the employee.
            engineer_info: Information for the manager.

        """
        ...

    @classmethod
    def from_dict(
        cls,
        id: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        type: typing.Optional[str] = None,
        engineer_info: typing.Optional[str] = None,
    ) -> "TEngineer":
        """
        Construct from a dictionary (eg. a POST payload).

        Args:
            id: Unique identifier for the engineer.
            name: The name of the employee.
            type: The type of the employee.
            engineer_info: Information for the manager.

        Returns:
            Model instance based on the dictionary.

        """
        ...

    @classmethod
    def from_str(cls, value: str) -> "TEngineer":
        """
        Construct from a JSON string (eg. a POST payload).

        Returns:
            Model instance based on the JSON string.

        """
        ...

    def to_dict(self) -> EngineerDict:
        """
        Convert to a dictionary (eg. to send back for a GET request).

        Returns:
            Dictionary based on the model instance.

        """
        ...

    def to_str(self) -> str:
        """
        Convert to a JSON string (eg. to send back for a GET request).

        Returns:
            JSON string based on the model instance.

        """
        ...


Engineer: typing.Type[TEngineer] = models.Engineer  # type: ignore