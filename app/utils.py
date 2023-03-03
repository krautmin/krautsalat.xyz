from functools import wraps
import os
from email.message import EmailMessage

from aiocache import caches
import aiosmtplib
from arq import create_pool
from arq.connections import RedisSettings

from quart import current_app, g, request


caches.set_config(
    {
        "default": {
            "cache": "aiocache.RedisCache",
            "endpoint": os.environ.get("REDIS_HOST", "localhost"),
            "port": int(os.environ.get("REDIS_PORT", 6379)),
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            "plugins": [
                {"class": "aiocache.plugins.HitMissRatioPlugin"},
                {"class": "aiocache.plugins.TimingPlugin"},
            ],
        }
    }
)


cache = caches.get("default")


def aio_cache(f, timeout=60, key="view/{}"):
    @wraps(f)
    async def decorator(*args, **kwargs):
        if g.user:
            return await f(*args, **kwargs)
        cache_key = key.format(request.path)
        rv = await cache.get(cache_key)
        if rv is not None:
            return rv
        await cache.set(cache_key, rv, ttl=timeout)
        return await f(*args, **kwargs)

    return decorator


async def get_task_queue():
    if "arq" not in g:
        redis_conf = RedisSettings(
            host=current_app.config["CACHE_REDIS_HOST"],
            port=current_app.config["CACHE_REDIS_PORT"],
            database=current_app.config["CACHE_REDIS_DB"],
            password=current_app.config["CACHE_REDIS_PASSWORD"],
        )
        g.arq = await create_pool(redis_conf)

    return await g.arq


async def send_mail(subject, content, to=None):
    email = EmailMessage()
    email["To"] = to
    if email["To"] is None:
        email["To"] = current_app.config["MAIL_TO"]
    email["From"] = current_app.config["SMTP_USER"]
    email["To"] = current_app.config["MAIL_TO"]
    email["Subject"] = subject
    email.set_content(content)
    return await aiosmtplib.send(
        email,
        hostname=current_app.config["SMTP_HOST"],
        port=current_app.config["SMTP_PORT"],
        username=current_app.config["SMTP_USER"],
        password=current_app.config["SMTP_PASSWORD"],
    )
