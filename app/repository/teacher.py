import uuid

from sqlalchemy.orm import Session

from app.db.models.users import User, Teacher

from typing import List, Type


class TeacherRepository:
    def __init__(self, db: Session):
        self._db = db

    def create_teacher_by_id(self, user_id: uuid.UUID) -> Teacher | None:
        user = self._db.query(User).filter(User.user_id == user_id).first()

        if user:
            teacher = Teacher(user_id=user_id)
            self._db.add(teacher)
            self._db.commit()
            self._db.flush()

            return teacher

    def get_teachers(self) -> List[Type[Teacher]] | None:
        teachers = self._db.query(Teacher).all()

        if teachers:
            return teachers
