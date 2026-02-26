from pydantic import BaseModel, Field


class PaginatorModel(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=500, description="Count objects per page")


class PaginatedResponseModel[T](PaginatorModel):
    items: list[T]
