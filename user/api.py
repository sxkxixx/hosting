from fastapi import APIRouter, Depends, Response, Request, HTTPException
from user.hasher import Hasher
from user.models import User
from user.auth_data import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from user.schemas import UserRegister, UserSchema

user_route = APIRouter()


async def get_current_user(request: Request):
    try:
        username = jwt.decode(request.cookies.get('access_token'), SECRET_KEY, algorithms=[ALGORITHM])['sub']
        user = User.select().where(User.username == username).get()
        return user
    except:
        return None


@user_route.post('/register')
async def register(user: UserRegister):
    email, username, password, password_repeat = user.email, user.username, user.password, user.password_repeat
    try:
        user_by_data = User.select().where(User.email == email or User.username == username).get()
    except:
        user_by_data = None
    if user_by_data or password != password_repeat:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        user = User.create(
            username=username,
            email=email,
            hashed_password=Hasher.get_hash_password(password),
            role=1,
        )
        user.save()
        return {'status': 200, 'detail': 'Пользователь {} успешно создан'.format(user.username)}
    except:
        raise HTTPException(status_code=400, detail='Bad Request')


@user_route.post('/login')
async def login(user: UserSchema, response: Response):
    username, password = user.username, user.password
    if not (username and password):
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        user = User.select().where(username == User.username).get()
        if not user:
            raise HTTPException(status_code=400, detail='Bad Request')
        if Hasher.verify_password(password, user.hashed_password):
            data = {'sub': username, 'role': user.role.id}
            token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            response.set_cookie(key='access_token', value=token, httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES)
            return Response({'status': 200, 'detail': 'Пользователь авторизован.'})
    except:
        raise HTTPException(status_code=400, detail='Bad Request')


@user_route.get('/user/me')
async def current_user(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401)

    return Response(f'user: {user.username}')
