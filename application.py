from flask import Blueprint

hello_world_bp = Blueprint("hello_world_bp", __name__)
application = Flask(__name__)

# Register Blueprints here
application.register_blueprint(hello_world_bp)

@hello_world_bp.get("/")
def say_hello_world():
    return "Hello, World!"