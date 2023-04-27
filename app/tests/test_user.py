from app.main import app
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

url = 'http://127.0.0.1:8000/api/v1/user'


def get_query_params(method: str, body):
    return {"jsonrpc": "2.0", "id": 0, "method": method, "params": body}


@pytest.mark.asyncio
async def test_register_method():
    email = 'secret@mail.com'
    query_params_register = get_query_params(method='register', body={'user': {'username': 'secret', 'email': email,
                                                                               'password': 'secret',
                                                                               'password_repeat': 'secret'}})
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url, json=query_params_register)
    assert response.status_code == 200
    assert response.json()['result'] == {'detail': f'Пользователь {email} успешно создан'}

    query_params_delete = get_query_params(method='delete_user', body={"email": email})
    async with LifespanManager(app):
        async with AsyncClient(app=app) as async_client:
            response = await async_client.post(url, json=query_params_delete)
    assert response.status_code == 200
    assert response.json()['result'] == 'deleted'

