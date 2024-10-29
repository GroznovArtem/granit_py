from sqlalchemy.orm import Session

from app.api.schemas.student import (
    CreateStudentResponse,
    GetStudentsResponse,
    ShowStudent,
)
from app.repository.student import StudentRepository

import uuid


def create_student_by_id(
    db: Session, user_id: uuid.UUID
) -> CreateStudentResponse | None:
    student_repo = StudentRepository(db)

    student = student_repo.create_user_by_id(user_id=user_id)

    if student:
        return CreateStudentResponse(
            user_id=student.user_id, student_id=student.student_id
        )


def get_all_students(db: Session) -> GetStudentsResponse | None:
    student_repo = StudentRepository(db)

    students = student_repo.get_students()

    if students:
        return GetStudentsResponse(
            students=[
                ShowStudent(
                    user_id=student.user_id,
                    student_id=student.student_id,
                    teachers_ids=student.teachers_ids,
                )
                for student in students
            ]
        )
