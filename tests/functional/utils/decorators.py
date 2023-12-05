from functools import wraps
import time
from functional.logger import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=20):
    """
    if something is wrong it relaunch the functions
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_sleep_time = start_sleep_time
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    logger.info(f"Error: {str(e)}. Retrying in {current_sleep_time} seconds.")
                    print(f"Error: {str(e)}. Retrying in {current_sleep_time} seconds.")
                    time.sleep(current_sleep_time)
                    current_sleep_time = min(current_sleep_time * factor, border_sleep_time)
        return inner
    return func_wrapper
