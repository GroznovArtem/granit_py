from fastapi import APIRouter

from app.api.routers.user import user_router

main_router = APIRouter()

main_router.include_router(user_router, prefix="/user", tags=["user"])
