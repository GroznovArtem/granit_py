import uuid

import pytest

from sqlalchemy.orm import Session
from app.db.models.users import Teacher


@pytest.fixture
def user_params():
    return {
        "user_id": str(uuid.uuid4()),
        "name": "Artem",
        "surname": "Groznov",
        "email": "a.g@ya.ru",
        "hashed_password": "fhntv33",
        "is_active": True,
        "roles": [],
    }


@pytest.fixture
def create_teacher():
    def wrapper(user_id: uuid.UUID, session: Session):
        teacher = Teacher(user_id=user_id)
        with session as db:
            db.add(teacher)
            db.commit()
            db.flush()

        return teacher.teacher_id

    return wrapper


def test_create_teacher(db, create_user_in_db, user_params, client):
    create_user_in_db(**user_params, session=db)

    response = client.post("/teacher", json={"user_id": user_params["user_id"]})

    assert response.status_code == 200
    assert response.json()["user_id"] == user_params["user_id"]

    teacher = (
        db.query(Teacher).filter(Teacher.user_id == user_params["user_id"]).first()
    )

    assert teacher is not None


def test_create_teacher_if_user_not_found(db, create_user_in_db, user_params, client):
    response = client.post("/teacher", json={"user_id": user_params["user_id"]})

    assert response.status_code == 400
    assert response.json() == {"detail": "Unbound error."}

    teacher = db.query(Teacher).first()

    assert teacher is None


def test_get_teachers(db, create_user_in_db, create_teacher, user_params, client):
    user1 = {
        "user_id": str(uuid.uuid4()),
        "name": "test1",
        "surname": "test1",
        "email": "test1@ya.ru",
        "hashed_password": "test1",
        "is_active": True,
        "roles": [],
    }
    user2 = {
        "user_id": str(uuid.uuid4()),
        "name": "test2",
        "surname": "test2",
        "email": "test2@ya.ru",
        "hashed_password": "test2",
        "is_active": True,
        "roles": [],
    }
    user3 = {
        "user_id": str(uuid.uuid4()),
        "name": "test3",
        "surname": "test3",
        "email": "test3@ya.ru",
        "hashed_password": "test3",
        "is_active": True,
        "roles": [],
    }

    create_user_in_db(**user1, session=db)
    create_user_in_db(**user2, session=db)
    create_user_in_db(**user3, session=db)

    teacher_id1 = create_teacher(uuid.UUID(user1["user_id"]), session=db)
    teacher_id2 = create_teacher(uuid.UUID(user2["user_id"]), session=db)
    teacher_id3 = create_teacher(uuid.UUID(user3["user_id"]), session=db)

    response = client.get("/teacher")

    assert response.status_code == 200
    assert response.json() == {
        "teachers": [
            {
                "user_id": str(user1["user_id"]),
                "teacher_id": str(teacher_id1),
                "students_ids": [],
                "groups_ids": [],
            },
            {
                "user_id": str(user2["user_id"]),
                "teacher_id": str(teacher_id2),
                "students_ids": [],
                "groups_ids": [],
            },
            {
                "user_id": str(user3["user_id"]),
                "teacher_id": str(teacher_id3),
                "students_ids": [],
                "groups_ids": [],
            },
        ]
    }

    teachers = db.query(Teacher).all()
    assert len(teachers) == 3
