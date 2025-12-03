"""
API Client for communicating with Django backend
"""

import requests
from typing import Optional, Dict, List


class APIClient:
    """Handles all API communication with the backend"""

    # TODO: Change this to your backend URL
    # For local testing: "http://localhost:8000/api"
    # For testing on phone: "http://YOUR_COMPUTER_IP:8000/api"
    API_BASE_URL = "http://localhost:8000/api"

    def __init__(self):
        self.token: Optional[str] = None
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
        self.token = result.get("token")
        self._update_auth_header()

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

    # Goals endpoints
    def get_goals(self) -> List[Dict]:
        """Get all goals for current week"""
        url = f"{self.API_BASE_URL}/goals/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_goal(self, goal_text: str, category: str = "personal") -> Dict:
        """Create new weekly goal"""
        url = f"{self.API_BASE_URL}/goals/"
        data = {
            "goal_text": goal_text,
            "category": category
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

    # Journal endpoints
    def get_journal_entries(self) -> List[Dict]:
        """Get all journal entries"""
        url = f"{self.API_BASE_URL}/journal/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_journal_by_date(self, date: str) -> Optional[Dict]:
        """Get journal entry for specific date (YYYY-MM-DD)"""
        url = f"{self.API_BASE_URL}/journal/{date}/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def create_journal_entry(self, date: str, content: str, language: str = "en") -> Dict:
        """Create new journal entry"""
        url = f"{self.API_BASE_URL}/journal/"
        data = {
            "date": date,
            "content": content,
            "language": language
        }
        response = requests.post(url, json=data, headers=self.headers)
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


# Singleton instance
api_client = APIClient()
