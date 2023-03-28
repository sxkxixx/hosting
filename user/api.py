from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.responses import HTMLResponse
from user.hasher import Hasher
from user.models import User
from user.auth_data import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.templating import Jinja2Templates
from jose import jwt

user_route = APIRouter()
templates = Jinja2Templates(directory='templates')


async def get_current_user(request: Request):
    try:
        username = jwt.decode(request.cookies.get('access_token'), SECRET_KEY, algorithms=[ALGORITHM])['sub']
        user = User.select().where(User.username == username).get()
        return user
    except:
        return None


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
        return templates.TemplateResponse('login.html',
                                          {'request': request, 'message': f'Аккаунт {user.email} успешно создан.'})
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
        if not user:
            errors.append('Нет пользователя с таким именем.')
            return templates.TemplateResponse('login.html', {'request': request, 'errors': errors})
        if Hasher.verify_password(password, user.hashed_password):
            data = {'sub': username}
            token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            message = 'Вход успешно выполнен'
            response = templates.TemplateResponse('login.html', {'request': request, 'message': message})
            response.set_cookie(key='access_token', value=token, httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES)
            return response
    except:
        errors.append('Ой... Что-то пошло не так.')
        return templates.TemplateResponse('login.html', {'request': request, 'errors': errors})


@user_route.get('/user/me')
async def current_user(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail='Пожалуйста, авторизуйтесь или зарегистрируйтесь.')

    return HTMLResponse(f'user: {user.username}')
