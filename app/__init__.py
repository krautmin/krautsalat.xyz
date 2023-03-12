import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from quart import Quart
from quart_schema import Info, QuartSchema
from quart_session import Session

from app.documents import beanie_init_list
from app.utils import get_task_queue

version = "v0.2.6"

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"

if env_path.exists():
    """
    Load in the .env file
    If it exists
    """
    load_dotenv(str(env_path))

quart_schema = QuartSchema(
    info=Info(title="krautsalat.xyz API", version=version),
    security=[{"token": []}],
    security_schemes={"token": {"type": "apiKey", "name": "x-api-key", "in": "header"}},
)
sesh = Session()


# Application Factory
def create_app():
    app = Quart(__name__)

    # Configure the quart app instance
    app.config.from_object(os.environ.get("CONFIG_TYPE", None))

    @app.before_serving
    async def init_db():
        client = AsyncIOMotorClient(app.config["MONGODB_URL"])
        await init_beanie(
            database=client.quart_kraut,
            document_models=beanie_init_list,
        )

    @app.before_serving
    async def init_task_queue():
        await get_task_queue()

    # Register context processors
    register_context_processors(app)

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
def register_context_processors(app):
    @app.context_processor
    def inject_today_date():
        return {"date": datetime.date.today()}


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
