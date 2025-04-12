from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from schemas.product import ProductResponseSchema


class CatalogResponseSchema(BaseModel):
    products: list[ProductResponseSchema]
    count: int


class CatalogFilterResponseSchema(BaseModel):
    count: int

    model_config = ConfigDict(extra="allow")


class SortType(StrEnum):
    UID = "uid"
    NAME = "name"
