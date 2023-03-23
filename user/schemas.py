from pydantic import BaseModel


class UserScheme(BaseModel):
    username: str
    is_active: bool | None = None


class UserInDB(UserScheme):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
