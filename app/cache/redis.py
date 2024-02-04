# import json
# from fastapi import Depends
# from typing import Any
# from fastapi.encoders import jsonable_encoder
# from app.config import Config
# from app.database.db import get_redis


# config = Config()


# class Cache:

#     def __init__(self):
#         self.redis = Depends(get_redis)

#     def get(self, key: str) -> Any:
#         cached_data = self.get(key)
#         if cached_data:
#             return cached_data.decode("utf-8")
#         return None

#     def set(self, key: str, value: Any) -> None:
#         self.set(key, value)

#     def fetch(self,
#               key: str,
#               repository: Any,
#               *args,
#               **kwargs) -> Any:
#         cached = self.get(key)
#         if cached:
#             return json.loads(cached)
#         data = repository(*args, **kwargs)
#         value = jsonable_encoder(data)
#         self.set(key, json.dumps(value))
#         return data

#     def invalidate(self, *args: str) -> None:
#         for key in args:
#             self.redis.delete(key)


# cache_instance = Cache()
