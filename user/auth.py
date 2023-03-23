from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError
from user.auth_data import SECRET_KEY, ALGORITHM
from user.schemas import UserScheme, UserInDB
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from user.models import User

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    try:
        user = UserInDB(**User.select().where(username == User.username).dicts()[0])
    except:
        user = None
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return UserScheme(username=user.username)


def get_user(username: str):
    try:
        return UserInDB(**User.select().where(username == User.username).dicts()[0])
    except:
        return None


async def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return UserScheme(username=user.username, is_active=user.is_active)


async def get_current_active_user(current_user: Annotated[UserScheme, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
