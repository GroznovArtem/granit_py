import uuid

import pytest

from sqlalchemy.orm import Session
from app.db.models.users import Student


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
def create_student():
    def wrapper(user_id: uuid.UUID, session: Session):
        student = Student(user_id=user_id)
        with session as db:
            db.add(student)
            db.commit()
            db.flush()

        return student.student_id

    return wrapper


def test_create_student(db, create_user_in_db, user_params, client):
    create_user_in_db(**user_params, session=db)

    response = client.post("/student", json={"user_id": user_params["user_id"]})

    assert response.status_code == 200
    assert response.json()["user_id"] == user_params["user_id"]

    student = (
        db.query(Student).filter(Student.user_id == user_params["user_id"]).first()
    )

    assert student is not None


def test_create_student_if_user_not_found(db, create_user_in_db, user_params, client):
    response = client.post("/student", json={"user_id": user_params["user_id"]})

    assert response.status_code == 400
    assert response.json() == {"detail": "Unbound error."}

    student = db.query(Student).first()

    assert student is None


def test_get_student(db, create_user_in_db, create_student, user_params, client):
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

    student_id1 = create_student(uuid.UUID(user1["user_id"]), session=db)
    student_id2 = create_student(uuid.UUID(user2["user_id"]), session=db)
    student_id3 = create_student(uuid.UUID(user3["user_id"]), session=db)

    response = client.get("/student")

    assert response.status_code == 200
    assert response.json() == {
        "students": [
            {
                "user_id": str(user1["user_id"]),
                "student_id": str(student_id1),
                "teachers_ids": [],
            },
            {
                "user_id": str(user2["user_id"]),
                "student_id": str(student_id2),
                "teachers_ids": [],
            },
            {
                "user_id": str(user3["user_id"]),
                "student_id": str(student_id3),
                "teachers_ids": [],
            },
        ]
    }

    student = db.query(Student).all()
    assert len(student) == 3


def test_delete_student(db, create_user_in_db, create_student, user_params, client):
    create_user_in_db(**user_params, session=db)
    student_id = create_student(uuid.UUID(user_params["user_id"]), session=db)

    response = client.delete("/student/{}".format(str(student_id)))

    assert response.status_code == 200
    assert response.json() == {"student_id": str(student_id)}

    student = db.query(Student).filter(Student.student_id == student_id).first()

    assert student is None
