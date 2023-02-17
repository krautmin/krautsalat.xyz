from dotenv import load_dotenv
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    DEPLOYED = os.environ.get("DEPLOYED") == "1"
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    MONGODB_DB = os.environ.get("MONGO_DB", "flask_project")
    MONGODB_HOST = os.environ.get("MONGO_HOST", "localhost")
    MONGODB_PORT = int(os.environ.get("MONGO_PORT", 27017))
    MONGODB_TZ_AWARE = False
    MONGODB_ALIAS = "default"


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    MONGODB_USERNAME = os.environ.get("MONGO_USERNAME", None)
    MONGODB_PASSWORD = os.environ.get("MONGO_PASSWORD", None)
    SERVER_NAME = "krautsalat.xyz"


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    DEBUG_TB_PANELS = (
        "flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel",
        "flask_debugtoolbar.panels.g.GDebugPanel",
        "flask_debugtoolbar.panels.headers.HeaderDebugPanel",
        "flask_debugtoolbar.panels.logger.LoggingPanel",
        "flask_debugtoolbar.panels.profiler.ProfilerDebugPanel",
        "flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel",
        "flask_debugtoolbar.panels.route_list.RouteListDebugPanel",
        "flask_debugtoolbar.panels.template.TemplateDebugPanel",
        "flask_debugtoolbar.panels.timer.TimerDebugPanel",
        "flask_debugtoolbar.panels.versions.VersionDebugPanel",
        "flask_mongoengine.panels.MongoDebugPanel",
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False
