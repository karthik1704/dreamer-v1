from typing import Annotated
from fastapi import Depends, Response, status, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.students import Student
from ..models.users import User
from ..schemas.auth import Token
from ..utils.auth import create_student_access_token, verify_password, create_access_token
from ..database import get_async_db

router = APIRouter(prefix="/auth", tags=["auth"])


db_dep = Annotated[AsyncSession, Depends(get_async_db)]


async def authenticate_user(username: str, password: str, db: db_dep):
    user = await User.get_one(db, [User.username == username])
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def authenticate_student(username: str, password: str, db: db_dep):
    user = await Student.get_one(db, [Student.student_code == username])
    if not user:
        print('user')
        return False
    if not verify_password(password, user.password):
        print('password')
        return False
    return user


@router.post("/", response_model=Token)
async def admin_login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dep,
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )

    token = create_access_token(user.username, user.email, user.id)
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=2 * 24 * 60 * 60,  # Two days in seconds
        secure=False,
        httponly=True,
        path="/",
        domain="localhost",
    )

    return {"access_token": token, "token_type": "bearer"}

@router.post("/student/", response_model=Token)
async def student_login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dep,
):
    user = await authenticate_student(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )

    token = create_student_access_token(user.student_code, user.email, user.id, user.batch_id)
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=2 * 24 * 60 * 60,  # Two days in seconds
        secure=False,
        httponly=True,
        path="/",
        domain="localhost",
    )

    return {"access_token": token, "token_type": "bearer"}
