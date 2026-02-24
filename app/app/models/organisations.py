from decimal import Decimal
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, model_validator
from sqlmodel import BigInteger, Field, Index, Relationship, SQLModel, text

from app.exceptions import CustomValidationError

# class ActivityModel(SQLModel, table=True):
#     __tablename__ = "activity"
#
#     id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
#     name: str = Field(max_length=256)
#     parent_id: int | None = Field(foreign_key="activity.id", sa_type=BigInteger)
#
#
# class CityModel(SQLModel, table=True):
#     __tablename__ = "city"
#
#     id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
#     name: str = Field(max_length=256)
#     streets: list["StreetModel"] = Relationship(back_populates="city")
#
#
# class StreetModel(SQLModel, table=True):
#     __tablename__ = "street"
#
#     id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
#     name: str = Field(max_length=256)
#     city_id: int = Field(foreign_key="city.id", sa_type=BigInteger)
#     city: "CityModel" = Relationship(back_populates="streets")
#     buildings: list["BuildingModel"] = Relationship(back_populates="street")
#
#
# class BuildingModel(SQLModel, table=True):
#     __tablename__ = "building"
#
#     id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
#     name: str = Field(max_length=256)
#     street_id: int = Field(foreign_key="street.id", sa_type=BigInteger)
#     latitude: float = Field(ge=-90, le=90)
#     longitude: float = Field(ge=-180, le=180)
#     street: "StreetModel" = Relationship(back_populates="buildings")
#     addresses: list["OrganisationAddressModel"] = Relationship(back_populates="building")
#


class OrganisationTypes(StrEnum):
    LLC = "LLC"
    IP = "IP"


class OrganisationModel(SQLModel, table=True):
    __tablename__ = "organisation"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    type: OrganisationTypes = Field(max_length=3, sa_column_kwargs={"nullable": False})
    name: str = Field(max_length=256)
    address_id: int = Field(foreign_key="organisation_address.id", sa_type=BigInteger)
    phones: list["PhoneModel"] = Relationship(back_populates="organisation")
    activities: list["OrganisationActivityModel"] = Relationship(back_populates="organisation")
    address: "OrganisationAddressModel" = Relationship(back_populates="organisations")

    __table_args__ = (
        Index(
            "idx_org_name_trgm",
            text("name gin_trgm_ops"),
            postgresql_using="gin",
        ),
    )


class OrganisationAddressModel(SQLModel, table=True):
    __tablename__ = "organisation_address"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    building_id: int = Field(foreign_key="building.id", sa_type=BigInteger)
    office: str = Field(max_length=128)
    building: "BuildingModel" = Relationship(back_populates="addresses")  # noqa: F821
    organisations: list["OrganisationModel"] = Relationship(back_populates="address")  # noqa: F821


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


class PhoneResponseModel(BaseModel):
    phone: str


class ActivityResponseModel(BaseModel):
    id: int


class OrganisationDetailResponseModel(BaseModel):
    id: int
    type: OrganisationTypes
    name: str
    address: str
    phones: list[PhoneResponseModel]
    activities: list[ActivityResponseModel]


class OrganisationListResponseModel(BaseModel):
    id: int
    type: OrganisationTypes
    name: str


class OrganisationFilterModel(BaseModel):
    name: str | None = None
    activity_id: int | None = None
    building_id: int | None = None
    latitude_from: Decimal | None = None
    latitude_to: Decimal | None = None
    longitude_from: Decimal | None = None
    longitude_to: Decimal | None = None

    @model_validator(mode="after")
    def check_coords_completeness(self) -> Self:
        coords = [self.latitude_from, self.latitude_to, self.longitude_from, self.longitude_to]

        if 0 < sum(1 for c in coords if c is not None) < 4:  # noqa: PLR2004
            raise CustomValidationError(msg="latitude_from, latitude_to, longitude_from, longitude_to must be send.")

        return self


__all__ = [
    "OrganisationTypes",
    "OrganisationModel",
    "PhoneModel",
    "OrganisationActivityModel",
]
