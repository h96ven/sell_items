import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/"
    f"{settings.database_name}_test"
)


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
def test_one_more_author(client):
    author_data = {
        "email": "steve@email.com",
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


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_author, test_one_more_author, session):
    posts_data = [
        {
            "title": "first_title",
            "description": "first_description",
            "price": 111,
            "author_id": test_author["id"],
        },
        {
            "title": "second_title",
            "description": "second_description",
            "price": 222,
            "author_id": test_author["id"],
        },
        {
            "title": "third_title",
            "description": "third_description",
            "price": 333,
            "author_id": test_author["id"],
        },
        {
            "title": "forth_title",
            "description": "forth_description",
            "price": 444,
            "author_id": test_one_more_author["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)

    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()

    return posts


@pytest.fixture
def test_reviews(test_posts, test_author, test_one_more_author, session):
    reviews_data = [
        {
            "comment": "A very cool comment.",
            "author": test_author["id"],
            "post": test_posts[0].id,
        },
        {
            "comment": "A very interesting comment.",
            "author": test_author["id"],
            "post": test_posts[0].id,
        },
        {
            "comment": "A very shocking comment.",
            "author": test_author["id"],
            "post": test_posts[0].id,
        },
        {
            "comment": "A very shocking comment.",
            "author": test_one_more_author["id"],
            "post": test_posts[3].id,
        },
    ]

    def create_review_model(review):
        return models.Review(**review)

    review_map = map(create_review_model, reviews_data)

    reviews = list(review_map)

    session.add_all(reviews)

    session.commit()

    reviews = session.query(models.Review).all()

    return reviews
