import os

from taskiq_redis.redis_broker import RedisBroker
from taskiq_redis.redis_backend import RedisAsyncResultBackend

redis_url = f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{int(os.environ.get('REDIS_PORT', 6379))}"

redis_async_result = RedisAsyncResultBackend(
    redis_url=redis_url,
)

scheduler = RedisBroker(
    url=redis_url,
    result_backend=redis_async_result,
)
