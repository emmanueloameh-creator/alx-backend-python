#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient.public_repos.

Tests use mock HTTP responses and simulate org and repo payloads.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient

@parameterized_class([
    {
        "org_payload": {"login": "google", "id": 1},
        "repos_payload": [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ],
        "expected_repos": ["repo1", "repo2"],
        "apache2_repos": ["repo1"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get to return mock responses."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Define side_effect for requests.get().json()
        def side_effect(url):
            mock_response = Mock()
            if url.endswith("/orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all expected repos."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns only repos with apache-2.0 license."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
