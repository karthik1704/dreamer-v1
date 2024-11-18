import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserSchema(BaseModel):
    id:int
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    email: EmailStr
    phone: Optional[str]

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: Optional[EmailStr] = Field(None, description="Invalid E-mail")
    password: str
    password2: str
    phone: str
   

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 4 characters long")
        if len(value) > 20:
            raise ValueError("Username must be at most 20 characters long")
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores"
            )
        return value

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if value == "":
            return None
        return value


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: Optional[EmailStr] = None
    phone: str
  

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 4 characters long")
        if len(value) > 20:
            raise ValueError("Username must be at most 20 characters long")
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError(
                "Username can only contain letters, numbers, and underscores"
            )
        return value

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if value == "":
            return None
        return value
