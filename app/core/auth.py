from sqlalchemy.orm import Session
from app.services.hashing import Hasher
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose import jwt
from jose import JWTError
from app.db.models.users import User
from app.db.session import get_db

from app.repository.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
SECRET_KEY = "yN9uNSmIkP8dyb9cIUwQFd8u-tuqiBnvh2riD5W0BZM"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


def _get_user_by_email_for_auth(email: str, db: Session) -> User | None:
    with db.begin():
        user_repo = UserRepository(db)
        return user_repo.get_user_by_email(
            email=email,
        )


def authenticate_user(email: str, password: str, db: Session) -> User | None:
    user = _get_user_by_email_for_auth(email=email, db=db)
    if user is None:
        return None
    if not Hasher.verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = _get_user_by_email_for_auth(email, db)
    if user is None:
        raise credentials_exception

    return user
