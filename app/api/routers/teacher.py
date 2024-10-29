from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.api.schemas.teacher import (
    CreateTeacherRequest,
    CreateTeacherResponse,
    GetTeachersResponse,
)
from app.core.teacher import (
    create_teacher_by_user_id,
    get_all_teachers,
)

from fastapi.exceptions import HTTPException

teacher_router = APIRouter()


@teacher_router.get("/")
def get_teachers(db: Session = Depends(get_db)) -> GetTeachersResponse:
    teachers = get_all_teachers(db)

    if not teachers:
        raise HTTPException(status_code=404, detail="Teachers not found.")

    return teachers


@teacher_router.post("/")
def create_teacher(
    data: CreateTeacherRequest, db: Session = Depends(get_db)
) -> CreateTeacherResponse:
    teacher = create_teacher_by_user_id(db, user_id=data.user_id)

    if not teacher:
        raise HTTPException(status_code=400, detail="Unbound error.")

    return teacher
