import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db

from app.api.schemas.user import ShowUser, CreateUserResponse, CreateUserRequest, GetUserResponse, DeleteUserResponse, UpdateUserResponse, UpdateUserRequest
from app.core.user import create_new_user, get_user_by_id, delete_user_by_id, update_user_by_id

from fastapi.exceptions import HTTPException

user_router = APIRouter()


@user_router.post("/", response_model=CreateUserResponse)
def create_user(body: CreateUserRequest, db: Session = Depends(get_db)) -> CreateUserResponse:
    user = create_new_user(db, params=body)

    if not user:
        raise HTTPException(status_code=400, detail="Unknown error")

    return user


@user_router.get("/{user_id}", response_model=GetUserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> GetUserResponse:
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")

    return user


@user_router.delete("/{user_id}", response_model=DeleteUserResponse)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = delete_user_by_id(db, user_id)

    if not deleted_user_id.user_id:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")

    return deleted_user_id


@user_router.patch("/{user_id}", response_model=UpdateUserResponse)
def update_user(user_id: uuid.UUID, body: UpdateUserRequest, db: Session = Depends(get_db)) -> UpdateUserResponse:
    if not body.name or not body.surname or not body.email:
        raise HTTPException(status_code=400, detail="All fields must be filled in.")

    updated_user = update_user_by_id(db, user_id=user_id, params=body)

    if not updated_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")

    return updated_user
