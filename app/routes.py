from flask import Blueprint
from flask import Flask

hello_world_bp = Blueprint("hello_world_bp", __name__)

@hello_world_bp.get("/")
def say_hello_world():
    return "Hello, World!"
