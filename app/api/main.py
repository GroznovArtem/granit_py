from fastapi import APIRouter

from app.api.routers.user import user_router
from app.api.routers.authorization import login_router

main_router = APIRouter()

main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(login_router, prefix="/login", tags=["login"])
