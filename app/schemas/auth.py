from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class ForgotPassword(BaseModel):
    password: str
    password2: str


class ChangePassword(BaseModel):
    current_password: str
    password: str
    password2: str


class Token(BaseModel):
    access_token: str
    token_type: str
