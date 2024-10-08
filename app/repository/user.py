import uuid

from sqlalchemy.orm import Session
from app.db.models.users import User


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def create_user(
        self, name: str, surname: str, email: str, hashed_password: str
    ) -> User:
        user = User(
            name=name, surname=surname, email=email, hashed_password=hashed_password
        )

        self._db.add(user)
        self._db.commit()
        self._db.flush()

        return user

    def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        user = self._db.query(User).filter(User.user_id == user_id).first()

        return user

    def delete_user_by_id(self, user_id: uuid.UUID) -> uuid.UUID | None:
        user = self._db.query(User).filter(User.user_id == user_id).first()

        if user:
            user.is_active = False
            self._db.commit()
            self._db.flush()

            return user.user_id

    def update_user_by_id(
        self, user_id: uuid.UUID, name: str, surname: str, email: str
    ) -> dict[str, str | uuid.UUID] | None:
        user = self._db.query(User).filter(User.user_id == user_id).first()

        if user:
            user.name = name
            user.surname = surname
            user.email = email

            self._db.commit()
            self._db.flush()

            return {
                "user_id": user.user_id,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
            }
