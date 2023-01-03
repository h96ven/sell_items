import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_home_page(client):
    res = client.get("/")
    assert res.json() == "Welcome"
    assert res.status_code == 200


def test_create_author(client):
    res = client.post(
        "/authors",
        json={"email": "monica@mail.com", "password": "n74cty57645t"},
    )
    new_author = schemas.AuthorOutResponse(**res.json())

    assert new_author.email == "monica@mail.com"
    assert res.status_code == 201


def test_login_author(test_author, client):
    res = client.post(
        "/login",
        data={"username": test_author["email"], "password": test_author["password"]},
    )

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")

    assert id == test_author["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong_email@mail.com", "ILoveDjango", 403),
        ("tom@email.com", "wrong_password", 403),
        ("wrong_email@mail.com", "wrong_password", 403),
        (None, "ILoveDjango", 422),
        ("tom@email.com", None, 422),
    ],
)
def test_incorrect_login(test_author, client, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )

    assert res.status_code == status_code


def test_logout_author_unauthorized(client):
    res = client.get("/logout")

    assert res.status_code == 401


def test_logout_author(authorized_client):
    res = authorized_client.get("/logout")

    assert res.status_code == 200
