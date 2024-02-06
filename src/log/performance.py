from functools import wraps
import time
from typing import Any, Callable
import logging

def measure(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger = logging.getLogger(__name__)
        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start_time
        logger.debug(f"Function {func.__name__}() took {total_time:0.3f}s")
        return result
    return wrapper