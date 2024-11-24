from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.notes import Note
from app.schemas.notes import NoteCreate, NoteSchema

router = APIRouter(prefix="/notes", tags=["Notes"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]


@router.get("/", response_model=List[NoteSchema])
async def get_all_notes(db: db_dep, user: user_dep):

    notes = await Note.get_all(db, [])

    return notes


"""
    Student Notes
"""

@router.get("/student/", response_model=List[NoteSchema])
async def get_student_notes(db: db_dep, student: student_dep):

    notes = await Note.get_all(db, [Note.batch_id == student['batch_id']])

    return notes

@router.get("/student/{id}/", response_model=NoteSchema)    
async def get_student_note(db: db_dep, student: student_dep, id: int = Path(gt=0)):

    note_detail = await Note.get_one(db, [Note.id == id, Note.batch_id == student['batch_id']])

    if not note_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note_detail

# """
# Admin API's
# """

@router.get("/{id}/", response_model=NoteSchema)    
async def get_note(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    note_detail = await Note.get_one(db, [Note.id == id])

    return note_detail

@router.post("/", status_code=status.HTTP_201_CREATED)  # status code 201 for created
async def create_note(data: NoteCreate, db: db_dep, user: user_dep):

    new_note_data = data.model_dump()
    new_note = Note(**new_note_data)
    await Note.create_note(db, new_note)

@router.put("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_note(
    data: NoteCreate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):

    updated_data = data.model_dump()

    note = await Note.get_one(db, [Note.id == id])

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    note.update_note(updated_data)
    await db.commit()

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    note = await Note.get_one(db, [Note.id == id])

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    await db.delete(note)
    await db.commit()

  
