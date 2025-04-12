import os
import time
import uuid
from enum import StrEnum

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


def uuidv7() -> uuid.UUID:
    """Generate a UUIDv7."""

    # random bytes
    value = bytearray(os.urandom(16))

    # current timestamp in ms
    timestamp = int(time.time() * 1000)

    # timestamp
    value[0] = (timestamp >> 40) & 0xFF
    value[1] = (timestamp >> 32) & 0xFF
    value[2] = (timestamp >> 24) & 0xFF
    value[3] = (timestamp >> 16) & 0xFF
    value[4] = (timestamp >> 8) & 0xFF
    value[5] = timestamp & 0xFF

    # version and variant
    value[6] = (value[6] & 0x0F) | 0x70  # noqa WPS339
    value[8] = (value[8] & 0x3F) | 0x80

    return uuid.UUID(bytes=bytes(value))


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    uid: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuidv7)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa N805
        return f"{cls.__name__.lower()}s"


class PropertyType(StrEnum):
    LIST = "list"
    INT = "int"
