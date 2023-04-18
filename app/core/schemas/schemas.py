from fastapi import File
from pydantic import BaseModel, EmailStr, validator
import string


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserSchema):
    username: str
    password_repeat: str

    @validator('username', 'password_repeat', 'email')
    def no_space_validator(cls, v, values, **kwargs):
        if ' ' in v:
            raise ValueError(f'No space in "{kwargs["field"].name.capitalize()}"')
        return v

    @validator('password', 'password_repeat')
    def password_len_validator(cls, v, values, **kwargs):
        if len(v) < 12:
            raise ValueError(f'{kwargs["field"].name.capitalize()} must be longer then 12 symbols')
        return v

    @validator('password', 'password_repeat')
    def password_symbols_validator(cls, v, values, **kwargs):
        return v


class VideoUploadSchema(BaseModel):
    title: str
    description: str
    video_file: bytes = File(...)


class CommentUploadSchema(BaseModel):
    video_id: int
    comment_text: str
