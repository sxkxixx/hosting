from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    password: str


class UserRegister(UserSchema):
    email: EmailStr
    password_repeat: str
