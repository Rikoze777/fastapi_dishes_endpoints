import json
import aioredis
from typing import Any
from app.config import Config
from fastapi.encoders import jsonable_encoder


config = Config()
redis_host = config.REDIS_HOST
redis_port = config.REDIS_PORT


class Cache:

    def __init__(self, redis_host: str, redis_port: int):
        self.redis_client = aioredis.StrictRedis(host=redis_host,
                                                 port=redis_port,
                                                 db=0)

    async def get(self, key: str) -> Any:
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return cached_data.decode("utf-8")
        return None

    async def set(self, key: str, value: Any) -> None:
        await self.redis_client.set(key, value)

    async def fetch(self,
                    key: str,
                    repository: Any,
                    *args,
                    **kwargs) -> Any:
        cached = await self.get(key)
        if cached:
            return json.loads(cached)
        data = await repository(*args, **kwargs)
        value = jsonable_encoder(data)
        await self.set(key, json.dumps(value))
        return data

    async def invalidate(self, *args: str) -> None:
        for key in args:
            await self.redis_client.delete(key)


cache_instance = Cache(redis_host, redis_port)
