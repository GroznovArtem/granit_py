import uuid

import pytest

from app.db.models.users import User


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


def test_create_user(db, client, user_params):
    response = client.post("/user", json=user_params)

    assert response.status_code == 200
    assert response.json() == {
        "name": "Artem",
        "surname": "Groznov",
        "email": "a.g@ya.ru",
    }

    created_user = db.query(User).filter(User.user_id == user_params["user_id"])
    assert created_user is not None


def test_get_user(db, client, create_user_in_db, user_params):
    create_user_in_db(**user_params, session=db)

    response = client.get("/user/{}".format(user_params["user_id"]))

    assert response.status_code == 200
    assert response.json() == user_params


def test_get_user_if_not_found(db, client, create_user_in_db, user_params):
    create_user_in_db(**user_params, session=db)
    user_params["user_id"] = str(uuid.uuid4())

    response = client.get("/user/{}".format(user_params["user_id"]))

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"User with id {user_params['user_id']} not found."
    }


def test_delete_user(db, client, create_user_in_db, user_params):
    create_user_in_db(**user_params, session=db)

    response = client.delete("/user/{}".format(user_params["user_id"]))

    assert response.status_code == 200
    assert response.json() == {"user_id": user_params["user_id"]}

    user = db.query(User).filter(User.user_id == user_params["user_id"]).first()

    assert not user.is_active


def test_delete_user_if_not_found(db, client, create_user_in_db, user_params):
    create_user_in_db(**user_params, session=db)
    user_params["user_id"] = str(uuid.uuid4())

    response = client.delete("/user/{}".format(user_params["user_id"]))

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"User with id {user_params['user_id']} not found."
    }


def test_update_user(db, client, create_user_in_db, user_params):
    create_user_in_db(**user_params, session=db)

    data_to_update = {
        "name": "Alex",
        "surname": "Volin",
        "email": "a.v@ya.ru",
    }

    response = client.patch(
        "/user/{}".format(user_params["user_id"]), json=data_to_update
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": user_params["user_id"],
        "name": data_to_update["name"],
        "surname": data_to_update["surname"],
        "email": data_to_update["email"],
    }

    user = db.query(User).filter(User.user_id == user_params["user_id"]).first()

    assert user.name == data_to_update["name"]
    assert user.surname == data_to_update["surname"]
    assert user.email == data_to_update["email"]


def test_update_user_if_not_found(db, client, create_user_in_db, user_params):
    create_user_in_db(**user_params, session=db)
    user_params["user_id"] = str(uuid.uuid4())

    data_to_update = {
        "name": "Alex",
        "surname": "Volin",
        "email": "a.v@ya.ru",
    }

    response = client.patch(
        "/user/{}".format(user_params["user_id"]), json=data_to_update
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"User with id {user_params['user_id']} not found."
    }


# def test_get_users(db, client, create_user_in_db, user_params):
#     u_p_1 = user_params
#     u_p_1["email"] = "test1@ya.ru"
#     u_p_2 = user_params
#     u_p_2["email"] = "test2@ya.ru"
#     u_p_3 = user_params
#     u_p_3["email"] = "test3@ya.ru"
#     create_user_in_db(**u_p_1, session=db)
#     create_user_in_db(**u_p_2, session=db)
#     create_user_in_db(**u_p_3, session=db)
#
#     response = client.get(
#         "/user"
#     )
#
#     assert response.status_code == 200
#     assert response.json() == {
#         users: [
#             {
#                 "name": u_p_1["name"],
#                 "surname": u_p_1["surname"],
#                 "email": u_p_1["email"],
#             },
#             {
#                 "name": u_p_2["name"],
#                 "surname": u_p_2["surname"],
#                 "email": u_p_2["email"],
#             },
#             {
#                 "name": u_p_3["name"],
#                 "surname": u_p_3["surname"],
#                 "email": u_p_3["email"],
#             },
#         ]
#     }
