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


def call_history(method: Callable) -> Callable:
    """ call_history """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def replay(method: Callable):
    """ replay """
    redis_instance = method.__self__._redis
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        inp_str = inp.decode('utf-8')
        out_str = out.decode('utf-8')
        print(f"{method.__qualname__}(*{inp_str}) -> {out_str}")


class Cache:
    """
    Cache CLass
    """
    def __init__(self):
        """ __init__ """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
