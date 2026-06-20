from flask import Blueprint, request, jsonify, send_from_directory
import os
import uuid
import requests
from dotenv import load_dotenv
from openai import OpenAI
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

load_dotenv()
client = OpenAI()
# limiter = Limiter(
#     get_remote_address,
#     default_limits=["1 per day"],
#     storage_uri="redis://localhost:6379",
# )

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
SONG_DIR = os.path.join(os.getcwd(), "generated_songs")
os.makedirs(SONG_DIR, exist_ok=True)

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
# @limiter.limit("1 per day", override_defaults=True)
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

# 3) makes API call to ElevenLabs and returns SONG
#==============================================================
def build_music_prompt(genre, mood, tempo):
    return (
        f"Create a {mood}, {genre} instrumental background track "
        f"with a {tempo} tempo. "
        "Make it suitable for content creators, social media videos, "
        "podcasts, or background use. "
        "No vocals, no lyrics, no copyrighted artist references. "
        "Use a clean intro, steady groove, and natural ending."
    )

@song_bp.route('/create_song', methods=['POST'])
# @limiter.limit("1 per day", override_defaults=True)
def generate_song_from_api():
    user_input = get_user_inputs(request)
    if "error" in user_input:
        return jsonify(user_input), user_input.get("status", 400)

    genre = user_input["genre"][0]
    mood = user_input["mood"][0]
    tempo = user_input["tempo"][0]

    prompt = build_music_prompt(genre, mood, tempo)

    response = requests.post(
        "https://api.elevenlabs.io/v1/music",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt,
            "music_length_ms": 30000,
            "model_id": "music_v2",
            "force_instrumental": True,
        },
        timeout=180,
    )

    if not response.ok:
        return jsonify({
            "error": "ElevenLabs music generation failed",
            "status": response.status_code,
            "detail": response.text,
        }), response.status_code

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(SONG_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    return jsonify([
        {
            "file_url": f"/songs/{filename}",
            "type": "music",
            "prompt": prompt,
            "provider": "elevenlabs",
        }
    ])

@song_bp.route('/songs/<filename>')
def get_song(filename):
    response = send_from_directory(SONG_DIR, filename)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 4) makes API call to Google reCAPTCHA server to verify a users reCAPTCHA response
#==============================================================
@song_bp.route('/verify-recaptcha', methods=['POST'])
# @limiter.limit("1 per day", override_defaults=True)
def verify_recaptcha():
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Missing captcha token"}), 400

    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": os.getenv("RECAPTCHA_SECRET_KEY"),
        "response": token,
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to verify captcha"}), 500
