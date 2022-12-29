from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db

router = APIRouter(prefix="/posts/{id}/comments", tags=["Comments"])


@router.get("/", response_model=List[schemas.ReviewResponse])
def get_all_comments(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found.",
        )

    comments = db.query(models.Review).filter(models.Review.post == id).all()

    return comments


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_a_new_comment(
    id: int,
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    # Requires a user to be authenticated in order to create a new post.
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The post with id {id} was not found.",
        )

    new_comment = models.Review(author=current_user.id, post=id, **review.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
