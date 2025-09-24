from ..db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    existing = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Этот адрес электронной почты уже используется",
        )
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    find_user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not find_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ником: {user_id}, не найден",
        )
    return find_user