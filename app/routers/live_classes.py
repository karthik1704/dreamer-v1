from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.live_classes import LiveClass
from app.schemas.live_classes import LiveClassCreate, LiveClassSchema

router = APIRouter(prefix="/live-classes", tags=["Live Classes"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]


@router.get("/", response_model=List[LiveClassSchema])
async def get_all_live_classes(db: db_dep, user: user_dep):

    lives = await LiveClass.get_all(db, [])

    return lives




# """
#     Student 
# """


@router.get("/student/", response_model=LiveClassSchema)
async def get_all_student_live_class(db: db_dep, user: user_dep, student: student_dep):

    live = await LiveClass.get_one(db, [LiveClass.batch_id == student["batch_id"]])

    return live




# """
# Admin API's
# """


@router.get("/{id}/", response_model=LiveClassSchema)
async def get_live_class(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    live_class_detail = await LiveClass.get_one(db, [LiveClass.id == id])

    if not live_class_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Live class not found",
        )

    return live_class_detail


@router.post("/", status_code=status.HTTP_201_CREATED)  # status code 201 for created
async def create_live_class(data: LiveClassCreate, db: db_dep, user: user_dep):

    new_video_data = data.model_dump()

    new_video = LiveClass(**new_video_data)

    await LiveClass.create_live_classes(db, new_video)


@router.put("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_live_class(
    data: LiveClassCreate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):

    updated_data = data.model_dump()

    live_class = await LiveClass.get_one(db, [LiveClass.id == id])

    if not live_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Live class not found",
        )

    live_class.update_live_classes(updated_data)
    await db.commit()
    


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    live_class = await LiveClass.get_one(db, [LiveClass.id == id])

    if not live_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Live class not found",
        )

    await db.delete(live_class)
    await db.commit()
