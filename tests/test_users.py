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


def test_login_author(client, test_author):
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
