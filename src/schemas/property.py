from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from db.base import PropertyType


class PropertyValueSchema(BaseModel):
    value_uid: UUID = Field(..., alias="uid")
    value: str

    class Config:
        from_attributes = True
        validate_by_name = True


class PropertyListResponseSchema(BaseModel):
    uid: UUID
    name: str
    type: PropertyType
    values: list[PropertyValueSchema]

    class Config:
        from_attributes = True


class PropertyIntResponseSchema(BaseModel):
    uid: UUID
    name: str
    type: PropertyType

    class Config:
        from_attributes = True


class PropertyCreateSchema(BaseModel):
    uid: UUID
    name: str
    type: PropertyType
    values: list[PropertyValueSchema] | None = None

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def check_value(cls, data) -> dict:
        if data.get("type") is PropertyType.LIST and not data.get("values"):
            raise ValueError("List property must have values")
        return data
