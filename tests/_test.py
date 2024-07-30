import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from app.routes import get_user_inputs
from app import create_app



# def test_say_hello_world(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert response.data == b"Hello, World!"



@pytest.fixture
    # def app_context():
    # with create_app() :  # Replace 'your_app' with your Flask app object
    #     yield
def app_context():
    app = create_app() # Initialize your Flask app 
    with app.app_context(): 
        yield app

def test_get_user_inputs_empty_genre(app_context):
    # Create a mock request object
    mock_request = MagicMock()
    mock_request.get_json.return_value = {'genre': [], 'mood': ['happy'], 'tempo': ['fast']}
    print(mock_request.get_json())
    
    response = get_user_inputs(mock_request)
    print(response)

    assert response[0] == "The 'genre' parameter is required and must be a list containing at least element."
    assert response[1] == 400