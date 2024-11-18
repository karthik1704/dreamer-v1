from fastapi import APIRouter, Depends, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_user

from app.models.notes import Note
from app.schemas.users import UserCreate, UserSchema, UserUpdate

router = APIRouter(prefix="/notes", tags=["Notes"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]


@router.get("/", response_model=List[UserSchema])
async def get_all_notes(db: db_dep, user: user_dep):

    users = await Note.get_all(db, [Note.batch_id == user.get("batch_id")])

    return users



@router.get("/{id}/", response_model=UserSchema)
async def get_user(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    user_detail = await Note.get_one(db, [Note.id == id])

    return user_detail


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: db_dep,
    user: user_dep,
):

    new_user = User(**data.model_dump())
    db.add(new_user)
    await db.commit()


@router.put("/{id}/", response_model=UserSchema)
async def update_user( data: UserUpdate,db: db_dep, user: user_dep, id: int = Path(gt=0)):

    users = await User.get_one(db, [User.id == id])

    return users

