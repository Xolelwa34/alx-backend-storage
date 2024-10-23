#!/usr/bin/env python3
"""
 Redis exercise
 """
 import redis
from typing import Callable, Optional, Any

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, key: str, fn: Optional[Callable[[bytes], Any]] = None) -> Optional[Any]:
        value = self.client.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=lambda x: int(x))
