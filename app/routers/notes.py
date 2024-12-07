from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.notes import Note, NoteCategory
from app.schemas.notes import NoteCategoryCreate, NoteCategorySchema, NoteCreate, NoteSchema

router = APIRouter(prefix="/notes", tags=["Notes"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]


@router.get("/", response_model=List[NoteSchema])
async def get_all_notes(db: db_dep, user: user_dep):

    notes = await Note.get_all(db, [])

    return notes

# """
#     Note Categories API's
# """

@router.get("/categories/", )
async def get_categories_without_repeat (db: db_dep, user: user_dep):

    categories = await NoteCategory.get_all_without_repeat(db, [])

    return categories


@router.get("/categories/batch/{id}/")
async def get_batch_categories(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    categories = await NoteCategory.get_all_without_repeat(db, [NoteCategory.batch_id == id])

    return categories

@router.get("/categories/all/",  response_model=List[NoteCategorySchema])
async def get_all_categories(db: db_dep, user: user_dep):

    categories = await NoteCategory.get_all(db, [])
   
    return categories


@router.get("/categories/{id}/", response_model=NoteCategorySchema)
async def get_category(db: db_dep, user: user_dep, id: int = Path(gt=0)):
        
        category = await NoteCategory.get_one(db, [NoteCategory.id == id])
    
        return category

@router.post("/categories/", status_code=status.HTTP_201_CREATED)  # status code 201 for created
async def create_category(data: NoteCategoryCreate, db: db_dep, user: user_dep):

    new_category_data = data.model_dump()
    new_category = NoteCategory(**new_category_data)
    await NoteCategory.create_note_category(db, new_category)

@router.put("/categories/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_category(
    data: NoteCategoryCreate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):

    updated_data = data.model_dump()

    category = await NoteCategory.get_one(db, [NoteCategory.id == id])

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    category.update_note_category(updated_data)
    await db.commit()

@router.delete("/categories/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    category = await NoteCategory.get_one(db, [NoteCategory.id == id])

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    await db.delete(category)
    await db.commit()

# """
#     Student Notes
# """

@router.get("/student/", response_model=List[NoteSchema])
async def get_student_notes(db: db_dep, student: student_dep):

    notes = await Note.get_all(db, [Note.batch_id == student['batch_id'], Note.category_id == None])

    return notes

@router.get("/student/folders/", )
async def get_student_notes_folders(db: db_dep, student: student_dep):

    notes_folders = await NoteCategory.get_all_without_repeat(db, [Note.batch_id == student['batch_id']])

    return notes_folders

@router.get("/student/folders/{id}", )
async def get_student_notes_folders_by_id(db: db_dep, student: student_dep, id:int=Path(gt=0)):

    notes_folder = await NoteCategory.get_one(db, [Note.batch_id == student['batch_id'], NoteCategory.id == id])

    if not notes_folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found",
        )

    return notes_folder

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

  
