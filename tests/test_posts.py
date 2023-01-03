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
