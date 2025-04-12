from uuid import UUID

from pydantic import BaseModel


class ProductPropertyCreateSchema(BaseModel):
    uid: UUID
    value_uid: UUID | None = None
    value: int | None = None


class ProductPropertySchema(BaseModel):
    uid: UUID
    name: str | None
    value_uid: UUID | None = None
    value: str | int | None


class ProductCreateSchema(BaseModel):
    uid: UUID
    name: str | None
    properties: list[ProductPropertyCreateSchema]


class ProductSchema(BaseModel):
    uid: UUID
    name: str | None
    properties: list[ProductPropertySchema]

    class Config:
        from_attributes = True
