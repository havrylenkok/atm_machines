from typing import List

from fastapi import APIRouter

from atm_machines.atms.schemas import Note, NoteIn
from atm_machines.database import notes, db

router = APIRouter()


@router.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await db.fetch_all(query)


@router.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await db.execute(query)
    return {**note.dict(), "id": last_record_id}
