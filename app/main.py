from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import author, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(author.router)


@app.get("/")
def home():
    return "Welcome"
