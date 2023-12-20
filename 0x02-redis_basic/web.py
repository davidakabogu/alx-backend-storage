# #!/usr/bin/env python3
# """
# web cache and tracker
# """
# import requests
# import redis
# from functools import wraps

# store = redis.Redis()


# def count_url_access(method):
#     """ Decorator counting how many times
#     a URL is accessed """
#     @wraps(method)
#     def wrapper(url):
#         cached_key = "cached:" + url
#         cached_data = store.get(cached_key)
#         if cached_data:
#             return cached_data.decode("utf-8")

#         count_key = "count:" + url
#         html = method(url)

#         store.incr(count_key)
#         store.set(cached_key, html)
#         store.expire(cached_key, 10)
#         return html
#     return wrapper


# @count_url_access
# def get_page(url: str) -> str:
#     """ Returns HTML content of a url """
#     res = requests.get(url)
#     return res.text

import requests
import time
from functools import wraps

def cache_function_results(expiration_time):
    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"count:{args[0]}"
            current_time = time.time()

            if key in cache and current_time - cache[key]["timestamp"] < expiration_time:
                print(f"Cache hit for {args[0]}")
                return cache[key]["data"]
            else:
                print(f"Cache miss for {args[0]}")
                result = func(*args, **kwargs)
                cache[key] = {"data": result, "timestamp": current_time}
                return result

        return wrapper

    return decorator

@cache_function_results(expiration_time=10)
def get_page(url):
    response = requests.get(url)
    return response.text

# # Example usage:
# if __name__ == "__main__":
#     slow_url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com"

#     # Accessing the slow URL twice within 10 seconds should use the cache.
#     print(get_page(slow_url))
#     print(get_page(slow_url))

#     # Wait for 11 seconds to expire the cache.
#     time.sleep(11)

#     # Accessing the slow URL again after cache expiration.
#     print(get_page(slow_url))
