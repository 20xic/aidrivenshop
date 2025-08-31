from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from uuid import UUID
from core.model import Category
from .base import CRUDBase
from typing import Optional

class CRUDCategory(CRUDBase[Category]):
    async def get_by_slug(
        self, 
        db: AsyncSession, 
        *, 
        slug: str
    ) -> Optional[Category]:
        result = await db.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Category,
        obj_in: dict
    ) -> Category:
        if obj_in.get("parent_id") == "":
            obj_in["parent_id"] = None
            
        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

category_crud = CRUDCategory(Category)