from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from user.auth import get_current_active_user, authenticate_user, create_access_token
from user.hasher import Hasher
from user.models import User
from user.schemas import Token
from user.auth_data import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi.templating import Jinja2Templates
from jose import jwt

user_route = APIRouter()
templates = Jinja2Templates(directory='templates')


@user_route.post("/token/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_route.post('/register')
async def register(request: Request):
    form = await request.form()
    email, username, password, repeat_password = form.get('email'), form.get('username'), form.get(
        'password'), form.get('repeat_password')
    try:
        user_by_data = User.select().where(User.email == email or User.username == username).get()
    except:
        user_by_data = None
    if user_by_data:
        return templates.TemplateResponse('register.html',
                                          {'request': request, 'message': 'Имя пользователя или почта не валидны'})
    if password != repeat_password:
        return templates.TemplateResponse('register.html', {'request': request, 'message': 'Пароли не совпадают'})
    try:
        user = User.create(
            username=username,
            email=email,
            hashed_password=Hasher.get_hash_password(password),
            role=1,
        )
        user.save()
        return templates.TemplateResponse('login.html', {'request': request, 'message': f'Аккаунт {user.username} успешно создан.'})
    except:
        return templates.TemplateResponse('register.html', {'request': request, 'message': 'Что-то пошло не так'})


@user_route.post('/login')
async def login(response: Response, request: Request):
    form = await request.form()
    username, password = form.get('username'), form.get('password')
    errors = []
    if not (username and password):
        errors.append('Введите корректные данные.')
        return templates.TemplateResponse('login.html', {'request': request, "errors": errors})
    try:
        user = User.select().where(username == User.username).get()
        print(user)
        if not user:
            errors.append('Нет пользователя с таким именем.')
            return templates.TemplateResponse('login.html', {'request': request, 'errors': errors})
        if Hasher.verify_password(password, user.hashed_password):
            data = {'sub': username}
            token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            message = 'Вход успешно выполнен'
            response = templates.TemplateResponse('login.html', {'request': request, 'message': message})
            response.set_cookie(key='access_token', value=f'Bearer {token}', httponly=True)
            return response
    except:
        errors.append('Ой... Что-то пошло не так.')
        return templates.TemplateResponse('login.html', {'request': request, 'errors': errors})


@user_route.get('/users/me')
async def read_users_me(current_user: Annotated[str, Depends(get_current_active_user)]):
    return current_user
