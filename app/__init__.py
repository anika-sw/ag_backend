from flask import Flask
# from app.routes import hello_world_bp # uncomment for eb
from app.routes import song_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints here
    # app.register_blueprint(hello_world_bp) # uncomment for eb
    app.register_blueprint(song_bp)

    return app