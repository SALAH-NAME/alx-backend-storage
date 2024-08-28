#!/usr/bin/env python3
""" exercise.py """
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count_calls """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cache CLass
    """
    def __init__(self):
        """ __init__ """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float, None]:
        """ get """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """ get_str """
        data = self._redis.get(key)
        return data.decode('utf-8')

    def get_int(self, key: str) -> Optional[int]:
        """ get_int """
        data = self._redis.get(key)
        try:
            value = int(value.decode('uft-8'))
        except Exception:
            data = 0
        return data
