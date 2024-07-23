import pytest
from app import create_app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

