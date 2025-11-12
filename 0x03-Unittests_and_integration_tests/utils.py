#!/usr/bin/env python3
"""Utility functions module."""


def access_nested_map(nested_map, path):
    """Access nested map using path."""
    current = nested_map
    for key in path:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(key)
        current = current[key]
    return current
