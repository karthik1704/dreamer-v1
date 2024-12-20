from datetime import datetime, timedelta, UTC
from typing import  Any, Optional
from jose import jwt
from passlib.context import CryptContext
from app.settings import JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"



def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(
    username: str,
    email: str,
    user_id: int,
    expires_delta: int | None = None,
) -> str:
    if expires_delta is not None:
        expires_at = datetime.now(UTC) + timedelta(days=30)
    else:
        expires_at = datetime.now(UTC) + timedelta(days=30)

    print(expires_at)

    encode = {"sub": username, "email":email, "id": user_id, }
    encode.update({"exp": expires_at})
    encoded_jwt = jwt.encode(encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_student_access_token(
    username: str,
    email: str,
    user_id: int,
    batch_id: int,
    expires_delta: int | None = None,
) -> str:
    if expires_delta is not None:
        expires_at = datetime.now(UTC) + timedelta(days=30)
    else:
        expires_at = datetime.now(UTC) + timedelta(days=30)

    print(expires_at)

    encode = {"sub": username, "email":email, "id": user_id, "batch_id": batch_id}
    encode.update({"exp": expires_at})
    encoded_jwt = jwt.encode(encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    email: str, user_id: int, role: str, expires_delta: int | None = None
) -> str:
    if expires_delta is not None:
        expires_at = datetime.now(UTC) + timedelta(days=expires_delta)

    else:
        expires_at = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_MINUTES)
    encode = {"sub": email, "id": user_id, "role": role}
    encode.update({"exp": expires_at})
    encoded_jwt = jwt.encode(encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])


