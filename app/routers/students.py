from turtle import st
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.students import Student
from app.schemas.students import StudentSchema, StudentCreate

router = APIRouter(prefix="/notes", tags=["Notes"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]

@router.get("/", response_model=List[StudentSchema])
async def get_all_students(db: db_dep, user: user_dep):

    students = await Student.get_all(db, [])

    return students

@router.get("/{id}/", response_model=StudentSchema)
async def get_student(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    student_detail = await Student.get_one(db, [Student.id == id])
    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return student_detail

@router.post("/", status_code=status.HTTP_201_CREATED)  # status code 201 for created
async def create_student(data: StudentCreate, db: db_dep, user: user_dep):

    new_student_data = data.model_dump()

    await Student.create_student(db, new_student_data)

@router.put("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(data: StudentCreate, db: db_dep, user: user_dep, id: int = Path(gt=0)):

    student_detail = await Student.get_one(db, [Student.id == id])
    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    updated_data = data.model_dump()
    student_detail.update_student(updated_data)
    
    await db.commit()

@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    student_detail = await Student.get_one(db, [Student.id == id])
    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    await db.delete(student_detail)
    await db.commit()

#"""
# Students API
#"""

@router.get("/me/", response_model=StudentSchema)
async def get_current_logged_student(db:db_dep,student: student_dep):

    student_detail = await Student.get_one(db, [Student.id == student['id']])

    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return student_detail

@router.put("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def update_current_logged_student(data: StudentCreate, db: db_dep, student: student_dep):

    student_detail = await Student.get_one(db, [Student.id == student['id']])
    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    updated_data = data.model_dump()
    student_detail.update_student(updated_data)
    
    await db.commit()