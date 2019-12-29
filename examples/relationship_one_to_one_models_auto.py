"""Autogenerated SQLAlchemy models based on OpenAlchemy models."""
# pylint: disable=no-member,useless-super-delegation

import typing

import sqlalchemy
from sqlalchemy import orm

from open_alchemy import models


class PayInfoDict(typing.TypedDict, total=False):
    """TypedDict for properties that are not required."""

    id: typing.Optional[int]
    account_number: typing.Optional[str]


class PayInfo(models.PayInfo):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: typing.Optional[int]
    account_number: typing.Optional[str]
    employee: typing.Optional["Employee"]

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "PayInfo":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> PayInfoDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()


class EmployeeDict(typing.TypedDict, total=True):
    """TypedDict for properties that are required."""

    id: int
    name: str
    pay_info: "PayInfoDict"


class Employee(models.Employee):
    """SQLAlchemy model."""

    # SQLAlchemy properties
    __table__: sqlalchemy.Table
    __tablename__: str
    query: orm.Query

    # Model properties
    id: int
    name: str
    pay_info: "PayInfo"

    @classmethod
    def from_dict(cls, **kwargs: typing.Any) -> "Employee":
        """Construct from a dictionary (eg. a POST payload)."""
        return super().from_dict(**kwargs)

    def to_dict(self) -> EmployeeDict:
        """Convert to a dictionary (eg. to send back for a GET request)."""
        return super().to_dict()
