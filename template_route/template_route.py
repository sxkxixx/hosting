from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

template_route = APIRouter()
templates = Jinja2Templates(directory='templates')


@template_route.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})


@template_route.get('/register')
def register(request: Request):
    return templates.TemplateResponse('register.html', context={'request': request})
