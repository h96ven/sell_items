from datetime import datetime

from app import schemas


def test_get_all_reviews(client, test_posts, test_reviews):
    res = client.get(f"/posts/{test_posts[0].id}/comments")

    assert res.status_code == 200
    assert len(res.json()) == 3


def test_get_all_reviews_authorized_author(authorized_client, test_posts, test_reviews):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments")

    assert res.status_code == 200
    assert len(res.json()) == 3


def test_get_all_reviews_for_nonenxistent_post(client, test_posts, test_reviews):
    res = client.get(f"/posts/{99999}/comments")

    assert res.status_code == 404


def test_get_all_reviews_for_nonenxistent_post_authorized(
    authorized_client, test_posts, test_reviews
):
    res = authorized_client.get(f"/posts/{99999}/comments")

    assert res.status_code == 404


def test_create_review(authorized_client, test_author, test_posts, test_reviews):
    res = authorized_client.post(
        f"/posts/{test_posts[0].id}/comments",
        json={"comment": "A brand new comment"},
    )

    new_review = schemas.ReviewResponse(**res.json())

    assert res.status_code == 201
    assert new_review.comment == "A brand new comment"
    assert new_review.author == test_author["id"]
    assert isinstance(new_review.created_at, datetime)


def test_create_review_unauthorized(client, test_author, test_posts, test_reviews):
    res = client.post(
        f"/posts/{test_posts[0].id}/comments",
        json={"comment": "A brand new comment"},
    )

    assert res.status_code == 401


def test_create_review_for_nonenxistent_post(
    authorized_client, test_author, test_posts, test_reviews
):

    res = authorized_client.post(
        f"/posts/{99999}/comments",
        json={"comment": "A brand new comment"},
    )

    assert res.status_code == 404
