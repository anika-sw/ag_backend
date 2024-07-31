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

#================================== TEST 1 ============================================
def test_get_user_inputs_empty_list(app_context):
    # Create a mock request object
    mock_request = MagicMock()
    mock_request.get_json.return_value = {'genre': [], 'mood': ['happy'], 'tempo': ['fast']}
    
    response = get_user_inputs(mock_request)

    assert response[0] == "The 'genre' parameter is required and must be a list containing at least element."
    assert response[1] == 400

#================================== TEST 2 ============================================
def test_get_user_inputs_missing_parameter(app_context):
    mock_request = MagicMock()
    mock_request.get_json.return_value = {'genre': ["edm"], 'tempo': ['slow']}
    
    response = get_user_inputs(mock_request)

    assert response[0] == "The 'mood' parameter is required and must be a list containing at least element."
    assert response[1] == 400

#================================== TEST 3 ============================================
def test_get_user_inputs_not_in_list(app_context):
    mock_request = MagicMock()
    mock_request.get_json.return_value = {'genre': ["country"], 'mood': ["angry"], 'tempo': 'medium'}
    print(mock_request.get_json())
    
    response = get_user_inputs(mock_request)
    print(response)

    assert response[0] == "The 'tempo' parameter is required and must be a list containing at least element."
    assert response[1] == 400