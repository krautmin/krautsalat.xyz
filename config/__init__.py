import os


class Config:
    SECRET_KEY = os.environ.get("QUART_SECRET_KEY")
    MONGODB_URL = os.environ.get("MONGO_URL")
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = "3600"
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(os.environ.get("REDIS_DB", 0))
    CACHE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
    SESSION_TYPE = "redis"
    SESSION_URI = CACHE_REDIS_URL
    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = int(os.environ.get("SMTP_PORT"))
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
    MAIL_TO = os.environ.get("MAIL_TO")


class ProdConfig(Config):
    SERVER_NAME = "krautsalat.xyz"
    ENV = "production"
    DEBUG = False
    TESTING = False
    CACHE_REDIS_PASSWORD = os.environ.get("REDIS_PW", None)
    API_KEY = os.environ.get("QUART_API_KEY", None)
    UPLOAD_FOLDER = "/app/app/media/"


class DevConfig(Config):
    ENV = "dev"
    DEBUG = True
    TESTING = True
    API_KEY = "test-key"
    UPLOAD_FOLDER = "app/media/"
    CACHE_REDIS_PASSWORD = os.environ.get("REDIS_PW", None)
