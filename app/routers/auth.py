from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, models, oauth2, schemas, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.Author)
        .filter(models.Author.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
def logout(
    token: str = Depends(oauth2.get_token_from_user),
    current_user: schemas.AuthorOutResponse = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    # Saving token to blacklist
    new_entry = models.Blacklist(token=token, email=current_user.email)

    db.add(new_entry)
    db.commit()

    return "The user logged out successfully."
