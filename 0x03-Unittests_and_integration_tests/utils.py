#!/usr/bin/env python3
"""Utility functions module."""

def access_nested_map(nested_map, path):
    """Access nested map using path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map
