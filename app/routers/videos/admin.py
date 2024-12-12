import base64
import uuid
from pathlib import Path as PyPath
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.videos import Video, VideoCategory
from app.schemas.videos import VideoCategorySchema, VideoCreate, VideoSchema, VidoeCategoryCreate
from app.settings import UPLOAD_DIR

router = APIRouter(prefix="/videos", tags=["Admin Videos"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]


@router.get("/", response_model=List[VideoSchema])
async def get_all_videos(db: db_dep, user: user_dep):

    videos = await Video.get_all(db, [])

    return videos


@router.get("/categories/", response_model=List[VideoCategorySchema])
async def get_all_video_categories(db: db_dep, user: user_dep):

    categories = await VideoCategory.get_all(db, [])

    return categories


@router.get("/categories/no-repeat/", response_model=List[VideoCategorySchema])
async def get_all_video_categories_no_repeat(db: db_dep, user: user_dep):

    categories = await VideoCategory.get_all_without_repeat(db, [])

    return categories


@router.get("/categories/batch/{batch_id}/", response_model=List[VideoCategorySchema])
async def get_all_video_categories_by_batch(
    db: db_dep, user: user_dep, batch_id: int = Path(gt=0)
):
    categories = await VideoCategory.get_all(db, [VideoCategory.batch_id == batch_id])

    return categories


@router.get("/categories/{id}/", response_model=VideoCategorySchema)
async def get_video_category(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    category = await VideoCategory.get_one(db, [VideoCategory.id == id])

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category



@router.post(
    "/categories/", status_code=status.HTTP_201_CREATED
)  # status code 201 for created
async def create_video_category(
    data: VidoeCategoryCreate,
    db: db_dep,
    user: user_dep,
):

    new_category_data = data.model_dump()
    image = new_category_data.pop("image", None)
    image_path = None
    if image:
        try:
            # Decode Base64 image
            image_data = image.split(",")[
                1
            ]  # Remove the Base64 metadata if present
            image_binary = base64.b64decode(image_data)

            # Save the image to the server
            unique_filename = f"{uuid.uuid4()}-{new_category_data.get("category_name")}.png"
            image_path = UPLOAD_DIR / unique_filename
            image_path.write_bytes(image_binary)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error processing image: {str(e)}"
            )

    new_category = VideoCategory(**new_category_data,  image=f"/static/{unique_filename}" if image_path else None)

    db.add(new_category)
    await db.commit()
   

@router.put("/categories/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_video_category(
    data: VidoeCategoryCreate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):

    updated_data = data.model_dump()
    image = updated_data.pop("image", None)
    category = await VideoCategory.get_one(db, [VideoCategory.id == id])

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    category.update_video_category(updated_data)

    if image:
        if category.image:
            image_path = UPLOAD_DIR / PyPath(category.image).name 
            image_path.unlink(missing_ok=True)
        try:
            # Decode Base64 image
            image_data = image.split(",")[
                1
            ]  # Remove the Base64 metadata if present
            image_binary = base64.b64decode(image_data)

            # Save the image to the server
            unique_filename = f"{uuid.uuid4()}-{category.category_name}.png"
            image_path = UPLOAD_DIR / unique_filename
            image_path.write_bytes(image_binary)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error processing image: {str(e)}"
            )

        category.image = f"/static/{unique_filename}"

    await db.commit()


@router.delete("/categories/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video_category(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    category = await VideoCategory.get_one(db, [VideoCategory.id == id])

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    await db.delete(category)
    await db.commit()


@router.get("/student/", response_model=List[VideoSchema])
async def get_all_student_videos(db: db_dep,  student: student_dep):

    videos = await Video.get_all(db, [Video.batch_id == student["batch_id"]])

    return videos

@router.get("/student/folders/", )
async def get_all_student_video_categories(db: db_dep, student: student_dep):

    categories = await VideoCategory.get_all_without_repeat(db, [VideoCategory.batch_id == student["batch_id"]])

    return categories

@router.get("/student/folders/{id}/", )
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
