from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.api.schemas.auth import Token
from app.services.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.core.auth import authenticate_user

from app.db.session import get_db

login_router = APIRouter()

SECRET_KEY = "yN9uNSmIkP8dyb9cIUwQFd8u-tuqiBnvh2riD5W0BZM"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


@login_router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )

    # return {"access_token": access_token, "token_type": "bearer"}
    return Token(access_token=access_token, token_type="bearer")
