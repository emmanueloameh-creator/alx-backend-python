#!/usr/bin/env python3
"""Utility functions module."""

import requests
from functools import wraps


def access_nested_map(nested_map, path):
    """Access nested map using path."""
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        current = current[key]
    return current


def get_json(url):
    """Fetch JSON content from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn):
    """Memoization decorator for a class method."""
    attr_name = "_memoized_" + fn.__name__

    @wraps(fn)
    def memoizer(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoizer
