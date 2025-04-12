from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base, PropertyType


class Property(Base):
    """Свойство товара."""

    __tablename__ = "properties"

    name: Mapped[str | None]
    type: Mapped[PropertyType]

    values = relationship("PropertyValue", back_populates="property", cascade="all, delete-orphan", lazy="selectin")


class PropertyValue(Base):
    """Значение свойства товара."""

    __tablename__ = "property_values"

    value: Mapped[str]
    property_id: Mapped[UUID] = mapped_column(ForeignKey("properties.uid"))
    property = relationship("Property", back_populates="values")


class Product(Base):
    """Товар."""

    name: Mapped[str]
    properties = relationship(
        "ProductProperty", back_populates="product", cascade="all, delete-orphan", lazy="selectin"
    )


class ProductProperty(Base):
    """Свойства товара."""

    __tablename__ = "product_properties"

    int_value: Mapped[int | None]

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.uid"))
    property_id: Mapped[UUID] = mapped_column(ForeignKey("properties.uid"))
    value_uid: Mapped[UUID] = mapped_column(ForeignKey("property_values.uid"), nullable=True)

    product = relationship("Product", back_populates="properties", lazy="selectin")
    property = relationship("Property", lazy="selectin")
    value = relationship("PropertyValue", lazy="selectin")
