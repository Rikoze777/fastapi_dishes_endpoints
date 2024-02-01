import aioredis
from typing import Any


class Cache:
    def __init__(self, redis_host: str):
        self.redis_client = aioredis.StrictRedis(host=redis_host, port=6379, db=0)

    async def get(self, key: str) -> Any:
        cached_data = await self.redis_client.get(key)
        if cached_data:
            return cached_data.decode("utf-8")
        return None

    async def set(self, key: str, value: Any) -> None:
        await self.redis_client.set(key, value)