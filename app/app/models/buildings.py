from decimal import Decimal

from sqlmodel import BigInteger, Field, Index, Relationship, SQLModel


class CityModel(SQLModel, table=True):
    __tablename__ = "city"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    name: str = Field(max_length=256)
    streets: list["StreetModel"] = Relationship(back_populates="city")


class StreetModel(SQLModel, table=True):
    __tablename__ = "street"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    name: str = Field(max_length=256)
    city_id: int = Field(foreign_key="city.id", sa_type=BigInteger)
    city: "CityModel" = Relationship(back_populates="streets")
    buildings: list["BuildingModel"] = Relationship(back_populates="street")


class BuildingModel(SQLModel, table=True):
    __tablename__ = "building"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    name: str = Field(max_length=256)
    street_id: int = Field(foreign_key="street.id", sa_type=BigInteger)
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    street: "StreetModel" = Relationship(back_populates="buildings")
    addresses: list["OrganisationAddressModel"] = Relationship(back_populates="building")  # noqa: F821

    __table_args__ = (Index("idx_building_coords", "latitude", "longitude"),)


__all__ = [
    "CityModel",
    "StreetModel",
    "BuildingModel",
]
