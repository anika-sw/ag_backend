import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from app.routes import get_user_inputs, generate_song_name_prompt
from app import create_app
import os



# def test_say_hello_world(client):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert response.data == b"Hello, World!"



@pytest.fixture
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
    
    response = get_user_inputs(mock_request)

    assert response[0] == "The 'tempo' parameter is required and must be a list containing at least element."
    assert response[1] == 400

#================================== TEST 4 ============================================
def test_song_name_prompt_parameters_match():
    genre = "pop"
    mood = "happy"
    tempo = "medium"

    response = generate_song_name_prompt(genre, mood, tempo)

    assert response == "generate a short song name inspired by a song in the genre of pop with a happy mood and a medium tempo."

#================================== TEST 5 ============================================
def test_generate_song_from_api_is_called_once(client):
    # Mock the external API call
    with patch('requests.request') as mock_request:  # Mock requests.request instead of requests.post

        # Set up the mock response object
        mock_response = MagicMock()
        mock_response.json.return_value = {'song_data': 'mocked song data'}   # Switch to .json() instead of .text
        mock_request.return_value = mock_response
        
        # Set up test data
        test_data = {
            "genre": ["pop"],
            "mood": ["happy"],
            "tempo": ["medium"]
        }
        
        # Make a POST request to the /create_song endpoint
        response = client.post('/create_song', json=test_data)
        
        # Assert the external API was called with the expected payload and headers
        expected_payload = {
            "prompt": "Create a song in the genre of pop with a happy mood and a medium tempo."
        }
        expected_headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv("MUSICFY_API_KEY")
        }
        
        mock_request.assert_called_once_with(
            "POST",
            "https://api.musicfy.lol/v1/generate-music",
            json=expected_payload,
            headers=expected_headers
        )
        
        # Assert the response from the Flask endpoint
        assert response.status_code == 200
        assert response.get_json() == {'song_data': 'mocked song data'}
        # Ensures the API has been called only once
        assert mock_request.call_count == 1