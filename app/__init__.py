import os
from pathlib import Path

from dotenv import load_dotenv
import motor.motor_asyncio

from quart import Quart


BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    """
    Load in the .env file
    If it exists
    """
    load_dotenv(str(ENV_PATH))

CONFIG_TYPE = os.environ.get("CONFIG_TYPE", "config.DevConfig")

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URL"))
db = client.quart_kraut


# Application Factory
def create_app():
    app = Quart(__name__)

    # Configure the flask app instance
    app.config.from_object(CONFIG_TYPE)

    # Register blueprints
    register_blueprints(app)

    # Register API docs
    register_json_api(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    return app


# Helper functions
def register_blueprints(app):
    from . import home

    app.register_blueprint(home.bp, url_prefix="/")


def register_json_api(app):
    from . import api

    app.register_blueprint(api.bp, url_prefix="/api")


def initialize_extensions(app):
    pass


def register_error_handlers(app):
    pass


def configure_logging(app):
    pass
