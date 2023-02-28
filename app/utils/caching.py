from aiocache import caches
import os
from functools import wraps
from quart import g, request


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
