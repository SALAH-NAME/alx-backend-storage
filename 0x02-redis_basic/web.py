#!/usr/bin/env python3
""" web.py """
import redis
import requests
from typing import Callable
from functools import wraps


redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ count_requests """
    @wraps(method)
    def wrapper(url):
        """ wrapper """
        redis_client.incr(f"count:{url}")
        cached_response = redis_client.get(f'cached:{url}')
        if cached_response:
            return cached_response.decode('utf-8')
        response = method(url)
        redis_client.setex(f'cached:{url}', 10, response)
        return response
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ get_page """
    response = requests.get(url)
    return response.text
