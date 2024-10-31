from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.api.schemas.teacher import (
    CreateTeacherRequest,
    CreateTeacherResponse,
    GetTeachersResponse,
    DeleteTeacherResponse,
)
from app.core.teacher import (
    create_teacher_by_user_id,
    get_all_teachers,
    delete_teacher_by_id,
)

from fastapi.exceptions import HTTPException

import uuid

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


@teacher_router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: uuid.UUID, db: Session = Depends(get_db)
) -> DeleteTeacherResponse:
    deleted_teacher_id = delete_teacher_by_id(db, teacher_id=teacher_id)

    if not deleted_teacher_id:
        raise HTTPException(status_code=404, detail="Teacher not found.")

    return deleted_teacher_id
