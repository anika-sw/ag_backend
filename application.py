from flask import Blueprint

hello_world_bp = Blueprint("hello_world_bp", __name__)

@hello_world_bp.get("/")
def say_hello_world():
    return "Hello, World!"