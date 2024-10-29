from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from app.db.models.users import User

from app.api.schemas.portal_role import UserPortalRoles
from app.api.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserResponse,
    DeleteUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    AssignAdminRoleResponse,
    ShowUsersResponse,
    GetUser,
)
from app.repository.user import UserRepository

import uuid


def create_new_user(db: Session, params: CreateUserRequest) -> CreateUserResponse:
    user_repo = UserRepository(db)

    try:
        user = user_repo.create_user(
            name=params.name,
            surname=params.surname,
            email=params.email,
            hashed_password=params.hashed_password,
        )
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return CreateUserResponse(
        name=user.name,
        surname=user.surname,
        email=user.email,
    )


def get_user_by_id(db: Session, user_id: uuid.UUID) -> GetUserResponse | None:
    user_repo = UserRepository(db)
    try:
        user = user_repo.get_user_by_id(user_id=user_id)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if user:
        return GetUserResponse(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            roles=user.roles,
        )


def delete_user_by_id(db: Session, user_id: uuid.UUID) -> DeleteUserResponse | None:
    user_repo = UserRepository(db)
    deleted_user_id = None
    try:
        deleted_user_id = user_repo.delete_user_by_id(user_id)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not deleted_user_id:
        raise HTTPException(status_code=402, detail="User not found")

    return DeleteUserResponse(user_id=deleted_user_id)


def update_user_by_id(
    db: Session, user_id: uuid.UUID, params: UpdateUserRequest
) -> UpdateUserResponse | None:
    user_repo = UserRepository(db)
    try:
        updated_user = user_repo.update_user_by_id(
            user_id=user_id,
            name=params.name,
            surname=params.surname,
            email=params.email,
        )
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_user:
        return UpdateUserResponse(
            user_id=updated_user["user_id"],
            name=updated_user["name"],
            surname=updated_user["surname"],
            email=updated_user["email"],
        )


def assign_user_role(
    db: Session, from_user: User, to_user_id: uuid.UUID, role: UserPortalRoles
) -> AssignAdminRoleResponse | None:
    user_repo = UserRepository(db)

    assigned_user = user_repo.assign_user_role(to_user_id, role)

    if assigned_user:
        return AssignAdminRoleResponse(
            name=assigned_user["name"],
            surname=assigned_user["surname"],
            email=assigned_user["email"],
            roles=assigned_user["roles"],
        )


def revoke_user_role(
    db: Session, from_user: User, to_user_id: uuid.UUID, role: UserPortalRoles
) -> AssignAdminRoleResponse | None:
    user_repo = UserRepository(db)

    assigned_user = user_repo.revoke_user_role(to_user_id, role)

    if assigned_user:
        return AssignAdminRoleResponse(
            name=assigned_user["name"],
            surname=assigned_user["surname"],
            email=assigned_user["email"],
            roles=assigned_user["roles"],
        )


def get_all_users(db: Session):
    user_repo = UserRepository(db)

    users = user_repo.get_users()

    if users:
        return ShowUsersResponse(
            users=[
                GetUser(
                    user_id=user.user_id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    is_active=user.is_active,
                )
                for user in users
            ]
        )


#
# def create_teacher_by_user_id(db: Session, user_id: uuid.UUID) -> CreateTeacherResponse | None:
#     teacher_repo = TeacherRepository(db)
#
#     teacher = teacher_repo.create_teacher_by_id(user_id=user_id)
#
#     if teacher:
#         return CreateTeacherResponse(user_id=teacher.user_id, teacher_id=teacher.teacher_id)
#
#
# def get_all_teachers(db: Session) -> GetTeachersResponse | None:
#     teacher_repo = TeacherRepository(db)
#
#     teachers = teacher_repo.get_teachers()
#
#     if teachers:
#         return GetTeachersResponse(
#             teachers=[ShowTeacher(user_id=teacher.user_id, teacher_id=teacher.user_id, students_ids=teacher.students_ids, groups_ids=teacher.groups_ids) for teacher in teachers]
#         )
