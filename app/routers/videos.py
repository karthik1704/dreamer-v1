from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.videos import Video
from app.schemas.videos import VideoCreate, VideoSchema

router = APIRouter(prefix="/videos", tags=["Videos"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]


@router.get("/", response_model=List[VideoSchema])
async def get_all_videos(db: db_dep, user: user_dep):

    videos = await Video.get_all(db, [])

    return videos




# """
#     Student Videos
# """


@router.get("/student/", response_model=List[VideoSchema])
async def get_all_student_videos(db: db_dep, user: user_dep, student: student_dep):

    videos = await Video.get_all(db, [Video.batch_id == student["batch_id"]])

    return videos


@router.get("/student/{id}/", response_model=VideoSchema)
async def get_student_video(
    db: db_dep, user: user_dep, student: student_dep, id: int = Path(gt=0)
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

# """
# Admin API's
# """


@router.get("/{id}/", response_model=VideoSchema)
async def get_video(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    video_detail = await Video.get_one(db, [Video.id == id])

    if not video_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        )

    return video_detail


@router.post("/", status_code=status.HTTP_201_CREATED)  # status code 201 for created
async def create_video(data: VideoCreate, db: db_dep, user: user_dep):

    new_video_data = data.model_dump()

    new_video = Video(**new_video_data)

    await Video.create_video(db, new_video)


@router.put("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_video(
    data: VideoCreate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):

    updated_data = data.model_dump()

    video = await Video.get_one(db, [Video.id == id])

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        )

    video.update_video(updated_data)
    await db.commit()
    


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    video = await Video.get_one(db, [Video.id == id])

    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found",
        )

    await db.delete(video)
    await db.commit()
