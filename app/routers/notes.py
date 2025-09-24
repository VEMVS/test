from ..db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_note(note: schemas.PostCreate, db: Session = Depends(get_db)):
    new_note = models.Note(**note.model_dump())

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/")
def get_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

