from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .base import Base

class ImageMetadata(Base):
    __tablename__ = "images_metadata"

    original_filename: Mapped[str] = mapped_column(String(255))
    file_size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(100))
    upload_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    bucket_name: Mapped[str] = mapped_column(String(255))