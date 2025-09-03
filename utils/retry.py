import asyncio
from functools import wraps
from asyncpg import PostgresError

def async_retry(max_retries=3, delay=1, backoff=2):
    """Decorator for retry attempts"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except PostgresError as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    
                    print(f"Retry {retries}/{max_retries} after error: {e}")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator