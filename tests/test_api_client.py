"""Tests for API client"""

import pytest
from unittest.mock import patch, MagicMock

from services.api_client import APIClient, api_client


class TestAPIClient:
    """Tests for APIClient class"""

    def test_singleton_instance_exists(self):
        """Test api_client singleton is created"""
        assert api_client is not None
        assert isinstance(api_client, APIClient)

    def test_initial_state(self):
        """Test APIClient initial state"""
        client = APIClient()
        assert client.token is None
        assert "Content-Type" in client.headers
        assert client.headers["Content-Type"] == "application/json"

    def test_update_auth_header_with_token(self):
        """Test auth header is updated when token is set"""
        client = APIClient()
        client.token = "test-token-123"
        client._update_auth_header()

        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer test-token-123"

    def test_update_auth_header_without_token(self):
        """Test auth header not set when token is None"""
        client = APIClient()
        client.token = None
        client._update_auth_header()

        assert "Authorization" not in client.headers

    @patch("services.api_client.requests.post")
    def test_login_success(self, mock_post):
        """Test successful login stores token"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "abc123", "user": {"id": 1}}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        client = APIClient()
        result = client.login("testuser", "password")

        assert client.token == "abc123"
        assert result["token"] == "abc123"
        mock_post.assert_called_once()

    @patch("services.api_client.requests.post")
    def test_register(self, mock_post):
        """Test register makes correct API call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "username": "newuser"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        client = APIClient()
        result = client.register("newuser", "password", "email@test.com")

        assert result["username"] == "newuser"
        call_args = mock_post.call_args
        assert "register" in call_args[0][0]

    @patch("services.api_client.requests.get")
    def test_get_goals(self, mock_get):
        """Test get_goals returns list"""
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1, "goal_text": "Test goal"}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_goals()

        assert isinstance(result, list)
        assert len(result) == 1

    @patch("services.api_client.requests.get")
    def test_get_journal_by_date_not_found(self, mock_get):
        """Test get_journal_by_date returns None for 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_journal_by_date("2024-01-01")

        assert result is None

    @patch("services.api_client.requests.get")
    def test_get_latest_analysis_not_found(self, mock_get):
        """Test get_latest_analysis returns None for 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_latest_analysis()

        assert result is None
