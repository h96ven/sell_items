from random import randrange

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    description: str
    price: int
    is_active: bool = True


posts = [
    {
        "id": 1,
        "title": "Iphone 13",
        "description": "...",
        "price": 1000,
        "is_active": True,
        "created_at": "",
        "updated_at": "",
        "author": {"id": 1, "email": ""},
    },
    {
        "id": 2,
        "title": "Iphone 12",
        "description": "...",
        "price": 800,
        "is_active": True,
        "created_at": "",
        "updated_at": "",
        "author": {"id": 2, "email": ""},
    },
]


def find_post(id):
    for p in posts:
        if p["id"] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(posts):
        if p["id"] == id:
            return i


@app.get("/")
def home():
    return {"Data": "Welcome"}


@app.get("/posts")
def get_all_posts():
    return posts


@app.get("/posts/{id}")
def get_a_post_detail(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found.",
        )
    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_a_new_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    posts.append(post_dict)
    return post_dict


@app.put("/posts/{id}")
def update_a_post(id: int, post: Post):
    index = find_post_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} does not exist.",
        )

    post_dict = post.dict()
    post_dict["id"] = id
    posts[index] = post_dict
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(id: int):
    index = find_post_index(id)
    if not index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} does not exist.",
        )
    posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
