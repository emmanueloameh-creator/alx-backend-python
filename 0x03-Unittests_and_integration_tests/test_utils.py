#!/usr/bin/env python3
"""Unit tests for utils.py."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map behaviour."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test normal access returns expected value."""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected
        )

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test a KeyError is raised and message is correct."""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)
        self.assertEqual(
            str(error.exception),
            f"'{path[-1]}'"
        )


class TestGetJson(unittest.TestCase):
    """Test get_json using mocked requests.get."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns the payload and calls get."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test memoize decorator behaviour."""

    def test_memoize(self):
        """Test memoize caches method call result."""

        class TestClass:
            """Test class for memoize."""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with patch.object(TestClass, "a_method", return_value=42
                          ) as mock_method:
            res1 = test_instance.a_property()
            res2 = test_instance.a_property()
            self.assertEqual(res1, 42)
            self.assertEqual(res2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
