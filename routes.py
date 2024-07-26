from flask import Blueprint
from flask import Flask

hello_world_bp = Blueprint("hello_world_bp", __name__)

def create_app():
    application = Flask(__name__)

    # Register Blueprints here
    application.register_blueprint(hello_world_bp)

    return application

@hello_world_bp.get("/")
def say_hello_world():
    return "Hello, World!"
