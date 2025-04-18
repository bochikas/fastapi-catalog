from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.product import create_product, delete_product, get_product
from dependencies.db import get_db
from schemas.product import ProductCreateSchema, ProductResponseSchema

router = APIRouter(prefix="/product", tags=["Product"])


@router.post("/", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
async def create(data: ProductCreateSchema, db: AsyncSession = Depends(get_db)):
    """Создание товара."""

    return await create_product(data, db)


@router.get("/{uid}", response_model=ProductResponseSchema, status_code=status.HTTP_200_OK)
async def get(uid: UUID, db: AsyncSession = Depends(get_db)):
    """Получение товара по UID."""

    return await get_product(uid, db)


@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(uid: UUID, db: AsyncSession = Depends(get_db)):
    """Удаление товара по UID."""

    await delete_product(uid, db)
