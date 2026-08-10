"""Retry logic with exponential backoff."""
import asyncio
import random
from functools import wraps
from typing import Type, Tuple, Callable, Any

def async_retry(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0, exceptions: Tuple[Type[Exception], ...] = (Exception,), jitter: bool = True):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt == max_retries:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    if jitter:
                        delay *= 0.5 + random.random()
                    await asyncio.sleep(delay)
            raise last_exc
        return wrapper
    return decorator
