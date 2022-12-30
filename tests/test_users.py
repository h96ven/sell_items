from app import schemas
from tests.database import client, session  # noqa


def test_home_page(client):  # noqa
    res = client.get("/")
    assert res.json() == "Welcome"
    assert res.status_code == 200


def test_create_author(client):  # noqa
    res = client.post(
        "/authors",
        json={"email": "monica@mail.com", "password": "n74cty57645t"},
    )
    new_author = schemas.AuthorOutResponse(**res.json())
    assert new_author.email == "monica@mail.com"
    assert res.status_code == 201
