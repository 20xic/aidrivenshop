from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional, List

from core.model import db_helper
from core.schemas.category import CategoryCreate, CategoryUpdate, CategoryPublic
from service.category import category_service

router = APIRouter()

@router.post("/", response_model=CategoryPublic, status_code=status.HTTP_201_CREATED)
async def create_category(
    *,
    db: AsyncSession = Depends(db_helper.session_getter),
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(...),
    parent_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    # Преобразуем пустую строку в None для parent_id
    if parent_id == "":
        parent_id = None
    
    # Если parent_id не None, пытаемся преобразовать в UUID
    if parent_id is not None:
        try:
            parent_id = UUID(parent_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parent_id format. Must be a valid UUID."
            )

    category_in = CategoryCreate(
        name=name,
        slug=slug,
        description=description,
        parent_id=parent_id
    )
    
    return await category_service.create_category(
        db, category_in=category_in, image_file=image
    )

@router.get("/{category_id}", response_model=CategoryPublic)
async def get_category(
    category_id: UUID,
    db: AsyncSession = Depends(db_helper.session_getter)
):
    # Используем сервис вместо прямого доступа к CRUD
    category = await category_service.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    return category

@router.get("/", response_model=List[CategoryPublic])
async def get_categories(
    db: AsyncSession = Depends(db_helper.session_getter),
    skip: int = 0,
    limit: int = 100
):
    # Используем сервис вместо прямого доступа к CRUD
    return await category_service.get_categories(db, skip=skip, limit=limit)

@router.put("/{category_id}", response_model=CategoryPublic)
async def update_category(
    category_id: UUID,
    *,
    db: AsyncSession = Depends(db_helper.session_getter),
    name: Optional[str] = Form(None),
    slug: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    parent_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    # Преобразуем пустую строку в None для parent_id
    if parent_id == "":
        parent_id = None
    
    # Если parent_id не None, пытаемся преобразовать в UUID
    if parent_id is not None:
        try:
            parent_id = UUID(parent_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parent_id format. Must be a valid UUID."
            )

    update_data = CategoryUpdate(
        name=name,
        slug=slug,
        description=description,
        parent_id=parent_id
    )
    
    return await category_service.update_category(
        db,
        category_id=category_id,
        category_in=update_data,
        image_file=image
    )

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(db_helper.session_getter)
):
    # Используем сервис вместо прямого доступа к CRUD
    await category_service.delete_category(db, category_id=category_id)
    return {"message": "Category deleted successfully"}