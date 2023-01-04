from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, author, post, review

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(author.router)
app.include_router(auth.router)
app.include_router(review.router)


@app.get("/")
def home():
    return "Welcome"
