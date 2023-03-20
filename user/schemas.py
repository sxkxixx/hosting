from pydantic import BaseModel


class UserScheme(BaseModel):
    # id: str | None = None
    username: str
    # email: str
    # role: int
    is_active: bool | None = None
    # is_superuser: bool = False


class UserInDB(UserScheme):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
