#!/usr/bin/env python3
"""
Unit tests for utils.memoize decorator.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the method result properly."""

        class TestClass:
            """A simple class to test memoization."""

            def a_method(self):
                """Return a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """Call a_method, but result should be cached."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            first = obj.a_property()
            second = obj.a_property()

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()
