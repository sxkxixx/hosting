import pytest_asyncio
from main import app
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from tests.utils import get_query_params, ADMIN_PASSWORD, url, TEST_USER_EMAIL, TEST_USER_PASSWORD, ADMIN_EMAIL


# -p no:cacheprovider

@pytest_asyncio.fixture()
async def auth_admin_tokens():
    query_login = get_query_params(method='login',
                                   body={'user': {'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query_login)

    access_token = response.cookies.get('access_token')
    refresh_token = response.cookies.get('refresh_token')
    return {'access_token': access_token, 'refresh_token': refresh_token}


@pytest_asyncio.fixture()
async def auth_user_tokens():
    query_login = get_query_params(method='login',
                                   body={'user': {'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query_login)

    access_token = response.cookies.get('access_token')
    refresh_token = response.cookies.get('refresh_token')
    return {'access_token': access_token, 'refresh_token': refresh_token}


@pytest.mark.asyncio
async def test_admin_login():
    query = get_query_params(method='admin_login',
                             body={'admin_schema': {'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('admin'), json=query)

    assert response.status_code == 200
    assert not response.cookies.get('access_token') is None
    assert not response.cookies.get('refresh_token') is None
    assert response.json()['result']['user'] == ADMIN_EMAIL


@pytest.mark.asyncio
async def test_admin_login_wrong_data():
    query = get_query_params(method='admin_login',
                             body={'admin_schema': {'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('admin'), json=query)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_admin_login_no_user():
    query = get_query_params(method='admin_login',
                             body={'admin_schema': {'email': 'any_user@gmail.com', 'password': 'any_password'}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('admin'), json=query)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_admin_create_show_claims(auth_user_tokens, auth_admin_tokens):
    claim_ids = []
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            for i in range(5):
                query = get_query_params(method='create_claim', body={
                    'claim': {'description': f'Жалоба {i + 1}', 'claim_type': 'video', 'claim_object_id': 1}
                })
                response = await async_client.post(url('user'), json=query, cookies=auth_user_tokens)
                id = response.json()['result']['claim']['id']
                claim_ids.append(id)

    query = get_query_params(method='admin_claims', body={})
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('admin'), json=query, cookies=auth_admin_tokens)

    for claim_id, claim in zip(claim_ids, response.json()['result']):
        assert claim_id == claim['claim_id']

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            for id in claim_ids:
                query = get_query_params(method='delete_claim', body={'claim_id': id})
                response_delete = await async_client.post(url('admin'), json=query, cookies=auth_admin_tokens)



