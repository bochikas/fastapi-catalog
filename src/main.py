import logging

from fastapi import FastAPI
from starlette import status

from config.logging import LOGGING_CONFIG
from db.seed_db import seed_db
from routers.catalog import router as catalog_router
from routers.product import router as product_router
from routers.property import router as property_router

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)


app = FastAPI(title="Product Catalog API")

app.include_router(catalog_router)
app.include_router(product_router)
app.include_router(property_router)


@app.post("/seed-db", status_code=status.HTTP_200_OK, tags=["Common"])
async def root():
    await seed_db()
    return {"message": "DB filled successfully"}
