from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from user.api import get_current_user
from user.models import User

template_route = APIRouter()
templates = Jinja2Templates(directory='templates')


@template_route.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@template_route.get('/register')
def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})


@template_route.get('/profile')
async def profile(request: Request, user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail='Пожалуйста, авторизуйтесь или зарегистрируйтесь.')
    return templates.TemplateResponse('profile.html', context={'request': request, 'user': user})


@template_route.get('/test_upload_video')
def upload_video(request: Request):
    return templates.TemplateResponse('upload_video.html', {'request': request})
