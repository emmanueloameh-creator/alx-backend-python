#!/usr/bin/env python3
"""Unit tests for utils.py including memoize"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches the result and calls the method only once"""

        class TestClass:
            """Test class to use memoize decorator"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            # Call twice
            result1 = test_instance.a_property()
            result2 = test_instance.a_property()

            # The result should always be correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # a_method should be called only once
            mock_method.assert_called_once()
