from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"Data": "Welcome"}


@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}")
def get_a_post_detail(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found.",
        )
    return {"post_detail": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_a_new_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.put("/posts/{id}")
def update_a_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} does not exist.",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} does not exist.",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
