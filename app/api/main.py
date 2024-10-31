from fastapi import APIRouter

from app.api.routers.user import user_router
from app.api.routers.authorization import login_router
from app.api.routers.teacher import teacher_router
from app.api.routers.student import student_router

main_router = APIRouter()

main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(login_router, prefix="/login", tags=["login"])
main_router.include_router(teacher_router, prefix="/teacher", tags=["teacher"])
main_router.include_router(student_router, prefix="/student", tags=["student"])
