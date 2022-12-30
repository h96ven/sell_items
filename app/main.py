from fastapi import FastAPI

from app.routers import auth, author, post, review

app = FastAPI()

app.include_router(post.router)
app.include_router(author.router)
app.include_router(auth.router)
app.include_router(review.router)


@app.get("/")
def home():
    return "Welcome"
