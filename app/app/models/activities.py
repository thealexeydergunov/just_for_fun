from sqlmodel import BigInteger, Field, SQLModel


class ActivityModel(SQLModel, table=True):
    __tablename__ = "activity"

    id: int = Field(primary_key=True, sa_type=BigInteger, sa_column_kwargs={"autoincrement": True})
    name: str = Field(max_length=256)
    parent_id: int | None = Field(foreign_key="activity.id", sa_type=BigInteger)


__all__ = [
    "ActivityModel",
]
