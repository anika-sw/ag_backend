from flask import Flask
from flask_cors import CORS
# from app.routes import hello_world_bp # uncomment for eb
from app.routes import song_bp
from flask_executor import Executor # Import Executor to handle async processing

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize Executor
    executor = Executor(app)

    # Register Blueprints here
    # app.register_blueprint(hello_world_bp) # uncomment for eb
    app.register_blueprint(song_bp)

    return app