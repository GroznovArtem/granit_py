from sqlalchemy.orm import Session

from app.api.schemas.teacher import (
    CreateTeacherResponse,
    GetTeachersResponse,
    ShowTeacher,
)
from app.repository.teacher import TeacherRepository

import uuid


def create_teacher_by_user_id(
    db: Session, user_id: uuid.UUID
) -> CreateTeacherResponse | None:
    teacher_repo = TeacherRepository(db)

    teacher = teacher_repo.create_teacher_by_id(user_id=user_id)

    if teacher:
        return CreateTeacherResponse(
            user_id=teacher.user_id, teacher_id=teacher.teacher_id
        )


def get_all_teachers(db: Session) -> GetTeachersResponse | None:
    teacher_repo = TeacherRepository(db)

    teachers = teacher_repo.get_teachers()

    if teachers:
        return GetTeachersResponse(
            teachers=[
                ShowTeacher(
                    user_id=teacher.user_id,
                    teacher_id=teacher.teacher_id,
                    students_ids=teacher.students_ids,
                    groups_ids=teacher.groups_ids,
                )
                for teacher in teachers
            ]
        )
