from fastapi import File, UploadFile, Form
from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserSchema):
    username: str
    password_repeat: str

    @validator('username', 'password_repeat', 'email', 'password')
    def no_space_validator(cls, v, values, **kwargs):
        if ' ' in v:
            raise ValueError(f'No space in "{kwargs["field"].name.capitalize()}"')
        return v

    @validator('password', 'password_repeat')
    def password_len_validator(cls, v, values, **kwargs):
        if len(v) < 6:
            raise ValueError(f'{kwargs["field"].name.capitalize()} must be longer then 12 symbols')
        return v

    @validator('password', 'password_repeat')
    def password_symbols_validator(cls, v, values, **kwargs):
        return v


class VideoUploadSchema(BaseModel):
    title: str = Form(...)
    description: str = Form(...)
    video_file: UploadFile = File(...)
    preview_file: Optional[UploadFile | None] = File(...)


class CommentUploadSchema(BaseModel):
    video_id: int
    comment_text: str

    @validator('video_id', 'comment_text')
    def validate(cls, v, values, **kwargs):
        if not v:
            raise ValueError(f'Enter {kwargs["field"].name.capitalize()}')
        return v


class ClaimSchema(BaseModel):
    description: str
    claim_type: str
    claim_object_id: int

    @validator('description', 'claim_type', 'claim_object_id')
    def validate(cls, v, values, **kwargs):
        if not v:
            raise ValueError(f'Enter {kwargs["field"].name.capitalize()}')
        return v