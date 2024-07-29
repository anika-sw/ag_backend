from flask import Blueprint, request, jsonify, make_response, abort
import os
import requests
# from openai import OpenAI

# client = OpenAI()

# FUNCTIONAL HELLO WORLD 
#==============================================================
# hello_world_bp = Blueprint("hello_world_bp", __name__)

# @hello_world_bp.get("/")
# def say_hello_world():
#     return "Hello, World!"


song_bp = Blueprint("song_bp", __name__)

# GLOBAL VARIABLES (currently hard coded mock for development)
USER_INPUTS = {
    "genre": ["pop"],
  }


# 0) get user inputs from front end
#==============================================================
@song_bp.route('/get_user_inputs', methods=['POST'])
def get_user_inputs():
    """
    This route retrieve the user inputs selected from the drop down menus in the front 
    end when creating a song.

    request body parameters: 
    {
        "genre": ["pop", "country"], #Required 
    }  
    """
    # Extract JSON data from the request body
    data = request.get_json()

    # Extract the genre from the JSON data
    genre = data.get('genre')

    # Check to ensure that genre is provided and is a list
    if not genre or not isinstance(genre, list):
        return jsonify({"error": "The 'genre' parameter is required and must be a list."}), 400


    # Return the matched value
    return jsonify({"genre": genre})

# user_inputs = {
#     "genre": ["pop", "country"], #Required 
#     "instrument": ["guitar", "piano"], #Optional
# }


# 1) converts user inputs into string prompt for ChatGPT to generate NAME PROMPT
#==============================================================
def generate_song_name_prompt():
    prompt = f"generate a short song name inspired by: {USER_INPUT['selections']}"

    return prompt


# 2) makes API call to ChatGPT returns NAME
# #==============================================================
def generate_song_name_from_api():
    prompt = generate_song_name_prompt()
    
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )

    return(completion.choices[0].message.content)

#==============================================================
# 3) converts user inputs into string prompt for Musicfy AI to generate SONG PROMPT


# 4) makes API call to Musicfy AI returns SONG
#==============================================================
