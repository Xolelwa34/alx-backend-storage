#!/usr/bin/env python3
"""
 Method to store the instance of the redis client 
 as a private variable named
"""


import redis
from typing import Callable, Optional, Union
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Counts function"""
    method_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Increment numbers"""
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """call for a particular function"""
    qualified_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Add call_history"""
        self._redis.rpush(qualified_name + ':inputs', str(args))
        self._redis.rpush(
            qualified_name + ':outputs',
            method(self, *args, **kwargs)
        )
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ main class """

    def __init__(self):
        """ Init"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store uuid"""
        unique_id = str(uuid4)
        self._redis.set(unique_id, data)
        return unique_id

    def get(self, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
        """ get for task 0"""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, int, float]:
        """ Calls str"""
        return self.get(key, str)

    def get_int(self, key: str) -> Union[str, bytes, int, float]:
        """ calls int """
        return self.get(key, int)
