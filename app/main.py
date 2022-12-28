from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import auth, author, post, review

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(author.router)
app.include_router(auth.router)
app.include_router(review.router)


@app.get("/")
def home():
    return "Welcome"
