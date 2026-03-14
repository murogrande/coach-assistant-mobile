"""
API Client for communicating with Django backend
"""

import os
import json
from datetime import date, timedelta
import requests
from typing import Optional, Dict, List

# On Android (p4a), expanduser("~") resolves to /data which is not writable.
# Fall back to the app's internal files directory (parent of the working dir).
_token_dir = os.path.expanduser("~")
if not os.access(_token_dir, os.W_OK):
    _token_dir = os.path.dirname(os.getcwd())
TOKEN_FILE = os.path.join(_token_dir, ".coach_assistant_token.json")


class APIClient:
    """Handles all API communication with the backend"""

    # For phone testing: change to your laptop's local IP, e.g. http://192.168.1.x:8000/api
    API_BASE_URL = "http://localhost:8000/api"

    REQUEST_TIMEOUT = 15  # seconds

    def __init__(self):
        """Initialise the client with empty auth state."""
        self.token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.username: Optional[str] = None
        self.headers = {"Content-Type": "application/json"}

    def _update_auth_header(self):
        """Update authorization header with current token"""
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def login(self, username: str, password: str) -> Dict:
        """
        Login user and store authentication token

        Args:
            username: User's username
            password: User's password

        Returns:
            Dict with user info and token
        """
        url = f"{self.API_BASE_URL}/auth/login/"
        data = {"username": username, "password": password}

        response = requests.post(url, json=data)
        response.raise_for_status()

        result = response.json()
        # Backend returns tokens.access (JWT) or token (simple)
        tokens_obj = result.get("tokens", {})
        self.token = tokens_obj.get("access") or result.get("token")
        self.refresh_token = tokens_obj.get("refresh")
        self.username = result.get("user", {}).get("username") or username
        self._update_auth_header()
        self.save_token()

        return result

    def register(self, username: str, password: str, email: str = "") -> Dict:
        """
        Register new user

        Args:
            username: Desired username
            password: Password
            email: Email address (optional)

        Returns:
            Dict with user info
        """
        url = f"{self.API_BASE_URL}/auth/register/"
        data = {"username": username, "password": password, "email": email}

        response = requests.post(url, json=data)
        response.raise_for_status()

        return response.json()

    def save_token(self):
        """Persist the current access and refresh tokens to disk"""
        if self.token:
            with open(TOKEN_FILE, "w") as f:
                json.dump({
                    "access_token": self.token,
                    "refresh_token": self.refresh_token,
                    "username": self.username,
                }, f)

    def load_token(self) -> Optional[str]:
        """Load persisted tokens and username from disk"""
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE) as f:
                    data = json.load(f)
                self.token = data.get("access_token")
                self.refresh_token = data.get("refresh_token")
                self.username = data.get("username")
                if self.token:
                    self._update_auth_header()
                    return self.token
            except (json.JSONDecodeError, KeyError):
                pass
        return None

    def logout(self):
        """Clear tokens and username from memory and disk"""
        self.token = None
        self.refresh_token = None
        self.username = None
        self.headers.pop("Authorization", None)
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)

    def _refresh_access_token(self) -> bool:
        """Use the refresh token to obtain a new access token. Returns True on success."""
        if not self.refresh_token:
            return False
        url = f"{self.API_BASE_URL}/auth/token/refresh/"
        try:
            response = requests.post(
                url, json={"refresh": self.refresh_token}, timeout=self.REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                self.token = response.json().get("access")
                if self.token:
                    self._update_auth_header()
                    self.save_token()
                    return True
        except Exception:
            pass
        return False

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an HTTP request with timeout, retrying once after a token refresh on 401."""
        kwargs.setdefault("headers", self.headers)
        kwargs.setdefault("timeout", self.REQUEST_TIMEOUT)
        response = getattr(requests, method)(url, **kwargs)
        if response.status_code == 401 and self._refresh_access_token():
            kwargs["headers"] = self.headers
            response = getattr(requests, method)(url, **kwargs)
        response.raise_for_status()
        return response

    def is_authenticated(self) -> bool:
        """Return True if a token is currently set"""
        return bool(self.token)

    # Goals endpoints
    def get_goals(self) -> List[Dict]:
        """Get all goals for current week"""
        return self._request("get", f"{self.API_BASE_URL}/goals/").json()

    def create_goal(self, goal_text: str, category: str = "personal") -> Dict:
        """Create new weekly goal for the current week."""
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        data = {
            "goal_text": goal_text,
            "category": category,
            "week_start_date": week_start.isoformat(),
        }
        return self._request("post", f"{self.API_BASE_URL}/goals/", json=data).json()

    def update_goal(
        self,
        goal_id: int,
        completed: Optional[bool] = None,
        goal_text: Optional[str] = None,
    ) -> Dict:
        """Update goal status or text"""
        data = {}
        if completed is not None:
            data["completed"] = completed
        if goal_text is not None:
            data["goal_text"] = goal_text
        return self._request("patch", f"{self.API_BASE_URL}/goals/{goal_id}/", json=data).json()

    def delete_goal(self, goal_id: int) -> None:
        """Delete a goal by ID"""
        self._request("delete", f"{self.API_BASE_URL}/goals/{goal_id}/")

    # Journal endpoints
    def get_journal_entries(self) -> List[Dict]:
        """Get all journal entries"""
        return self._request("get", f"{self.API_BASE_URL}/journal/").json()

    def get_journal_by_date(self, date_str: str) -> Optional[Dict]:
        """Get journal entry for specific date (YYYY-MM-DD)"""
        url = f"{self.API_BASE_URL}/journal/by-date/{date_str}/"
        response = requests.get(url, headers=self.headers, timeout=self.REQUEST_TIMEOUT)
        if response.status_code == 401 and self._refresh_access_token():
            response = requests.get(url, headers=self.headers, timeout=self.REQUEST_TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def create_journal_entry(self, date_str: str, content: str, language: str = "en") -> Dict:
        """Create new journal entry"""
        data = {"date": date_str, "content": content, "language": language}
        return self._request("post", f"{self.API_BASE_URL}/journal/", json=data).json()

    def update_journal_entry(self, entry_id: int, content: str) -> Dict:
        """Update existing journal entry by ID"""
        return self._request(
            "patch", f"{self.API_BASE_URL}/journal/{entry_id}/", json={"content": content}
        ).json()

    # Analysis endpoints
    def generate_analysis(self, week_start_date: str) -> Dict:
        """Request weekly analysis generation"""
        return self._request(
            "post",
            f"{self.API_BASE_URL}/analysis/generate/",
            json={"week_start_date": week_start_date},
            timeout=120,  # generation can take up to 30-60s
        ).json()

    def get_latest_analysis(self) -> Optional[Dict]:
        """Get most recent weekly analysis"""
        url = f"{self.API_BASE_URL}/analysis/latest/"
        response = requests.get(url, headers=self.headers, timeout=self.REQUEST_TIMEOUT)
        if response.status_code == 401 and self._refresh_access_token():
            response = requests.get(url, headers=self.headers, timeout=self.REQUEST_TIMEOUT)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def get_analysis_list(self) -> List[Dict]:
        """Get all weekly analyses for the current user"""
        url = f"{self.API_BASE_URL}/analysis/"
        response = requests.get(url, headers=self.headers, timeout=self.REQUEST_TIMEOUT)
        if response.status_code == 401 and self._refresh_access_token():
            response = requests.get(url, headers=self.headers, timeout=self.REQUEST_TIMEOUT)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()

    def delete_analysis(self, analysis_id: int) -> None:
        """Delete an analysis by ID"""
        self._request("delete", f"{self.API_BASE_URL}/analysis/{analysis_id}/")


# Singleton instance
api_client = APIClient()
