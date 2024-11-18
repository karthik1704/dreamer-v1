from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_user

from app.models.users import User
from app.schemas.users import UserCreate, UserSchema, UserUpdate
from app.utils.auth import get_hashed_password

router = APIRouter(prefix="/users", tags=["Users"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]


@router.get("/", response_model=List[UserSchema])
async def get_all_users(db: db_dep, user: user_dep):

    users = await User.get_all(db, [])

    return users


@router.get("/me/", response_model=UserSchema)
async def get_current_loggedin_user(db: db_dep, user: user_dep):

    user_detail = await User.get_one(db, [User.id == user.get("id")])

    return user_detail


@router.get("/{id}/", response_model=UserSchema)
async def get_user(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    user_detail = await User.get_one(db, [User.id == id])

    return user_detail


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: db_dep,
    user: user_dep,
):
    new_user_data = data.model_dump()
    password = new_user_data.pop("password")
    password2 = new_user_data.pop("password2")

    email_already_exists = await User.get_one(
        db, [User.email == new_user_data.get("email")]
    )
    if email_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with email already exists",
        )

    username_already_exists = await User.get_one(
        db, [User.username == new_user_data.get("username")]
    )
    if username_already_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this username not avaliable",
        )

    if password != password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )

    hashed_password = get_hashed_password(password)

    new_user = User(**new_user_data, password=hashed_password)
    db.add(new_user)
    await db.commit()


@router.put("/{id}/", response_model=UserSchema)
async def update_user(
    data: UserUpdate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):

    users = await User.get_one(db, [User.id == id])

    return users
