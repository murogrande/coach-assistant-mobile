"""
API Client for communicating with Django backend
"""

import os
import json
from datetime import date, timedelta
import requests
from typing import Optional, Dict, List

TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".coach_assistant_token.json")


class APIClient:
    """Handles all API communication with the backend"""

    # TODO: Change this to your backend URL
    # For local testing: "http://localhost:8000/api"
    # For testing on phone: "http://YOUR_COMPUTER_IP:8000/api"
    API_BASE_URL = "http://localhost:8000/api"

    def __init__(self):
        """Initialise the client with empty auth state."""
        self.token: Optional[str] = None
        self.username: Optional[str] = None
        self.headers = {
            "Content-Type": "application/json"
        }

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
        data = {
            "username": username,
            "password": password
        }

        response = requests.post(url, json=data)
        response.raise_for_status()

        result = response.json()
        # Backend returns tokens.access (JWT) or token (simple)
        tokens_obj = result.get("tokens", {})
        self.token = tokens_obj.get("access") or result.get("token")
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
        data = {
            "username": username,
            "password": password,
            "email": email
        }

        response = requests.post(url, json=data)
        response.raise_for_status()

        return response.json()

    def save_token(self):
        """Persist the current access token and username to disk"""
        if self.token:
            with open(TOKEN_FILE, "w") as f:
                json.dump({"access_token": self.token, "username": self.username}, f)

    def load_token(self) -> Optional[str]:
        """Load persisted token and username from disk"""
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE) as f:
                    data = json.load(f)
                self.token = data.get("access_token")
                self.username = data.get("username")
                if self.token:
                    self._update_auth_header()
                    return self.token
            except (json.JSONDecodeError, KeyError):
                pass
        return None

    def logout(self):
        """Clear token and username from memory and disk"""
        self.token = None
        self.username = None
        self.headers.pop("Authorization", None)
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)

    def is_authenticated(self) -> bool:
        """Return True if a token is currently set"""
        return bool(self.token)

    # Goals endpoints
    def get_goals(self) -> List[Dict]:
        """Get all goals for current week"""
        url = f"{self.API_BASE_URL}/goals/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_goal(self, goal_text: str, category: str = "personal") -> Dict:
        """Create new weekly goal for the current week."""
        url = f"{self.API_BASE_URL}/goals/"
        today = date.today()
        week_start = today - timedelta(days=today.weekday())  # Monday
        data = {
            "goal_text": goal_text,
            "category": category,
            "week_start_date": week_start.isoformat(),
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_goal(self, goal_id: int, completed: bool = None, goal_text: str = None) -> Dict:
        """Update goal status or text"""
        url = f"{self.API_BASE_URL}/goals/{goal_id}/"
        data = {}
        if completed is not None:
            data["completed"] = completed
        if goal_text is not None:
            data["goal_text"] = goal_text

        response = requests.put(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_goal(self, goal_id: int) -> None:
        """Delete a goal by ID"""
        url = f"{self.API_BASE_URL}/goals/{goal_id}/"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()

    # Journal endpoints
    def get_journal_entries(self) -> List[Dict]:
        """Get all journal entries"""
        url = f"{self.API_BASE_URL}/journal/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_journal_by_date(self, date_str: str) -> Optional[Dict]:
        """Get journal entry for specific date (YYYY-MM-DD)"""
        url = f"{self.API_BASE_URL}/journal/by-date/{date_str}/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def create_journal_entry(self, date_str: str, content: str, language: str = "en") -> Dict:
        """Create new journal entry"""
        url = f"{self.API_BASE_URL}/journal/"
        data = {
            "date": date_str,
            "content": content,
            "language": language
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update_journal_entry(self, entry_id: int, content: str) -> Dict:
        """Update existing journal entry by ID"""
        url = f"{self.API_BASE_URL}/journal/{entry_id}/"
        data = {"content": content}
        response = requests.patch(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    # Analysis endpoints
    def generate_analysis(self, week_start_date: str) -> Dict:
        """Request weekly analysis generation"""
        url = f"{self.API_BASE_URL}/analysis/generate/"
        data = {
            "week_start_date": week_start_date
        }
        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_latest_analysis(self) -> Optional[Dict]:
        """Get most recent weekly analysis"""
        url = f"{self.API_BASE_URL}/analysis/latest/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def get_analysis_list(self) -> List[Dict]:
        """Get all weekly analyses for the current user"""
        url = f"{self.API_BASE_URL}/analysis/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()

    def delete_analysis(self, analysis_id: int) -> None:
        """Delete an analysis by ID"""
        url = f"{self.API_BASE_URL}/analysis/{analysis_id}/"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()


# Singleton instance
api_client = APIClient()
