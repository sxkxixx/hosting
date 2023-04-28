from app.main import app
import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.utils.hasher import Hasher

url = 'http://127.0.0.1:8000/api/v1/video'


def get_query_params(method: str, body):
    return {"jsonrpc": "2.0", "id": 0, "method": method, "params": body}
