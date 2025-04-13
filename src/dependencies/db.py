import logging
from typing import AsyncGenerator

from db.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.exception("Unexpected error in database session")
            raise
        finally:
            logger.debug("Database session closed")
            await session.close()
