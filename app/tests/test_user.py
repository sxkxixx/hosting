import datetime
from app.main import app
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.utils.hasher import Hasher
from app.tests.utils import get_query_params, url

@pytest.mark.asyncio
async def test_register_method():
    email = 'secret@mail.com'
    query_params_register = get_query_params(method='register', body={'user': {
        'username': 'secret', 'email': email, 'password': 'secret', 'password_repeat': 'secret'}})
    query_params_delete = get_query_params(method='delete_user', body={"email": email})
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query_params_register)
            response_delete = await async_client.post(url, json=query_params_delete)
    assert response.status_code == 200
    assert response.json()['result'] == {'detail': f'Пользователь {email} успешно создан'}

    assert response_delete.status_code == 200
    assert response_delete.json()['result'] == 'deleted'


@pytest.mark.asyncio
async def test_register_method_wrong_data():
    query_params_register = get_query_params(method='register', body={'user': {
        'username': 'sec ret', 'email': 'secret@mail.com', 'password': 'incorrect password',
        'password_repeat': 'incorrect password'
    }})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query_params_register)

    assert response.status_code == 200
    assert response.json()['error']['message'] == 'Invalid params'


@pytest.mark.asyncio
async def test_register_method_user_exists():
    query = get_query_params(method='register', body={'user': {
        'username': 'sxkxixx', 'email': 'any_mail@gmail.com', 'password': 'secret', 'password_repeat': 'secret'
    }})
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_register_method_wrong_passwords():
    query = get_query_params(method='register', body={'user': {
        'username': 'nickname', 'email': 'any_mail@gmail.com', 'password': 'secret', 'password_repeat': 'secret1'
    }})
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_register_login_method():
    email = 'secret@mail.com'
    password = 'secret'
    query_params_register = get_query_params(method='register', body={'user': {
        'username': 'username', 'email': email, 'password': password, 'password_repeat': password}})
    query_params_login = get_query_params(method='login', body={'user': {
        'email': email, 'password': password
    }})
    query_params_delete = get_query_params(method='delete_user', body={"email": email})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response_register = await async_client.post(url('user'), json=query_params_register)
            response_login = await async_client.post(url('user'), json=query_params_login)
            response_delete = await async_client.post(url('user'), json=query_params_delete)

    assert response_register.status_code == 200
    assert response_register.json()['result'] == {'detail': f'Пользователь {email} успешно создан'}

    assert response_login.status_code == 200
    assert not response_login.cookies.get('access_token') is None
    assert not response_login.cookies.get('refresh_token') is None
    assert response_login.json()['result'] == {'user': email, 'status': 'Authorized'}

    assert response_delete.status_code == 200
    assert response_delete.json()['result'] == 'deleted'


@pytest.mark.asyncio
async def test_login_method_no_user():
    query = get_query_params(method='login', body={'user': {
        'username': 'nickname', 'email': 'any_mail@gmail.com', 'password': 'password', 'password_repeat': 'password'
    }})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_register_method_sql_injection():
    query_params_register = get_query_params(method='register', body={'user': {
        'username': 'SELECT * FROM users WHERE id=1', 'email': 'secret@mail.com',
        'password': 'SELECT * FROM users WHERE id=1',
        'password_repeat': 'SELECT * FROM users WHERE id=1'}})
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query_params_register)

    assert response.status_code == 200
    assert response.json()['error']['message'] == 'Invalid params'


@pytest.mark.asyncio
async def test_profile_method_no_refresh_token():
    email = 'sasha.kornilov.1212@gmail.com'
    data = {'sub': email}
    token = Hasher.get_encode_token(data)

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(
                url('user'),
                json=get_query_params(method='profile', body={}),
                cookies={'access_token': token}
            )

    assert response.status_code == 401
    assert response.json()['detail'] == 'Unauthorized'


@pytest.mark.asyncio
async def test_profile_method_correct_data():
    email = 'sasha.kornilov.1212@gmail.com'
    data = {'sub': email}
    access_token = Hasher.get_encode_token(data)
    refresh_token = Hasher.get_encode_token(data, datetime.timedelta(hours=2))

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(
                url('user'),
                json=get_query_params(method='profile', body={}),
                cookies={'access_token': access_token, 'refresh_token': refresh_token}
            )

    assert response.status_code == 200
    assert response.json()['result']['email'] == email
