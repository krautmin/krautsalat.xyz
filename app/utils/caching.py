from aiocache import caches
import os
from functools import wraps
from quart import request


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


def aio_cache(timeout=60, key="view/{}"):
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            cache_key = key.format(request.path)
            rv = await cache.get(cache_key)
            if rv is not None:
                return rv
            await cache.set(cache_key, rv, ttl=timeout)
            return await f(*args, **kwargs)

        return decorated_function

    return decorator
