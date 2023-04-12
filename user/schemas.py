from pydantic import BaseModel, EmailStr, validator


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserSchema):
    username: str
    password_repeat: str

