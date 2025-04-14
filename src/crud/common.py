from sqlalchemy import and_, select

from db.models import Product, ProductProperty, PropertyType
from schemas.product import ProductPropertyIntSchema, ProductPropertyListSchema, ProductResponseSchema


async def product_to_schema(product: Product) -> ProductResponseSchema:
    """Приведение модели к схеме."""

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


def prepare_filter_query(name: str, filters: dict):
    """Подготовка запроса."""

    query = select(Product)
    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))

    for key, value in filters.items():
        if key.endswith("_from") or key.endswith("_to"):
            _, property_uid, filter_type = key.split("_")
            if filter_type == "from":
                query = query.where(
                    Product.properties.any(
                        and_(ProductProperty.property_id == property_uid, ProductProperty.int_value >= int(value))
                    )
                )
            elif filter_type == "to":
                query = query.where(
                    Product.properties.any(
                        and_(ProductProperty.property_id == property_uid, ProductProperty.int_value <= int(value))
                    )
                )
        else:
            values = value if isinstance(value, list) else [value]
            query = query.where(Product.properties.any(ProductProperty.property_id.in_(values)))
    return query
