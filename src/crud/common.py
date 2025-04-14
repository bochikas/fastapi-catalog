from sqlalchemy import and_, select

from db.models import Product, ProductProperty, Property, PropertyType
from schemas.product import ProductPropertyIntSchema, ProductPropertyListSchema, ProductResponseSchema
from schemas.property import PropertyIntResponseSchema, PropertyListResponseSchema


async def product_to_schema(product: Product) -> ProductResponseSchema:
    """Приведение модели к нужной схеме."""

    props = []
    for pp in product.properties:
        if pp.property.type is PropertyType.INT:
            props.append(ProductPropertyIntSchema(uid=pp.property.uid, name=pp.property.name, value=pp.int_value))
        else:
            props.append(
                ProductPropertyListSchema(
                    uid=pp.property.uid,
                    name=pp.property.name,
                    value_uid=pp.value_uid,
                    value=pp.value.value if pp.value else None,
                )
            )
    return ProductResponseSchema(uid=product.uid, name=product.name, properties=props)


async def property_to_schema(prop: Property) -> PropertyIntResponseSchema | PropertyListResponseSchema:
    """Приведение модели к нужной схеме."""

    if prop.type is PropertyType.INT:
        return PropertyIntResponseSchema.model_validate(prop)
    return PropertyListResponseSchema.model_validate(prop)


def prepare_filter_query(name: str, filters: dict):
    """Подготовка запроса для фильтрации продуктов.

    Возможно фильтрация по значению свойства, например, товары с id свойства c2dd7db0-690c-460c-8e4a-8d0cd54e0d7b и
    значением от 10 до 15.
    property_c2dd7db0-690c-460c-8e4a-8d0cd54e0d7b_from = 10
    property_c2dd7db0-690c-460c-8e4a-8d0cd54e0d7b_to = 15

    Фильтрация по id значения свойства.
    property_a28c7b6c-1a77-4bf3-b10a-1cc914ba5a61 = 0172a5d5-a6ed-4dae-82fd-0c60d022e4a0
    Товары с привязанным id свойства a28c7b6c-1a77-4bf3-b10a-1cc914ba5a61 и id значения свойства
    0172a5d5-a6ed-4dae-82fd-0c60d022e4a0
    """

    query = select(Product)
    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))

    for key, value in filters.items():
        if key.endswith("_from") or key.endswith("_to"):
            # property_c2dd7db0-690c-460c-8e4a-8d0cd54e0d7b_from = 10
            _, property_uid, filter_type = key.split("_")
            if filter_type == "from":
                query = query.where(
                    Product.properties.any(
                        and_(ProductProperty.property_id == property_uid, ProductProperty.int_value >= int(value))
                    )
                )
            # property_c2dd7db0-690c-460c-8e4a-8d0cd54e0d7b_to = 15
            elif filter_type == "to":
                query = query.where(
                    Product.properties.any(
                        and_(ProductProperty.property_id == property_uid, ProductProperty.int_value <= int(value))
                    )
                )
        else:
            # property_a28c7b6c-1a77-4bf3-b10a-1cc914ba5a61 = 0172a5d5-a6ed-4dae-82fd-0c60d022e4a0
            _, property_uid = key.split("_")
            values = value if isinstance(value, list) else [value]
            query = query.where(
                Product.properties.any(
                    and_(ProductProperty.property_id == property_uid, ProductProperty.value_uid.in_(values))
                )
            )
    return query
