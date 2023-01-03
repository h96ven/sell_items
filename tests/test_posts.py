import pytest

from app import schemas


def test_get_all_posts(client, test_posts):
    res = client.get("/posts")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_all_posts_authorized_author(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_post_detail_not_exists(client, test_posts):
    res = client.get("/posts/77777")

    assert res.status_code == 404


def test_post_detail_not_exists_authorized_author(authorized_client, test_posts):
    res = authorized_client.get("/posts/77777")

    assert res.status_code == 404


def test_post_detail(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert post.title == test_posts[0].title


def test_post_detail_authorized_author(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, description, price",
    [
        ("awesome new title", "awesome new description", 33333),
        ("favorite pizza", "I love peperoni", 22222),
        ("awesome weather today", "awesome blues skies", 55555),
    ],
)
def test_create_post(
    authorized_client, test_author, test_posts, title, description, price
):
    res = authorized_client.post(
        "/posts",
        json={
            "title": title,
            "description": description,
            "price": price,
        },
    )

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.description == description
    assert created_post.price == price
    assert created_post.author.id == test_author["id"]


@pytest.mark.parametrize(
    "title, description, price",
    [
        ("awesome new title", "awesome new description", 33333),
        ("favorite pizza", "I love peperoni", 22222),
        ("awesome weather today", "awesome blues skies", 55555),
    ],
)
def test_create_post_unauthorized(client, test_posts, title, description, price):
    res = client.post(
        "/posts",
        json={
            "title": title,
            "description": description,
            "price": price,
        },
    )

    assert res.status_code == 401


def test_delete_post_unauthorized(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_existent(authorized_client, test_posts):
    res = authorized_client.delete("/posts/9999")

    assert res.status_code == 404


def test_delete_other_authors_post(authorized_client, test_author, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403


def test_update_post(authorized_client, test_author, test_posts):
    data = {
        "title": "updated_title",
        "description": "updated_description",
        "price": 1000,
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.description == data["description"]
    assert updated_post.price == data["price"]


def test_update_another_users_post(
    authorized_client, test_author, test_one_more_author, test_posts
):
    data = {
        "title": "updated_title",
        "description": "updated_description",
        "price": 1000,
        "id": test_posts[3].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_update_post_unauthorized(client, test_posts):
    data = {
        "title": "updated_title",
        "description": "updated_description",
        "price": 1000,
        "id": test_posts[0].id,
    }

    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401


def test_update_post_non_existent(authorized_client, test_posts):
    data = {
        "title": "updated_title",
        "description": "updated_description",
        "price": 1000,
        "id": 9999,
    }

    res = authorized_client.put("/posts/9999", json=data)

    assert res.status_code == 404
