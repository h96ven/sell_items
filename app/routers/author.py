from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import get_db

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AuthorOutResponse,
)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(author.password)
    author.password = hashed_password
    new_author = models.Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/{id}", response_model=schemas.AuthorOutResponse)
def get_author(id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == id).first()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id {id} does not exist.",
        )
    return author
