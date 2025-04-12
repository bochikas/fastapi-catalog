from uuid import UUID

from pydantic import BaseModel, Field

from db.base import PropertyType


class PropertyValueSchema(BaseModel):
    value_uid: UUID = Field(..., alias="uid")
    value: str

    class Config:
        from_attributes = True
        validate_by_name = True


class PropertySchema(BaseModel):
    uid: UUID
    name: str | None
    type: PropertyType
    values: list[PropertyValueSchema] | None = None

    class Config:
        from_attributes = True


class PropertyCreateSchema(BaseModel):
    uid: UUID
    name: str
    type: PropertyType
    values: list[PropertyValueSchema] | None = None

    class Config:
        from_attributes = True
