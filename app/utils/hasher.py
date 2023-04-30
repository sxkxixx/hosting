import datetime
from passlib.context import CryptContext
from fastapi import Request, Response
from jose import jwt
from app.core.models.models import User
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)

    @staticmethod
    def get_encode_token(data: dict, expires_in: datetime.timedelta | None = None):
        to_encode_data = data.copy()
        if not expires_in:
            expires_in = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode_data.update({'expire': str(datetime.datetime.utcnow() + expires_in)})
        token = jwt.encode(to_encode_data, key=SECRET_KEY, algorithm=ALGORITHM)
        return token


def update_token(response: Response, data: dict, token_type: str,
                 expire: int):
    response.delete_cookie(token_type)
    token = Hasher.get_encode_token(data)
    response.set_cookie(key=token_type, value=token, httponly=True, expires=expire)


async def get_current_user(request: Request, response: Response) -> User | None:
    token = request.cookies.get('access_token', None)
    refresh_token = request.cookies.get('refresh_token', None)
    if not refresh_token:
        return None
    if not token:
        token = request.cookies.get('refresh_token')
        if not token:
            return None
        email = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])['sub']
        update_token(response, {'sub': email}, 'access_token', ACCESS_TOKEN_EXPIRE_MINUTES)
    try:
        email = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])['sub']
    except:
        email = None
    if email:
        try:
            user = await User.objects.get(User.email == email)
            return user
        except:
            return None
    return None
