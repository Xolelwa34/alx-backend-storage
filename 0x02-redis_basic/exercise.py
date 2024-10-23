#!/usr/bin/env python3
"""
Cache class to store data in Redis with method decorators for call counting and history.
"""

import redis
from typing import Callable, Optional, Union
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    method_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increment the call count each time the method is called."""
        self._redis.incr(method_name)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a method."""
    method_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Log input and output history of method calls."""
        self._redis.rpush(f"{method_name}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method_name}:outputs", output)
        return output

    return wrapper


class Cache:
    """Main Cache class to interact with Redis."""

    def __init__(self):
        """Initialize Redis connection and flush any existing data."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a randomly generated UUID key."""
        unique_id = str(uuid4())
        self._redis.set(unique_id, data)
        return unique_id

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis and apply an optional conversion function."""
        data = self._redis.get(key)
        if data is not None and fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis."""
        data = self.get(key, lambda d: d.decode('utf-8'))
        return data

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis."""
        data = self.get(key, int)
        return data


def replay(method: Callable) -> None:
    """Display the history of calls to a method."""
    method_name = method.__qualname__
    inputs = method.__self__._redis.lrange(f"{method_name}:inputs", 0, -1)
    outputs = method.__self__._redis.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")

