#!/usr/bin/env python3
"""Utility functions for unit tests."""

import requests
from functools import wraps


def access_nested_map(nested_map, path):
    """Access a nested map using a tuple path.

    Raises KeyError if a key is missing or if an intermediate value
    is not a dict.
    """
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url):
    """Return the JSON payload obtained from `url`."""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Memoization decorator to cache a no-arg method result."""
    attr_name = "_memoized_" + fn.__name__

    @wraps(fn)
    def memoizer(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoizer
