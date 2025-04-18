from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.common import property_to_schema
from db.models import Property, PropertyType, PropertyValue
from exceptions import UnknownPropertyTypeError
from schemas.property import PropertyCreateSchema, PropertyIntResponseSchema, PropertyListResponseSchema


async def create_property(
    data: PropertyCreateSchema, db: AsyncSession
) -> PropertyIntResponseSchema | PropertyListResponseSchema:
    """Создание свойства."""

    if (await db.execute(select(Property).filter_by(uid=data.uid))).scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Property exists")
    prop = Property(uid=data.uid, name=data.name, type=data.type)
    if data.type is PropertyType.LIST:
        for property_value in data.values:
            prop.values.append(PropertyValue(uid=property_value.value_uid, value=property_value.value))
    elif data.type is PropertyType.INT:
        prop.values = []
    else:
        raise UnknownPropertyTypeError(data.type)
    db.add(prop)
    await db.commit()
    return await property_to_schema(prop)


async def delete_property(uid: UUID, db: AsyncSession) -> None:
    """Удаление свойства."""

    result = await db.execute(select(Property).filter_by(uid=uid))
    if not (prop := result.scalar()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    await db.delete(prop)
    await db.commit()
