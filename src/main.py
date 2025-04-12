from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import engine
from db.models import Base
from db.seed_db import seed_db
from routers.catalog import router as catalog_router
from routers.product import router as product_router
from routers.property import router as property_router


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    await seed_db()

    yield
    await drop_db()


app = FastAPI(title="Product Catalog API", lifespan=lifespan)

app.include_router(catalog_router, tags=["catalog"])
app.include_router(product_router, tags=["product"])
app.include_router(property_router, tags=["property"])
