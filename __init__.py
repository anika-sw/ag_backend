from flask import Flask
from application import hello_world_bp

def create_app():
    application = Flask(__name__)

    # Register Blueprints here
    application.register_blueprint(hello_world_bp)

    return application