from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session
from .. import db, schemas, models, utils, shared, oauth2
from typing import Annotated
from yarl import URL
from ..config import settings

router = APIRouter(prefix="/link", tags=["Link"])


@router.get("/")
def create_link(
    data: schemas.Link,
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
    db: Session = Depends(db.get_db),
):

    note = db.query(models.Note).filter(models.Note.id == data.note_id).first()

    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не уполномочен выполнять запрошенное действие",
        )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заметка не найдена"
        )

    access_token = shared.create_token(
        payload={"note_id": data.note_id, "scope": data.scope}
    )

    if data.scope == "notes:edit":
        url_path = "edit"
    else:
        url_path = "read"

    url_host = settings.host
    url_port = settings.port

    share_link = str(URL.build(
        scheme="http",
        host=url_host,
        port=url_port,
        path=f"/notes/{url_path}",
        query={"token": access_token}
    ))
    return {"share_link": share_link}


