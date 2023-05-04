def url(route):
    return f'http://127.0.0.1:8000/api/v1/{route}'


def get_query_params(method: str, body):
    return {"jsonrpc": "2.0", "id": 0, "method": method, "params": body}


# -p no:cacheprovider
ADMIN_EMAIL = 'admin_test@gmail.com'
ADMIN_PASSWORD = 'ADMINSECRET'
TEST_USER_EMAIL = 'test@mail.com'
TEST_USER_PASSWORD = 'secret'
TEST_VIDEO_ID = 1