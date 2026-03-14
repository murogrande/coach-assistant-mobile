"""Tests for API client"""

import json
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
            client.login("testuser", "password")

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
            client.login("testuser", "password")

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

    @patch("services.api_client.requests.patch")
    def test_update_goal_uses_patch(self, mock_patch):
        """update_goal must use PATCH (not PUT) — PUT returns 400 Bad Request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 7, "completed": True}
        mock_response.raise_for_status = MagicMock()
        mock_patch.return_value = mock_response

        client = APIClient()
        client.update_goal(7, completed=True)

        mock_patch.assert_called_once()
        assert "goals/7/" in mock_patch.call_args[0][0]
        assert mock_patch.call_args[1]["json"]["completed"] is True

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
        """Test get_journal_by_date returns None on 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_journal_by_date("2024-01-01")

        assert result is None
        assert "journal/by-date/2024-01-01/" in mock_get.call_args[0][0]

    @patch("services.api_client.requests.get")
    def test_get_journal_by_date_found(self, mock_get):
        """Test get_journal_by_date returns the entry when found"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 5, "date": "2024-01-01", "content": "Hello"}
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_journal_by_date("2024-01-01")

        assert result == {"id": 5, "date": "2024-01-01", "content": "Hello"}

    @patch("services.api_client.requests.patch")
    def test_update_journal_entry(self, mock_patch):
        """Test update_journal_entry sends PATCH to /journal/{id}/"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 5, "content": "Updated"}
        mock_patch.return_value = mock_response

        client = APIClient()
        result = client.update_journal_entry(5, "Updated")

        mock_patch.assert_called_once()
        url = mock_patch.call_args[0][0]
        assert "journal/5/" in url
        assert result["content"] == "Updated"

    @patch("services.api_client.requests.get")
    def test_get_latest_analysis_not_found(self, mock_get):
        """Test get_latest_analysis returns None for 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        client = APIClient()
        result = client.get_latest_analysis()

        assert result is None


class TestTokenRefresh:
    """Tests for automatic JWT token refresh on 401.

    Root cause: access tokens expire after 5 minutes (Django SimpleJWT default).
    The app was not saving or using the refresh token, so every request would fail
    silently with 401 after 5 minutes. Fix: save refresh token at login, and retry
    any 401 response once after refreshing the access token.
    """

    def test_login_saves_refresh_token(self):
        """login() must store the refresh token from tokens.refresh."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tokens": {"access": "access-tok", "refresh": "refresh-tok"},
            "user": {"username": "u"},
        }
        mock_response.raise_for_status = MagicMock()

        client = APIClient()
        with patch("services.api_client.requests.post", return_value=mock_response), \
             patch("services.api_client.open", create=True), \
             patch("services.api_client.json.dump"):
            client.login("u", "p")

        assert client.refresh_token == "refresh-tok"

    def test_save_and_load_refresh_token(self, tmp_path, monkeypatch):
        """Refresh token must survive a save/load round-trip."""
        token_file = tmp_path / "token.json"
        monkeypatch.setattr("services.api_client.TOKEN_FILE", str(token_file))

        client = APIClient()
        client.token = "access-tok"
        client.refresh_token = "refresh-tok"
        client.username = "u"
        client.save_token()

        client2 = APIClient()
        monkeypatch.setattr("services.api_client.TOKEN_FILE", str(token_file))
        client2.load_token()

        assert client2.refresh_token == "refresh-tok"

    @patch("services.api_client.requests.post")
    def test_refresh_access_token_success(self, mock_post):
        """_refresh_access_token() updates the access token and returns True."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access": "new-access-tok"}
        mock_post.return_value = mock_response

        client = APIClient()
        client.refresh_token = "refresh-tok"

        with patch.object(client, "save_token"):
            result = client._refresh_access_token()

        assert result is True
        assert client.token == "new-access-tok"
        assert client.headers["Authorization"] == "Bearer new-access-tok"

    def test_refresh_access_token_no_refresh_token(self):
        """_refresh_access_token() returns False when no refresh token is stored."""
        client = APIClient()
        client.refresh_token = None

        assert client._refresh_access_token() is False

    @patch("services.api_client.requests.post", side_effect=Exception("network error"))
    def test_refresh_access_token_network_failure(self, _):
        """_refresh_access_token() returns False on network error."""
        client = APIClient()
        client.refresh_token = "refresh-tok"

        assert client._refresh_access_token() is False

    @patch("services.api_client.requests.get")
    def test_request_retries_after_401_and_succeeds(self, mock_get):
        """_request() retries once with a new token when the first response is 401."""
        expired_response = MagicMock()
        expired_response.status_code = 401

        ok_response = MagicMock()
        ok_response.status_code = 200
        ok_response.json.return_value = {"id": 1}

        mock_get.side_effect = [expired_response, ok_response]

        client = APIClient()
        client.refresh_token = "refresh-tok"

        with patch.object(client, "_refresh_access_token", return_value=True):
            response = client._request("get", "http://test/api/goals/")

        assert mock_get.call_count == 2
        assert response.status_code == 200

    @patch("services.api_client.requests.get")
    def test_request_raises_401_when_refresh_fails(self, mock_get):
        """_request() raises HTTPError when 401 persists after a failed refresh."""
        import requests as req

        expired_response = MagicMock()
        expired_response.status_code = 401
        expired_response.raise_for_status.side_effect = req.HTTPError("401")
        mock_get.return_value = expired_response

        client = APIClient()
        with patch.object(client, "_refresh_access_token", return_value=False):
            try:
                client._request("get", "http://test/api/goals/")
                assert False, "Expected HTTPError"
            except req.HTTPError:
                pass

    @patch("services.api_client.requests.get")
    def test_get_goals_auto_refreshes_on_401(self, mock_get):
        """get_goals() transparently refreshes the token and retries on 401."""
        expired = MagicMock()
        expired.status_code = 401

        ok = MagicMock()
        ok.status_code = 200
        ok.json.return_value = [{"id": 1, "goal_text": "Run"}]

        mock_get.side_effect = [expired, ok]

        client = APIClient()
        client.refresh_token = "refresh-tok"

        with patch.object(client, "_refresh_access_token", return_value=True):
            result = client.get_goals()

        assert result == [{"id": 1, "goal_text": "Run"}]
        assert mock_get.call_count == 2
