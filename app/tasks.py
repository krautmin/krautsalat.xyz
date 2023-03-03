import os
from pathlib import Path

from arq.connections import RedisSettings
from dotenv import load_dotenv


base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / ".env"

if env_path.exists():
    """
    Load in the .env file
    If it exists
    """
    load_dotenv(str(env_path))


async def sample_task(ctx):
    return "Hello, World!"


class WorkerSettings:
    functions = [sample_task]
    redis_settings = RedisSettings(
        host=os.environ.get("REDIS_HOST", "redis"),
        port=int(os.environ.get("REDIS_PORT", 6379)),
        database=int(os.environ.get("REDIS_DB", 1)),
        password=os.environ.get("REDIS_PW", None),
    )
