from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    description: str
    price: int
    is_active: bool = True


posts = [
    {
        "title": "Iphone 13",
        "description": "...",
        "price": 1000,
        "is_active": True,
        "created_at": "",
        "updated_at": "",
        "author": {"id": 1, "email": ""},
    },
    {
        "title": "Iphone 12",
        "description": "...",
        "price": 800,
        "is_active": True,
        "created_at": "",
        "updated_at": "",
        "author": {"id": 2, "email": ""},
    },
]


@app.get("/")
def home():
    return {"Data": "Welcome"}


@app.get("/posts")
def get_all_posts():
    return {"data": "These are your posts"}


@app.get("/posts/{id}")
def get_a_post_detail(id: int):
    return posts[id - 1]


@app.post("/posts")
def create_a_new_post(post: Post):
    return post
