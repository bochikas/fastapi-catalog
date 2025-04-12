from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.settings import app_config

engine = create_async_engine(app_config.database_uri, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
