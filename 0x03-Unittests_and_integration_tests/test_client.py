#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value
        and calls get_json once with the expected URL.
        """
        # Mock return value
        mock_get_json.return_value = {"org": org_name}

        # Create instance
        client = GithubOrgClient(org_name)
        result = client.org

        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"org": org_name})
	
    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL."""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch("client.GithubOrgClient.org", new_callable=Mock(return_value=payload)):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, payload["repos_url"])



if __name__ == "__main__":
    unittest.main()
