from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.common import prepare_filter_query, product_to_schema
from db.models import Product, Property, PropertyType
from schemas.catalog import CatalogFilterResponseSchema, CatalogResponseSchema, SortType


async def get_filtered_products(
    db: AsyncSession, name: str | None, sort: SortType, page: int, page_size: int, filters: dict
) -> CatalogResponseSchema:
    """Фильтрация товара."""

    query = prepare_filter_query(name, filters)
    # кол-во всего
    count_query = select(func.count()).select_from(query.subquery())
    products_count = (await db.execute(count_query)).scalar()
    query = query.order_by(getattr(Product, sort.value)).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    products = result.scalars().unique().all()
    return CatalogResponseSchema(products=[await product_to_schema(p) for p in products], count=products_count)


async def get_filter_statistics(
    db: AsyncSession, name: str | None, sort: SortType, filters: dict
) -> CatalogFilterResponseSchema:
    """Сгруппированная статистика по товарам."""

    query = prepare_filter_query(name, filters)
    result = await db.execute(query.order_by(getattr(Product, sort.value)))
    products = result.scalars().unique().all()
    count = len(products)
    used_property_ids = {pp.property_id for product in products for pp in product.properties}
    used_properties = (await db.execute(select(Property).where(Property.uid.in_(used_property_ids)))).scalars().all()
    stats: CatalogFilterResponseSchema = CatalogFilterResponseSchema(count=count)

    for prop in used_properties:
        if prop.type is PropertyType.LIST:
            stat = {}
            for val in prop.values:
                stat[val.uid] = sum(
                    1
                    for p in products
                    if any(pp.property_id == prop.uid and pp.value_uid == val.uid for pp in p.properties)
                )
            setattr(stats, str(prop.uid), stat)
        else:
            values = [
                pp.int_value
                for p in products
                for pp in p.properties
                if pp.property_id == prop.uid and pp.int_value is not None
            ]
            if values:
                setattr(stats, str(prop.uid), {"min_value": min(values), "max_value": max(values)})

    return stats
