from typing import Dict, Any
from fastapi import Depends, Response, HTTPException, Body
from user.hasher import Hasher, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from user.models import User
from user.schemas import UserRegister, UserSchema
import fastapi_jsonrpc as jsonrpc

user_route = jsonrpc.Entrypoint(path='/api/v1/user')


@user_route.method()
async def register(user: UserRegister) -> dict | Any:
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


@user_route.method()
async def login(response: Response, user: UserSchema = Body(...)) -> dict | Any:
    username, password = user.username, user.password
    if not (username and password):
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        user = User.select().where(username == User.username).get()
        if not user:
            raise HTTPException(status_code=400, detail='Bad Request')
        if Hasher.verify_password(password, user.hashed_password):
            data = {'sub': username}
            token = Hasher.get_encode_token(data)
            response.set_cookie(key='access_token', value=token, httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES)
            return {'detail': 'Authorized'}
    except:
        raise HTTPException(status_code=400, detail='Bad Request')


@user_route.method()
async def current_user(user: User = Depends(get_current_user)) -> str:
    if not user:
        raise HTTPException(status_code=401)
    return f'user: {user.username}'
