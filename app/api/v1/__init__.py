from fastapi import APIRouter
from .category.endpoints import router as category_router

router = APIRouter(prefix="/v1")
router.include_router(category_router, prefix="/categories", tags=["categories"])