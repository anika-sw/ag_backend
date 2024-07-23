import pytest

@pytest.fixture
def test_say_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Hello, World!"