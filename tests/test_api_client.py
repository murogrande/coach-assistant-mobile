"""Tests for API client"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock

from services.api_client import APIClient, api_client, TOKEN_FILE


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
    def test_login_success_jwt_format(self, mock_post):
        """Test successful login stores token from tokens.access (JWT format)"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tokens": {"access": "jwt-access-token", "refresh": "jwt-refresh-token"},
            "user": {"id": 1}
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        client = APIClient()
        with patch("services.api_client.open", create=True), \
             patch("services.api_client.json.dump"):
            result = client.login("testuser", "password")

        assert client.token == "jwt-access-token"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "Bearer jwt-access-token"
        mock_post.assert_called_once()

    @patch("services.api_client.requests.post")
    def test_login_success_simple_format(self, mock_post):
        """Test successful login stores token from simple token field"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "abc123", "user": {"id": 1}}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        client = APIClient()
        with patch("builtins.open", MagicMock()), \
             patch("services.api_client.json.dump"):
            result = client.login("testuser", "password")

        assert client.token == "abc123"
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

    def test_is_authenticated_false_without_token(self):
        """Test is_authenticated returns False when no token"""
        client = APIClient()
        assert client.is_authenticated() is False

    def test_is_authenticated_true_with_token(self):
        """Test is_authenticated returns True when token is set"""
        client = APIClient()
        client.token = "some-token"
        assert client.is_authenticated() is True

    def test_logout_clears_token_and_header(self, tmp_path, monkeypatch):
        """Test logout removes token from memory and disk"""
        token_file = tmp_path / "token.json"
        token_file.write_text(json.dumps({"access_token": "tok"}))
        monkeypatch.setattr("services.api_client.TOKEN_FILE", str(token_file))

        client = APIClient()
        client.token = "tok"
        client._update_auth_header()
        client.logout()

        assert client.token is None
        assert "Authorization" not in client.headers
        assert not token_file.exists()

    def test_save_and_load_token(self, tmp_path, monkeypatch):
        """Test token round-trips through save/load"""
        token_file = tmp_path / "token.json"
        monkeypatch.setattr("services.api_client.TOKEN_FILE", str(token_file))

        client = APIClient()
        client.token = "my-jwt-token"
        client.save_token()

        client2 = APIClient()
        loaded = client2.load_token()

        assert loaded == "my-jwt-token"
        assert client2.token == "my-jwt-token"
        assert client2.headers["Authorization"] == "Bearer my-jwt-token"

    def test_load_token_returns_none_when_no_file(self, tmp_path, monkeypatch):
        """Test load_token returns None when token file does not exist"""
        monkeypatch.setattr(
            "services.api_client.TOKEN_FILE",
            str(tmp_path / "nonexistent.json")
        )
        client = APIClient()
        assert client.load_token() is None

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

    @patch("services.api_client.requests.post")
    def test_create_goal_includes_week_start_date(self, mock_post):
        """Test create_goal sends week_start_date (Monday of current week)"""
        from datetime import date, timedelta

        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "goal_text": "Test goal"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        client = APIClient()
        client.create_goal("Test goal")

        payload = mock_post.call_args[1]["json"]
        assert "week_start_date" in payload

        today = date.today()
        expected_monday = (today - timedelta(days=today.weekday())).isoformat()
        assert payload["week_start_date"] == expected_monday

    @patch("services.api_client.requests.delete")
    def test_delete_goal(self, mock_delete):
        """Test delete_goal sends DELETE request"""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_delete.return_value = mock_response

        client = APIClient()
        client.delete_goal(42)

        mock_delete.assert_called_once()
        assert "goals/42/" in mock_delete.call_args[0][0]

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
