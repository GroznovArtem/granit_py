from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.api.schemas.student import (
    GetStudentsResponse,
    CreateStudentResponse,
    CreateStudentRequest,
    DeleteStudentResponse,
)
from app.core.student import (
    create_student_by_id,
    get_all_students,
    delete_student_by_id,
)

from fastapi.exceptions import HTTPException

import uuid


student_router = APIRouter()


@student_router.post("/")
def create_student(
    data: CreateStudentRequest, db: Session = Depends(get_db)
) -> CreateStudentResponse:
    student = create_student_by_id(db, user_id=data.user_id)

    if not student:
        raise HTTPException(status_code=400, detail="Unbound error.")

    return student


@student_router.get("/")
def get_students(db: Session = Depends(get_db)) -> GetStudentsResponse:
    students = get_all_students(db)

    if not students:
        raise HTTPException(status_code=404, detail="Students not found.")

    return students


@student_router.delete("/{student_id}")
def delete_student(
    student_id: uuid.UUID, db: Session = Depends(get_db)
) -> DeleteStudentResponse:
    deleted_student_id = delete_student_by_id(db, student_id=student_id)

    if not deleted_student_id:
        raise HTTPException(status_code=404, detail="Student not found.")

    return deleted_student_id
