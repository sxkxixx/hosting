import pytest_asyncio
from app.main import app
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.tests.utils import ADMIN_EMAIL, ADMIN_PASSWORD, url, get_query_params, TEST_USER_EMAIL, TEST_USER_PASSWORD


# -p no:cacheprovider

@pytest_asyncio.fixture()
async def auth_tokens():
    query_login = get_query_params(method='login',
                                   body={'user': {'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query_login)

    access_token = response.cookies.get('access_token')
    refresh_token = response.cookies.get('refresh_token')
    return {'access_token': access_token, 'refresh_token': refresh_token}


@pytest.mark.asyncio
async def test_admin_login():
    query = get_query_params(method='admin_login', body={'admin_schema': {'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('admin'), json=query)

    assert response.status_code == 200
    assert not response.cookies.get('access_token') is None
    assert not response.cookies.get('refresh_token') is None
    assert response.json()['result']['user'] == ADMIN_EMAIL


@pytest.mark.asyncio
async def test_admin_login_wrong_data():
    query = get_query_params(method='admin_login', body={'admin_schema': {'email': TEST_USER_EMAIL, 'password': TEST_USER_EMAIL}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('admin'), json=query)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_admin_login_no_user():
    query = get_query_params(method='admin_login', body={'admin_schema': {'email': 'any_user@gmail.com', 'password': 'any_password'}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('admin'), json=query)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


