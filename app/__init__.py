import os
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from quart import Quart, send_from_directory
from quart_schema import QuartSchema
from quart_session import Session


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    """
    Load in the .env file
    If it exists
    """
    load_dotenv(str(ENV_PATH))

CONFIG_TYPE = os.environ.get("CONFIG_TYPE", "config.DevConfig")

# Set up Motor client
client = AsyncIOMotorClient(os.environ.get("MONGO_URL"))

# Quart Extensions
quart_schema = QuartSchema()
sesh = Session()


# Application Factory
def create_app():
    app = Quart(__name__)

    # Configure the quart app instance
    app.config.from_object(CONFIG_TYPE)

    @app.get("/media/<path:path>")
    async def send_media(path):
        """
        :param path: a path like "posts/<int:post_id>/<filename>"
        """

        return await send_from_directory(
            directory=app.config["UPLOAD_FOLDER"],
            file_name=path,
            as_attachment=True,
        )

    # Register blueprints
    register_blueprints(app)

    # Register API docs
    register_json_api(app)

    # Initialize quart extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    app.session_interface.serialize = pickle

    return app


# Helper functions
def register_blueprints(app):
    from . import auth, home

    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(home.bp, url_prefix="/")


def register_json_api(app):
    from . import api

    app.register_blueprint(api.bp, url_prefix="/api")


def initialize_extensions(app):
    quart_schema.init_app(app)
    sesh.init_app(app)


def register_error_handlers(app):
    pass


def configure_logging(app):
    pass
