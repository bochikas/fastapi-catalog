from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.common import product_to_schema
from db.models import Product, ProductProperty, Property, PropertyType, PropertyValue
from exceptions import UnknownPropertyTypeError
from schemas.product import ProductCreateSchema, ProductResponseSchema


async def create_product(data: ProductCreateSchema, db: AsyncSession) -> ProductResponseSchema:
    """Создание товара."""

    if (await db.execute(select(Product).filter_by(uid=data.uid))).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product exists")

    product = Product(uid=data.uid, name=data.name)
    for prop in data.properties:
        property_obj = (await db.execute(select(Property).filter_by(uid=prop.uid))).scalar()
        if not property_obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Property {prop.uid} not found")

        if property_obj.type is PropertyType.INT:
            if prop.value is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Type of property id {prop.uid} is not int"
                )
            product.properties.append(ProductProperty(property_id=prop.uid, int_value=prop.value))
        elif property_obj.type is PropertyType.LIST:
            value = (await db.execute(select(PropertyValue).filter_by(uid=prop.value_uid))).first()
            if not value:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Value {prop.value_uid} not found")
            product.properties.append(ProductProperty(property_id=prop.uid, value_uid=prop.value_uid))
        else:
            raise UnknownPropertyTypeError(property_obj.type)

    db.add(product)
    await db.commit()
    return await product_to_schema(product)


async def get_product(uid: UUID, db: AsyncSession) -> ProductResponseSchema:
    """Получение товара по UID."""

    result = await db.execute(select(Product).filter_by(uid=uid))
    if not (product := result.scalar()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return await product_to_schema(product)


async def delete_product(uid: UUID, db: AsyncSession) -> None:
    """Удаление товара по UID."""

    result = await db.execute(select(Product).filter_by(uid=uid))
    if not (product := result.scalar()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    await db.delete(product)
    await db.commit()
