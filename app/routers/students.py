import base64
import os
import shutil
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user
from pathlib import Path as PyPath 

from app.settings import UPLOAD_DIR
from app.models.students import Student, StudentProfile
from app.schemas.students import CreateStudentProfile, StudentSchema, StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["Notes"])

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
    student_profile = new_student_data.pop("student_profile", None)

    # Create the new student entry
    new_student = Student(**new_student_data)

    # Add to the session and flush
    db.add(new_student)
    await db.flush()  # Flush to get the student ID for the profile

    if student_profile:
        # Process the profile image if available
        image = student_profile.pop("student_photo", None)
        image_path = None
        if image:
            try:
                # Decode Base64 image
                image_data = image.split(",")[
                    1
                ]  # Remove the Base64 metadata if present
                image_binary = base64.b64decode(image_data)

                # Save the image to the server
                unique_filename = f"{uuid.uuid4()}-{new_student.student_code}.png"
                image_path = UPLOAD_DIR / unique_filename
                image_path.write_bytes(image_binary)

            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error processing image: {str(e)}"
                )

        # Create the student profile
        new_student_profile = StudentProfile(
            student_id=new_student.id, **student_profile, student_photo=f"/static/{unique_filename}"
        )
        db.add(new_student_profile)

    # Commit all changes in the session
    await db.commit()


@router.put("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(
    data: StudentUpdate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):
    
    student_detail = await Student.get_one(db, [Student.id == id])
    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    updated_data = data.model_dump()
    student_profile = updated_data.pop("student_profile", None)
    student_detail.update_student(updated_data)
    if student_profile:
        if student_detail.student_profile:
            student_detail.student_profile.update_profile(student_profile)
        else:
            new_student_profile = StudentProfile(
                student_id=student_detail.id, **student_profile
            )
            db.add(new_student_profile)

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


@router.post("/upload-image/{student_id}/")
async def upload_image(
    student_id: int, 
    db: db_dep, 
    current_user: user_dep, 
    file: UploadFile = File(...),
):
    # Check if the file is an image
    if file.content_type is None or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File type not supported.")

    # Fetch the resume
    profile = await StudentProfile.get_one(db, [StudentProfile.student_id == student_id])
    if not profile:
        raise HTTPException(status_code=404, detail="student profile not found.")

    # Delete the existing image if it exists
    if profile.student_photo:
    # Convert the relative URL to an absolute path
        existing_image_path = UPLOAD_DIR / PyPath(profile.student_photo).name  # Get the filename and append to UPLOAD_DIR
        if existing_image_path.exists():
            try:
                os.remove(existing_image_path)  # Delete the existing image
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete existing image: {str(e)}")
    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    file_location = UPLOAD_DIR / unique_filename

    # Save the new file
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)  # Save the file efficiently
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save the file: {str(e)}")
    finally:
        await file.close()  # Close the file to free up resources

    # Update the resume with the new image path
    profile.student_photo = f"/static/{unique_filename}" # Save the new image path in the resume
    await db.commit()
    await db.refresh(profile)

    return {"message": "Image uploaded successfully", "student_photo": profile.student_photo}

# """
# Students API
# """


@router.get("/me/", response_model=StudentSchema)
async def get_current_logged_student(db: db_dep, student: student_dep):

    student_detail = await Student.get_one(db, [Student.id == student["id"]])

    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return student_detail


@router.put("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def update_current_logged_student(
    data: StudentCreate, db: db_dep, student: student_dep
):

    student_detail = await Student.get_one(db, [Student.id == student["id"]])
    if not student_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    updated_data = data.model_dump()
    student_detail.update_student(updated_data)

    await db.commit()
