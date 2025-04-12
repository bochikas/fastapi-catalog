from uuid import UUID

from pydantic import BaseModel


class ProductPropertyCreateSchema(BaseModel):
    uid: UUID
    value_uid: UUID | None = None
    value: int | None = None


class ProductPropertyListSchema(BaseModel):
    uid: UUID
    name: str
    value_uid: UUID
    value: str


class ProductPropertyIntSchema(BaseModel):
    uid: UUID
    name: str
    value: int


class ProductCreateSchema(BaseModel):
    uid: UUID
    name: str | None
    properties: list[ProductPropertyCreateSchema]


class ProductResponseSchema(BaseModel):
    uid: UUID
    name: str | None
    properties: list[ProductPropertyListSchema | ProductPropertyIntSchema]

    class Config:
        from_attributes = True
