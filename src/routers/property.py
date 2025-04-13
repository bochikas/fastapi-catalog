from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.property import create_property, delete_property
from dependencies.db import get_db
from schemas.property import PropertyCreateSchema, PropertyResponseSchema

router = APIRouter(prefix="/properties", tags=["Property"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PropertyResponseSchema)
async def create(data: PropertyCreateSchema, db: AsyncSession = Depends(get_db)):
    """Создание свойства."""

    return await create_property(data, db)


@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(uid: UUID, db: AsyncSession = Depends(get_db)):
    """Удаление свойства."""

    await delete_property(uid, db)
