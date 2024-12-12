# from fastapi import APIRouter, Depends, HTTPException, Path
# from starlette import status
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Annotated, List
# from app.database import get_async_db
# from app.dependencies.auth import get_current_student, get_current_user

# from app.models.videos import Video, VideoCategory
# from app.schemas.videos import VideoCategorySchema, VideoCreate, VideoSchema

# router = APIRouter(prefix="/videos/", tags=["Student Videos"])

# db_dep = Annotated[AsyncSession, Depends(get_async_db)]
# student_dep = Annotated[dict, Depends(get_current_student)]


