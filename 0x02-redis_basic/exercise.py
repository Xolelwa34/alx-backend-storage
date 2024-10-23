#!/usr/bin/env python3
"""
 Method to store the instance of the redis client 
 as a private variable named
"""
import redis
import uuid
from typing import Union

class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
