from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ARRAY, UUID, Boolean

import uuid


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(65), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    roles: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    teachers_ids: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID), default=list)


class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    students_ids: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID), default=list)
    groups_ids: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID), default=list)
