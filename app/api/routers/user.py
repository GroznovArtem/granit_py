import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.portal_role import UserPortalRoles
from app.db.session import get_db
from app.core.auth import get_current_user_from_token
from app.db.models.users import User

from app.api.schemas.user import (
    CreateUserResponse,
    CreateUserRequest,
    GetUserResponse,
    DeleteUserResponse,
    UpdateUserResponse,
    UpdateUserRequest,
    AssignAdminRoleResponse,
    ShowUsersResponse,
)
from app.core.user import (
    create_new_user,
    get_user_by_id,
    delete_user_by_id,
    update_user_by_id,
    assign_user_role,
    revoke_user_role,
    get_all_users,
)

from fastapi.exceptions import HTTPException

user_router = APIRouter()


# @user_router.get("/get_teachers")
# def get_teachers(db: Session = Depends(get_db)) -> GetTeachersResponse:
#     teachers = get_all_teachers(db)
#
#     if not teachers:
#         raise HTTPException(
#             status_code=404, detail="Teachers not found."
#         )
#
#     return teachers


@user_router.post("/", response_model=CreateUserResponse)
def create_user(
    body: CreateUserRequest, db: Session = Depends(get_db)
) -> CreateUserResponse:
    user = create_new_user(db, params=body)

    if not user:
        raise HTTPException(status_code=400, detail="Unknown error")

    return user


@user_router.get("/{user_id}", response_model=GetUserResponse)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> GetUserResponse:
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    return user


@user_router.delete("/{user_id}", response_model=DeleteUserResponse)
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> DeleteUserResponse:
    deleted_user_id = delete_user_by_id(db, user_id)

    if not deleted_user_id.user_id:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    return deleted_user_id


@user_router.patch("/{user_id}", response_model=UpdateUserResponse)
def update_user(
    user_id: uuid.UUID,
    body: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdateUserResponse:
    if not body.name or not body.surname or not body.email:
        raise HTTPException(status_code=400, detail="All fields must be filled in.")

    updated_user = update_user_by_id(db, user_id=user_id, params=body)

    if not updated_user:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    return updated_user


@user_router.patch("assign_role/", response_model=AssignAdminRoleResponse)
def assign_admin_role(to_user: uuid.UUID, role: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AssignAdminRoleResponse:
    if UserPortalRoles.ROLE_SUPER_ADMIN not in current_user.roles:
        raise HTTPException(status_code=409, detail="Forbidden.")

    # if role == "ADMIN":
    role_to_assign = UserPortalRoles.ROLE_ADMIN

    if role == "SUPER_ADMIN":
        role_to_assign = UserPortalRoles.ROLE_SUPER_ADMIN

    assigned_user = assign_user_role(db=db, from_user=current_user, to_user_id=to_user, role=role_to_assign)

    if not assigned_user:
        raise HTTPException(status_code=404, detail=f"User with id {to_user} not found.")

    return assigned_user


@user_router.patch("revoke_role/", response_model=AssignAdminRoleResponse)
def revoke_admin_role(to_user: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AssignAdminRoleResponse:
    revoked_user = revoke_user_role(db=db, from_user=current_user, to_user_id=to_user, role=UserPortalRoles.ROLE_ADMIN)

    if not revoked_user:
        raise HTTPException(status_code=404, detail=f"User with id {to_user} not found.")

    return revoked_user


@user_router.get("/")
def get_users(db: Session = Depends(get_db)) -> ShowUsersResponse:
    users = get_all_users(db)

    if not users:
        raise HTTPException(
            status_code=404, detail=f"Users not found."
        )

    return users


# @user_router.post("/create_teacher")
# def create_teacher(data: CreateTeacherRequest, db: Session = Depends(get_db)) -> CreateTeacherResponse:
#     teacher = create_teacher_by_user_id(db, user_id=data.user_id)
#
#     if not teacher:
#         raise HTTPException(
#             status_code=400, detail="Unbound error."
#         )
#
#     return teacher
