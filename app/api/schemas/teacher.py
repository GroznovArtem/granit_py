from pydantic import BaseModel
from uuid import UUID
from typing import List


class CreateTeacherRequest(BaseModel):
    user_id: UUID


class CreateTeacherResponse(BaseModel):
    user_id: UUID
    teacher_id: UUID


class ShowTeacher(BaseModel):
    user_id: UUID
    teacher_id: UUID
    students_ids: List[UUID]
    groups_ids: List[UUID]


class GetTeachersResponse(BaseModel):
    teachers: List[ShowTeacher]
