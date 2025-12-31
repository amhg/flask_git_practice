import pytest
#import pytest_asyncio
from app import create_app
#from httpx import AsyncClient

@pytest.fixture
def client():
    app = create_app('../config_test.toml')
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json["message"] == "pong"


"""
def test_async_route(client):
    response = client.get("/async")
    print(f"response : {response.status_code}")
"""



