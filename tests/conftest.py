import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test@localhost:5432/fastapi_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_author(client):
    author_data = {
        "email": "tom@email.com",
        "password": "ILoveDjango",
    }

    res = client.post("/authors", json=author_data)

    assert res.status_code == 201

    new_author = res.json()
    new_author["password"] = author_data["password"]

    return new_author


@pytest.fixture
def token(test_author):
    return create_access_token({"user_id": test_author["id"]})


def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client
