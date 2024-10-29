from pydantic import BaseModel
from uuid import UUID
from typing import List


class ShowStudent(BaseModel):
    user_id: UUID
    student_id: UUID
    teachers_ids: List[UUID]


class GetStudentsResponse(BaseModel):
    students: List[ShowStudent]


class CreateStudentRequest(BaseModel):
    user_id: UUID


class CreateStudentResponse(BaseModel):
    user_id: UUID
    student_id: UUID
