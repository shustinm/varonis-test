import pytest
from main import create_app
from pytest_sanic.plugin import TestClient


@pytest.fixture
def app():
    yield create_app()


@pytest.fixture
def run_app(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture
async def access_token(run_app: TestClient):
    res = await run_app.post('/auth', json={'username': 'michael', 'password': '123'})
    access_token = res.json()['access_token']
    yield access_token


@pytest.fixture
def auth_header(run_app: TestClient, access_token):
    return {'Authorization': f'Bearer {access_token}'}


async def test_auth(run_app: TestClient, auth_header):
    res = await run_app.get('/auth/verify', headers=auth_header)
    assert res.json()['valid']


async def test_normalize(run_app: TestClient, auth_header):
    json_data = [
        {
            "name": "device",
            "strVal": "iPhone",
            "metadata": "not interesting"
        },
        {
            "name": "isAuthorized",
            "boolVal": "false",
            "lastSeen": "not interesting"
        }
    ]
    res = await run_app.post('/normalize', json=json_data, headers=auth_header)

    assert res.json() == {
        "device": "iPhone",
        "isAuthorized": "false"
    }