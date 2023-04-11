from passlib.context import CryptContext
from fastapi import Request
from jose import jwt
from user.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = '6a4d3ef4988a34a29b1bbcbbc895fa6cbbd4df36cf545ee3b6119b8c172946da'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60


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


async def get_current_user(request: Request):
    try:
        username = jwt.decode(request.cookies.get('access_token'), SECRET_KEY, algorithms=[ALGORITHM])['sub']
        user = User.select().where(User.username == username).get()
        return user
    except:
        return None
