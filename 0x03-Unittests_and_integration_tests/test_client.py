#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls get_json once."""
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, {"org": org_name})
        mock_get_json.assert_called_once_with(url)

    @patch("client.GithubOrgClient.org", new_callable=Mock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property."""
        mock_org.return_value = {"repos_url": "http://example.com/repos"}

        client = GithubOrgClient("test-org")
        result = client._public_repos_url

        self.assertEqual(result, "http://example.com/repos")

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_public_repos(self, org_name, mock_get_json):
        """
        Test that public_repos returns the list of repo names,
        and that both _public_repos_url and get_json are called once.
        """
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = mock_payload

        repos_url = (
            f"https://api.github.com/orgs/{org_name}/repos"
        )

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=Mock
        ) as mock_public_url:
            mock_public_url.return_value = repos_url

            client = GithubOrgClient(org_name)
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_url.assert_called_once()
            mock_get_json.assert_called_once_with(repos_url)


if __name__ == "__main__":
    unittest.main()
