from flask import Blueprint, request, jsonify, make_response, abort
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# FUNCTIONAL HELLO WORLD/ USE FOR DEBUGGING # uncomment for eb
# ==============================================================
# hello_world_bp = Blueprint("hello_world_bp", __name__)

# @hello_world_bp.get("/")
# def say_hello_world():
#     return "Hello, World!"


song_bp = Blueprint("song_bp", __name__)

# GLOBAL VARIABLES (currently hard coded mock for development)
USER_INPUTS = {
    "genre": ["rock", "pop", "edm", "hiphop", "country"],
    "mood": ["happy", "sad", "angry", "romantic", "euphoric"],
    "tempo": ["slow", "medium", "fast"],
  }


# 0) get user inputs from front end
#==============================================================
def get_user_inputs(request):
    """
    This route retrieve the user inputs selected from the drop down menus in the front 
    end when creating a song.

    request body parameters: 
    {
        "genre": ["pop"], #Required
        "mood": ["happy"], #Required
        "tempo": ["medium"] #Required
    }  
    """
    # Extract JSON data from the request body
    if request.method == 'OPTIONS': 
        response = jsonify(status=200)
        response.headers.add('Access-Control-Allow-Origin', 'http://automated-groove-frontend-dev.us-west-2.elasticbeanstalk.com') 
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS') 
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type') 
        
        return response
    
    data = request.get_json()

    try:
        # Extract JSON data from the request body
        data = request.get_json()

        # Extract the genre from the JSON data
        genre = data.get('genre')
        mood = data.get('mood')
        tempo = data.get('tempo')

        # Check to ensure that genre is provided and is a list with a least one item
        if not genre or not isinstance(genre, list) or len(genre) == 0:
            return "The 'genre' parameter is required and must be a list containing at least element.", 400
        if not mood or not isinstance(mood, list) or len(mood) == 0:
            return "The 'mood' parameter is required and must be a list containing at least element.", 400
        if not tempo or not isinstance(tempo, list) or len(tempo) == 0:
            return "The 'tempo' parameter is required and must be a list containing at least element.", 400
        
        return {"genre": genre, "mood": mood, "tempo": tempo}

    except (ValueError, TypeError, KeyError) as e:
        # Handle specific exceptions here
        return {"error": f"Error processing request: {str(e)}"}, 500



# 1) converts user inputs into string to generate NAME PROMPT for ChatGPT
#==============================================================
def generate_song_name_prompt(genre, mood, tempo):
    prompt = f"generate a short song name inspired by a song in the genre of {genre} with a {mood} mood and a {tempo} tempo."

    return prompt

# 2) makes API call to ChatGPT returns NAME
# FUNCTIONAL
# #==============================================================
@song_bp.route('/create_song_name', methods=['POST'])
def generate_song_name_from_api():
    """
    user_input contains:
    {
        "genre": ["pop"],
        "mood": ["happy"],
        "tempo": ["medium"]
    }
    """
    user_input = get_user_inputs(request)
    prompt = generate_song_name_prompt(user_input["genre"][0], user_input["mood"][0], user_input["tempo"][0])
    
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )

    return(completion.choices[0].message.content)

# 3) makes API call to Musicfy AI returns SONG
#==============================================================
@song_bp.route('/create_song', methods=['POST'])
def generate_song_from_api():
    """
    user_input contains:
    {
        "genre": ["pop"],
        "mood": ["happy"],
        "tempo": ["medium"]
    }
    """
    user_input = get_user_inputs(request)

        # Call to musicfy API to generate a song
    url = "https://api.musicfy.lol/v1/generate-music"

    if isinstance(user_input, dict):
        payload = {"prompt": f"Create a song in the genre of {user_input['genre'][0]} with a {user_input['mood'][0]} mood and a {user_input['tempo'][0]} tempo.",}
        headers = {"Content-Type": "application/json", "Authorization": os.getenv("MUSICFY_API_KEY")}

        response = requests.request("POST", url, json=payload, headers=headers)

        return jsonify(response.text)
    
    else:
        return user_input


