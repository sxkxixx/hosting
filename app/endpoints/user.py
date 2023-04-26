import datetime

from fastapi import Depends, Response, HTTPException
from app.utils.hasher import Hasher, get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.models.models import User, Video
from app.core.schemas.schemas import UserRegister, UserSchema
import fastapi_jsonrpc as jsonrpc

user_route = jsonrpc.Entrypoint(path='/api/v1/user')


@user_route.method(tags=['user'])
async def register(user: UserRegister) -> dict:
    email, username, password, password_repeat = user.email.lower(), user.username.lower(), user.password, user.password_repeat
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


@user_route.method(tags=['user'])
async def login(response: Response, user: UserSchema) -> dict:
    email, password = user.email.lower(), user.password
    if not (email and password):
        raise HTTPException(status_code=400, detail='Bad Request')
    # try:
    user = User.select().where(email == User.email).get()
    if not user:
        raise HTTPException(status_code=400, detail='Bad Request')
    if Hasher.verify_password(password, user.hashed_password):
        data = {'sub': email}
        token = Hasher.get_encode_token(data)
        refresh_token = Hasher.get_encode_token(data, datetime.timedelta(hours=2))
        response.set_cookie(key='access_token', value=token, httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, expires=60*60*24)
        return {'user': user.username, 'status': 'Authorized'}
    raise HTTPException(status_code=400, detail='Bad Request')
    # except:
    #     raise HTTPException(status_code=400, detail='Bad Request')


@user_route.method(tags=['user'])
def logout(response: Response, user: User = Depends(get_current_user)) -> dict:
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {'user': user.username if user else 'No user', 'status': 'Logout'}


@user_route.method(tags=['user'])
def profile(user: User = Depends(get_current_user)) -> dict:
    if not user:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        videos = Video.select('id', 'title').where(Video.owner_id == user.id)
    except:
        videos = []
        print(f'no videos')
    context = {
        'username': user.username,
        'email': user.email,
        'videos': [{'id': video.id, 'title': video.title} for video in videos],
        'viewed_videos': user.viewed_videos
    }
    return context


@user_route.method(tags=['user'])
def current_user(user: User = Depends(get_current_user)) -> dict:
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return {'username': user.username}
