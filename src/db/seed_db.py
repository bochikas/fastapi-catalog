import json
import logging

from fastapi import HTTPException
from starlette import status

from config.settings import BASE_DIR
from db.base import PropertyType
from db.database import AsyncSessionLocal
from db.models import Product, ProductProperty, Property, PropertyValue

logger = logging.getLogger(__name__)


async def seed_db():  # noqa C901
    """Наполнение базы тестовыми данными."""

    try:
        async with AsyncSessionLocal() as db:
            with open(f"{BASE_DIR}/test_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            # Сначала сохраняем свойства
            for prop in data["properties"]:
                new_property = Property(uid=prop["uid"], name=prop["name"], type=PropertyType.INT)
                if property_values := prop.get("values"):
                    new_property.type = PropertyType.LIST
                    for property_value in property_values:
                        new_property_value = PropertyValue()
                        for key, value in property_value.items():
                            setattr(new_property_value, key, value)
                        new_property.values.append(new_property_value)
                db.add(new_property)

            # Сохраняем товары
            for product in data["products"]:
                new_product = Product(uid=product["uid"], name=product.get("name"))
                for pp in product["properties"]:
                    product_property = ProductProperty(property_id=pp["uid"])
                    if "value_uid" in pp:
                        product_property.value_uid = pp["value_uid"]
                    else:
                        product_property.int_value = pp["value"]
                    new_product.properties.append(product_property)
                db.add(new_product)

            await db.commit()
    except Exception:
        logger.exception("Filling DB error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filling DB error")  # noqa B904
