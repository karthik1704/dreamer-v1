from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.videos import Video, VideoCategory
from app.schemas.videos import VideoCategorySchema, VideoCreate, VideoSchema

router = APIRouter(prefix="/videos/student", tags=["Student Videos"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
student_dep = Annotated[dict, Depends(get_current_student)]




@router.get("/", response_model=List[VideoSchema])
async def get_all_student_videos(db: db_dep,  student: student_dep):

    videos = await Video.get_all(db, [Video.batch_id == student["batch_id"]])

    return videos

@router.get("/folders/", response_model=List[VideoCategorySchema])
async def get_all_student_video_categories(db: db_dep, student: student_dep):

    categories = await VideoCategory.get_all_without_repeat(db, [VideoCategory.batch_id == student["batch_id"]])

    return categories

@router.get("/folders/{id}/", response_model=VideoCategorySchema)
async def get_student_video_category(
    db: db_dep, student: student_dep, id: int = Path(gt=0)
):

    category = await VideoCategory.get_one(
        db, [VideoCategory.id == id, VideoCategory.batch_id == student["batch_id"]]
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


@router.get("/student/{id}/", response_model=VideoSchema)
async def get_student_video(
    db: db_dep,  student: student_dep, id: int = Path(gt=0)
):

    video = await Video.get_one(
        db, [Video.id == id, Video.batch_id == student["batch_id"]]
    )

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        )

    return video
