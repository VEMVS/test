from ..db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas, oauth2, shared
from typing import List

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.NoteResponse
)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    new_note = models.Note(owner_id=current_user.id, **note.model_dump())

    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/", response_model=List[schemas.NoteResponse])
def get_all_notes(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    return db.query(models.Note).all()


@router.get("/read", response_model=schemas.NoteResponse)
def read_note(token: str, db: Session = Depends(get_db)):
    payload = shared.decode_token(token)
    scope = payload.get("scope")
    note_id = payload.get("note_id")

    if note_id is None or scope != "notes:read":
        raise HTTPException(status_code=403, detail="Токен не позволяет просматривать")
    note_query = db.query(models.Note).filter(models.Note.id == note_id)
    note = note_query.first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка с id: {note_id} не найдена",
        )

    return note


@router.get("/{note_id}", response_model=schemas.NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена"
        )
    return note


@router.put("/edit", response_model=schemas.NoteResponse)
async def edit_note(
    update: schemas.NoteUpdate, token: str, db: Session = Depends(get_db)
):
    payload = shared.decode_token(token)
    scope = payload.get("scope")
    note_id = payload.get("note_id")
    if note_id is None or scope != "notes:edit":
        raise HTTPException(status_code=403, detail="Токен не позволяет редактировать")
    note_query = db.query(models.Note).filter(models.Note.id == note_id)
    note = note_query.first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка с id: {note_id} не найдена",
        )
    note_query.update(update.model_dump(), synchronize_session="fetch")
    db.commit()
    update_note = note_query.first()
    return update_note


@router.put("/{note_id}", response_model=schemas.NoteResponse)
def put_note(
    note_id: int,
    update_note: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    note_query = db.query(models.Note).filter(models.Note.id == note_id)
    note = note_query.first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заметка с id: {note_id} не найдена",
        )
    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
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
