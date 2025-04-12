from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.datastructures import QueryParams

from crud.catalog import get_filter_statistics, get_filtered_products
from dependencies.db import get_db
from schemas.catalog import CatalogFilterResponseSchema, CatalogResponseSchema, SortType

router = APIRouter()


def _prepare_filters(allowed_params: set, query_params: QueryParams):
    filters = {}

    for key in query_params:
        if key not in allowed_params and not key.startswith("property_"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid query parameter: {key}")
        if key not in allowed_params:
            values = query_params.getlist(key)
            filters[key] = values if len(values) > 1 else values[0]
    return filters


@router.get("/catalog/", status_code=status.HTTP_200_OK, response_model=CatalogResponseSchema)
async def catalog(
    request: Request,
    name: str | None = None,
    sort: SortType = SortType.UID,
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
) -> CatalogResponseSchema:
    """Каталог товара."""

    allowed_params = {"name", "sort", "page", "page_size"}
    filters = _prepare_filters(allowed_params, request.query_params)

    return await get_filtered_products(db, name, sort, page, page_size, filters)


@router.get("/catalog/filter/", status_code=status.HTTP_200_OK, response_model=CatalogFilterResponseSchema)
async def catalog_filter(
    request: Request,
    name: str | None = None,
    sort: SortType = SortType.UID,
    db: AsyncSession = Depends(get_db),
):
    """Каталог товара с фильтром."""

    allowed_params = {"name", "sort"}
    filters = _prepare_filters(allowed_params, request.query_params)

    return await get_filter_statistics(db, name, sort, filters)
