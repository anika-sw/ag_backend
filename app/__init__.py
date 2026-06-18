from flask import Flask
from flask_cors import CORS
from app.routes import song_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "https://automated-groove.vercel.app"}})

    # Register Blueprints here
    app.register_blueprint(song_bp)

    return app
