from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Attribute(Base):
    __tablename__ = "attributes"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)

    products = relationship("Product", secondary="products_attributes", back_populates="attributes")