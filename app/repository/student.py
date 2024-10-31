import uuid

from sqlalchemy.orm import Session

from app.db.models.users import User, Student

from typing import List, Type


class StudentRepository:
    def __init__(self, db: Session):
        self._db = db

    def create_user_by_id(self, user_id: uuid.UUID) -> Student | None:
        user = self._db.query(User).filter(User.user_id == user_id).first()

        if user:
            student = Student(user_id=user.user_id)
            self._db.add(student)
            self._db.commit()
            self._db.flush()

            return student

    def get_students(self) -> List[Type[Student]] | None:
        students = self._db.query(Student).all()

        if students:
            return students

    def delete_student_by_id(self, student_id: uuid.UUID) -> Type[Student] | None:
        student = self._db.query(Student).filter(Student.student_id == student_id).first()

        if student:
            self._db.delete(student)
            self._db.commit()
            self._db.flush()

            return student