import pytest_asyncio
from app.main import app
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.utils.hasher import Hasher

TEST_USER_EMAIL = 'test@mail.com'
TEST_USER_PASSWORD = 'secret'
TEST_VIDEO_ID = 1


def url(route):
    return f'http://127.0.0.1:8000/api/v1/{route}'


def get_query_params(method: str, body):
    return {"jsonrpc": "2.0", "id": 0, "method": method, "params": body}


# -p no:cacheprovider

@pytest_asyncio.fixture()
async def auth_tokens():
    query_login = get_query_params(method='login',
                                   body={'user': {'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD}})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('user'), json=query_login)

    access_token = response.cookies.get('access_token')
    refresh_token = response.cookies.get('refresh_token')
    return {'access_token': access_token, 'refresh_token': refresh_token}


@pytest.mark.asyncio
async def test_upload_delete_comment(auth_tokens):
    query_upload_comment = get_query_params(method='upload_comment', body={
        'comment_data': {'video_id': TEST_VIDEO_ID, 'comment_text': 'pytest_test_description'}
    })
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response_upload = await async_client.post(url('video'), json=query_upload_comment, cookies=auth_tokens)

    assert response_upload.status_code == 200
    assert response_upload.json()['result']['status'] == 'uploaded'
    comment_id = response_upload.json()['result']['comment']
    query_delete_comment = get_query_params(method='delete_comment', body={'comment_id': comment_id})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response_delete = await async_client.post(url('video'), json=query_delete_comment, cookies=auth_tokens)

    assert response_delete.status_code == 200
    assert response_delete.json()['result']['status'] == 'deleted'


@pytest.mark.asyncio
async def test_likes_methods(auth_tokens):
    query = get_query_params(method='change_like_status', body={'video_id': TEST_VIDEO_ID})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response_add = await async_client.post(url('video'), json=query, cookies=auth_tokens)
            response_remove = await async_client.post(url('video'), json=query, cookies=auth_tokens)

    assert response_add.status_code == 200
    assert response_add.json()['result']['status'] == 'Added'

    assert response_remove.status_code == 200
    assert response_remove.json()['result']['status'] == 'Removed'


@pytest.mark.asyncio
async def test_like_method_no_video(auth_tokens):
    query = get_query_params(method='change_like_status', body={'video_id': -TEST_VIDEO_ID})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('video'), json=query, cookies=auth_tokens)

    assert response.status_code == 400
    assert response.json()['detail'] == 'Bad Request'


@pytest.mark.asyncio
async def test_like_method_no_user():
    query = get_query_params(method='change_like_status', body={'video_id': TEST_VIDEO_ID})

    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url('video'), json=query)

    assert response.status_code == 401
    assert response.json()['detail'] == 'Unauthorized'


@pytest.mark.asyncio
async def test():
    pass
