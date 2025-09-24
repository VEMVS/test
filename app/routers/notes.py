from ..db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas
from typing import List

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


@router.get("/", response_model=List[schemas.PostResponse])
def get_all_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()


@router.get("/{note_id}", response_model=schemas.PostResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена"
        )
    return note


@router.put("/{note_id}", response_model=schemas.PostResponse)
def put_note(
    note_id: int, update_note: schemas.PostUpdate, db: Session = Depends(get_db)
):
    note_query = db.query(models.Note).filter(models.Note.id == note_id)
    note = note_query.first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка с id: {note_id} не найдена",
        )
    note_query.update(update_note.model_dump(), synchronize_session="fetch")
    db.commit()
    update_note = note_query.first()
    return update_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка с id: {note_id} не найдена",
        )
    db.delete(note)
    db.commit()
