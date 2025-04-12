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

        for p in property_map.values():
            prop = Property(uid=p["uid"], type=p["type"])
            if p["type"] is PropertyType.list:
                for val_uid, val_value in p["values"].items():
                    prop.values.append(PropertyValue(uid=val_uid, value=val_value))
            elif p["type"] is PropertyType.int:
                prop.int_value = p["value"]
            db.add(prop)
        await db.commit()

        for product in data["products"]:
            new_product = Product(uid=product["uid"], name=product.get("name"))
            for pp in product["properties"]:
                product_property = ProductProperty(property_id=pp["uid"])
                if "value_uid" in p:
                    product_property.value_uid = pp["value_uid"]
                new_product.properties.append(product_property)
            db.add(new_product)
        await db.commit()
