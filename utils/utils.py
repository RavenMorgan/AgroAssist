"""
AgriEdge BU,
Author: Noureddine ECH-CHOUKY
Contact: Noureddine.ECH-CHOUKY@um6p.ma
Description : This file contains the functions to retrieve the data from the SentinelHub API
Last updated: 18/03/2024
"""

from datetime import datetime


import requests
import json
from functools import wraps


def retry_(n_times):
    """
    Decorator that retries a function n times if it fails.

    :param n_times: int: number of times to retry the function
    :return: function: the decorated function
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for i in range(n_times):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    if i == n_times - 1:
                        raise e
                    print(f"Error: {e}, Retrying...")
                    time.sleep(1)

        return wrapper

    return decorator


def time_(function):
    """
    A decorator to calculate and log the time taken
    by a function to execute.

    :param function: function: the function to be decorated
    :return: function: the decorated function
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{function.__name__} took {elapsed_time:.2f} seconds to execute.")
        return result

    return wrapper


