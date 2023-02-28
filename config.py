import os


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    MONGODB_DB = os.environ.get("MONGO_DB", "quart_project")
    MONGODB_HOST = os.environ.get("MONGO_HOST", "localhost")
    MONGODB_PORT = int(os.environ.get("MONGO_PORT", 27017))
    MONGODB_TZ_AWARE = False
    MONGODB_ALIAS = "default"
    MONGODB_URL = os.environ.get("MONGO_URL")
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = "3600"
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    CACHE_REDIS_DB = 0
    DRAMATIQ_BROKER = "dramatiq.brokers.redis:RedisBroker"
    DRAMATIQ_BROKER_URL = os.environ.get("DRAMATIQ_BROKER_URL")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_SENDER")
    SESSION_TYPE = "redis"
    SESSION_URI = "redis://localhost:6379"
    UPLOAD_FOLDER = "app/media/"


class ProdConfig(Config):
    SERVER_NAME = "krautsalat.xyz"
    ENV = "production"
    DEBUG = False
    TESTING = False
    MONGODB_USERNAME = os.environ.get("MONGO_USERNAME", None)
    MONGODB_PASSWORD = os.environ.get("MONGO_PASSWORD", None)
    CACHE_REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)


class DevConfig(Config):
    ENV = "dev"
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
    API_KEY = "test-key"
