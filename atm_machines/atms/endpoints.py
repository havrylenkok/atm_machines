from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from atm_machines.atms import models
from atm_machines.atms.schemas import Note, NoteIn
from atm_machines.dependencies import get_db

router = APIRouter()


@router.get("/notes/", response_model=List[Note])
def read_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).filter()


@router.post("/notes/", response_model=Note)
def create_note(note: NoteIn, db: Session = Depends(get_db)):
    db_note = models.Note(text=note.text, completed=note.completed)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
