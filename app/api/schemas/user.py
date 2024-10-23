from pydantic import BaseModel
from uuid import UUID
from typing import List
from app.api.schemas.portal_role import UserPortalRoles

from typing import List


class ShowUser(BaseModel):
    name: str
    surname: str
    email: str


class GetUser(BaseModel):
    user_id: UUID
    name: str
    surname: str
    email: str
    is_active: bool


class GetUserResponse(BaseModel):
    user_id: UUID
    name: str
    surname: str
    email: str
    hashed_password: str
    is_active: bool
    roles: List[UserPortalRoles]


class CreateUserResponse(BaseModel):
    name: str
    surname: str
    email: str


class CreateUserRequest(BaseModel):
    name: str
    surname: str
    email: str
    hashed_password: str


class DeleteUserResponse(BaseModel):
    user_id: UUID | None


class UpdateUserRequest(BaseModel):
    name: str | None
    surname: str | None
    email: str | None


class UpdateUserResponse(BaseModel):
    user_id: UUID
    name: str
    surname: str
    email: str


class AssignAdminRoleResponse(BaseModel):
    name: str
    surname: str
    email: str
    roles: List[UserPortalRoles]


class ShowUsersResponse(BaseModel):
    users: List[GetUser]
