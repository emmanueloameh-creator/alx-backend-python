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
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_public_repos(self, org_name, mock_get_json):
        """Test public_repos returns the correct list of repos."""

        # Mock JSON payload returned by get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = mock_payload

        # Mock the _public_repos_url property
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=Mock
        ) as mock_public_url:
            mock_public_url.return_value = f"https://api.github.com/orgs/{org_name}/repos"
            client = GithubOrgClient(org_name)
            result = client.public_repos()

            # Expected repo names list
            self.assertEqual(result, ["repo1", "repo2"])

            # Assert get_json called once with the mocked URL
            mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}/repos"
            )


if __name__ == "__main__":
    unittest.main()
