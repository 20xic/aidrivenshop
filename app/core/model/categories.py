from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        ForeignKey("categories.id"), 
        nullable=True
    )
    
    # Self-referential relationship
    parent = relationship("Category", remote_side="Category.id", backref="subcategories")
    
    # Используем строки для отложенного импорта
    products = relationship("Product", back_populates="category")