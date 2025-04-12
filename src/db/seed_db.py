import json

from config.settings import BASE_DIR
from db.base import PropertyType
from db.database import AsyncSessionLocal
from db.models import Product, ProductProperty, Property, PropertyValue


async def seed_db():  # noqa C901
    """Наполнение базы тестовыми данными."""

    async with AsyncSessionLocal() as db:
        with open(f"{BASE_DIR}/test_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Сначала разбиваем по свойствам
        property_map = {}
        for product in data["products"]:
            for prop in product["properties"]:
                uid = prop["uid"]
                if uid not in property_map:
                    property_map[uid] = {"uid": uid, "values": {}}
                if "value_uid" in prop:
                    property_map[uid]["type"] = PropertyType.list
                    property_map[uid]["values"][prop["value_uid"]] = prop["value"]
                else:
                    property_map[uid]["type"] = PropertyType.int
                    property_map[uid]["value"] = prop["value"]
        # Сохраняем свойства
        for p in property_map.values():
            new_property = Property(uid=p["uid"], type=p["type"])
            if p["type"] is PropertyType.list:
                for val_uid, val_value in p["values"].items():
                    new_property.values.append(PropertyValue(uid=val_uid, value=val_value))
            db.add(new_property)
        await db.commit()

        # И уже потом сохраняем товары
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
