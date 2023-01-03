def test_get_all_posts(client, test_posts):
    res = client.get("/posts")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_all_posts_authorized_author(authorized_client, test_posts):
    res = authorized_client.get("/posts")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
