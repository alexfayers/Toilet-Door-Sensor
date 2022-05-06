from flask import Flask
from config import (
    LISTENER_HOST,
    LISTENER_PORT,
    DEBUG_MODE
)

# blueprints
from src.routes.api import api
from src.routes.home import main

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
app.register_blueprint(api)
app.register_blueprint(main)


if __name__ == '__main__':
    app.run(host=LISTENER_HOST, port=LISTENER_PORT, debug=DEBUG_MODE)
