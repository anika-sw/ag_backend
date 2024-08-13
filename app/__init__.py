from flask import Flask
from app.routes import song_bp #limiter  # Import limiter here

def create_app():
    app = Flask(__name__)

    # limiter.init_app(app)

    # Register Blueprints here
    app.register_blueprint(song_bp)

    return app