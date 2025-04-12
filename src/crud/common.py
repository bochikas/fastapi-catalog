from db.models import Product, PropertyType
from schemas.product import ProductPropertyIntSchema, ProductPropertyListSchema, ProductSchema


async def product_to_schema(product: Product) -> ProductSchema:
    """Приведение модели к схеме."""

    props = []
    for pp in product.properties:
        if pp.property.type is PropertyType.int:
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
    return ProductSchema(uid=product.uid, name=product.name, properties=props)
