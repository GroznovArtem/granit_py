from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException

from app.api.schemas.user import ShowUser, CreateUserRequest, CreateUserResponse, GetUserResponse, DeleteUserResponse, \
    UpdateUserRequest, UpdateUserResponse
from app.repository.user import UserRepository

import uuid


def create_new_user(db: Session, params: CreateUserRequest) -> CreateUserResponse:
    user_repo = UserRepository(db)

    try:
        user = user_repo.create_user(name=params.name, surname=params.surname, email=params.email, hashed_password=params.hashed_password)
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
    try:
        deleted_user_id = user_repo.delete_user_by_id(user_id)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return DeleteUserResponse(
        user_id=deleted_user_id
    )


def update_user_by_id(db: Session, user_id: uuid.UUID, params: UpdateUserRequest) -> UpdateUserResponse | None:
    user_repo = UserRepository(db)
    try:
        updated_user = user_repo.update_user_by_id(user_id=user_id, name=params.name, surname=params.surname, email=params.email)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_user:
        return UpdateUserResponse(
            user_id=updated_user["user_id"],
            name=updated_user["name"],
            surname=updated_user["surname"],
            email=updated_user["email"],
        )