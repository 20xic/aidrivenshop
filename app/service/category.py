from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException, status
from crud.category import category_crud
from core.schemas.category import CategoryCreate, CategoryUpdate
from core import minio_helper
from core.model import ImageMetadata
from core.model.categories import Category
import uuid
import io

class CategoryService:
    async def create_category(
        self,
        db: AsyncSession,
        *,
        category_in: CategoryCreate,
        image_file: Optional[UploadFile] = None
    ) -> Category:
        try:
            # Проверяем slug на уникальность
            existing = await category_crud.get_by_slug(db, slug=category_in.slug)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category with this slug already exists"
                )

            # Обрабатываем изображение если есть
            image_id = None
            if image_file:
                image_id = await self._save_image(db, image_file)

            # Создаем категорию
            category_data = category_in.model_dump()
            if category_data.get("parent_id") == "":
                category_data["parent_id"] = None
                
            if image_id:
                category_data["image"] = image_id

            category = await category_crud.create(db, obj_in=category_data)
            await db.commit()
            return category
            
        except Exception:
            await db.rollback()
            raise

    async def get_category(
        self, 
        db: AsyncSession, 
        category_id: UUID
    ) -> Optional[Category]:
        return await category_crud.get(db, id=category_id)

    async def get_categories(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Category]:
        return await category_crud.get_multi(db, skip=skip, limit=limit)

    async def update_category(
        self,
        db: AsyncSession,
        *,
        category_id: UUID,
        category_in: CategoryUpdate,
        image_file: Optional[UploadFile] = None
    ) -> Category:
        try:
            category = await category_crud.get(db, id=category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Category not found"
                )

            # Обновляем изображение если есть
            image_id = None
            if image_file:
                image_id = await self._save_image(db, image_file)

            update_data = category_in.model_dump(exclude_unset=True)
            if image_id:
                update_data["image"] = image_id

            category = await category_crud.update(
                db, db_obj=category, obj_in=update_data
            )
            await db.commit()
            return category
            
        except Exception:
            await db.rollback()
            raise

    async def delete_category(
        self, 
        db: AsyncSession, 
        category_id: UUID
    ) -> None:
        try:
            category = await category_crud.get(db, id=category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail="Category not found"
                )
            await category_crud.remove(db, id=category_id)
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    async def _save_image(
        self,
        db: AsyncSession,
        image_file: UploadFile
    ) -> UUID:
        try:
            import io
            
            # Генерируем UUID для имени файла
            file_uuid = uuid.uuid4()
            file_extension = image_file.filename.split('.')[-1] if '.' in image_file.filename else "jpg"
            filename = f"{file_uuid}.{file_extension}"

            # Читаем содержимое файла
            contents = await image_file.read()

            # Сохраняем в MinIO (синхронный вызов без await)
            minio_client = minio_helper.get_client()
            minio_client.put_object(
                bucket_name=minio_helper.bucket_name,
                object_name=filename,
                data=io.BytesIO(contents),
                length=len(contents),
                content_type=image_file.content_type
            )

            # Сохраняем метаданные в БД
            image_metadata = ImageMetadata(
                original_filename=image_file.filename,
                file_size=len(contents),
                content_type=image_file.content_type,
                bucket_name=minio_helper.bucket_name
            )
            db.add(image_metadata)
            await db.commit()
            await db.refresh(image_metadata)

            return image_metadata.id

        except Exception as e:
            if db.in_transaction():
                await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving image: {str(e)}"
            )

category_service = CategoryService()