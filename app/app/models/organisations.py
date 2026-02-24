from enum import StrEnum

from pydantic import BaseModel
from sqlmodel import BigInteger, Field, Relationship, SQLModel


class OrganisationTypes(StrEnum):
    LLC = "LLC"
    IP = "IP"


class OrganisationModel(SQLModel, table=True):
    __tablename__ = "organisation"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    type: OrganisationTypes = Field(max_length=3, sa_column_kwargs={"nullable": False})
    name: str = Field(max_length=256)
    phones: list["PhoneModel"] = Relationship(back_populates="organisation")
    activities: list["OrganisationActivityModel"] = Relationship(back_populates="organisation")


class PhoneModel(SQLModel, table=True):
    __tablename__ = "phone"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    phone: str = Field(max_length=14)
    organisation_id: int = Field(foreign_key="organisation.id", sa_type=BigInteger)
    organisation: OrganisationModel = Relationship(back_populates="phones")


class OrganisationActivityModel(SQLModel, table=True):
    __tablename__ = "organisation_activity"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    organisation_id: int = Field(foreign_key="organisation.id", sa_type=BigInteger)
    activity_id: int = Field(foreign_key="activity.id", sa_type=BigInteger)
    organisation: OrganisationModel = Relationship(back_populates="activities")


class PhoneResponse(BaseModel):
    phone: str


class ActivityResponse(BaseModel):
    id: int


class OrganisationDetailResponse(BaseModel):
    id: int
    type: OrganisationTypes
    name: str
    phones: list[PhoneResponse]
    activities: list[ActivityResponse]


class OrganisationListResponse(BaseModel):
    id: int
    type: OrganisationTypes
    name: str


class OrganisationFilter(BaseModel):
    name: str | None = None
    activity_id: int | None = None
    building_id: int | None = None


__all__ = [
    "OrganisationTypes",
    "OrganisationModel",
    "PhoneModel",
    "OrganisationActivityModel",
    "PhoneResponse",
    "ActivityResponse",
    "OrganisationDetailResponse",
    "OrganisationFilter",
]
