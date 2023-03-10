from functools import wraps
import os
from email.message import EmailMessage
from typing import Any, Coroutine

from aiocache import caches
import aiosmtplib
from aiosmtplib.response import SMTPResponse
from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

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


def aio_cache(f, timeout: int = 60, key: str = "view/{}"):
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


async def get_task_queue() -> Coroutine[Any, Any, ArqRedis]:
    if "arq" not in g:
        redis_conf = RedisSettings(
            host=current_app.config["CACHE_REDIS_HOST"],
            port=current_app.config["CACHE_REDIS_PORT"],
            database=current_app.config["CACHE_REDIS_DB"],
            password=current_app.config["CACHE_REDIS_PASSWORD"],
        )
        g.arq = await create_pool(redis_conf)

    return await g.arq


async def send_mail(
    subject: str, content: str, to: str = None
) -> tuple[dict[str, SMTPResponse], str]:
    email = EmailMessage()
    if to is None:
        email["To"] = current_app.config["MAIL_TO"]
    else:
        email["To"] = to
    email["From"] = current_app.config["SMTP_USER"]
    email["Subject"] = subject
    email.set_content(content)
    return await aiosmtplib.send(
        email,
        hostname=current_app.config["SMTP_HOST"],
        port=current_app.config["SMTP_PORT"],
        username=current_app.config["SMTP_USER"],
        password=current_app.config["SMTP_PASSWORD"],
    )
