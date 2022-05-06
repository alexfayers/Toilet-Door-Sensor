from flask import Flask
from config import (
    LISTENER_HOST,
    LISTENER_PORT,
    DEBUG_MODE
)
from src.helper.status_ingest import monitor

# blueprints
from src.routes.api import api
from src.routes.home import main


class AppFactory:
    def __init__(self):
        self.app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
        self.register_blueprints()

        monitor()

    def register_blueprints(self):
        self.app.register_blueprint(api)
        self.app.register_blueprint(main)

    def get_app(self):
        return self.app

    def run(self):
        self.app.run(
            host=LISTENER_HOST,
            port=LISTENER_PORT,
            debug=DEBUG_MODE
        )


factory = AppFactory()
app = factory.get_app()


if __name__ == '__main__':
    factory.run()
