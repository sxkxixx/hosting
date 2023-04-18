from passlib.context import CryptContext
from fastapi import Request
from jose import jwt
from app.user.models import User
from app.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)

    @staticmethod
    def get_encode_token(data):
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return token


def get_current_user(request: Request):
    try:
        user_email = jwt.decode(request.cookies.get('access_token'), SECRET_KEY, algorithms=[ALGORITHM])['sub']
        user = User.select().where(User.email == user_email).get()
        return user
    except:
        return None
