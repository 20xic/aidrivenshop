from pydantic import BaseModel, UUID4, field_validator
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: str
    parent_id: Optional[UUID4] = None

    @field_validator('parent_id', mode='before')
    @classmethod
    def validate_parent_id(cls, v):
        if v == "":
            return None
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[UUID4] = None

    @field_validator('parent_id', mode='before')
    @classmethod
    def validate_parent_id(cls, v):
        if v == "":
            return None
        return v

class CategoryInDB(CategoryBase):
    id: UUID4
    image: Optional[UUID4] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryPublic(CategoryInDB):
    pass