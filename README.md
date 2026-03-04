# Coach Assistant Mobile

KivyMD mobile application for personal coaching and goal tracking.

## Overview

This mobile app helps you:
- Set and track weekly goals
- Write daily journal entries
- Get AI-powered weekly analysis and insights
- Stay motivated with personalised coaching

## Technology Stack

- **Framework**: KivyMD 2.0.1.dev0 (Material Design 3)
- **UI Library**: Kivy 2.3.1
- **Platform**: Android via Buildozer
- **Backend**: Django REST API (`coach-assistant-backend`)
- **Language**: Python 3.10+

## Project Structure

```
coach-assistant-mobile/
├── main.py                 # App entry point, theme, ScreenManager, auto-login
├── screens/                # UI screens
│   ├── login.py            # Login + Register UI, validation, auth logic
│   ├── home.py             # Navigation dashboard
│   ├── goals.py            # Weekly goals management
│   ├── journal.py          # Daily journal entries
│   └── analysis.py         # AI weekly analysis display
├── services/
│   └── api_client.py       # REST API client singleton (auth, goals, journal, analysis)
├── utils/                  # Helper functions
├── assets/                 # Images, fonts, icons
├── tests/                  # Test suite (52 tests)
└── requirements.txt
```

## Setup

### Prerequisites

- Python 3.10+
- For Android build: Linux or WSL

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Edit `services/api_client.py` to set your backend URL:

```python
API_BASE_URL = "http://localhost:8000/api"          # desktop
API_BASE_URL = "http://192.168.x.x:8000/api"       # phone on same WiFi
```

Find your local IP with: `ip addr show | grep "inet 192"`

### Run on Desktop

```bash
python main.py
```

### Build for Android

```bash
pip install buildozer
buildozer init
buildozer -v android debug       # First build takes ~30 minutes
buildozer android deploy run
```

### Run Tests

```bash
python -m pytest tests/
python -m pytest tests/ -q      # quiet
python -m pytest tests/ -v      # verbose
```

## Current Status

### Done
- ✅ **Issue #1** — App structure, theme (Blue/Teal), ScreenManager, navigation
- ✅ **Issue #2** — Login screen UI: hero header, form card, field icons, validation, register toggle, password visibility toggle
- ✅ **Issue #3** — Authentication logic: login/register API calls (threaded), JWT token persistence, auto-login on start, error messages
- ✅ **Issue #4** — Home dashboard: greeting, username, stats cards (goals/journal), refresh button, navigation cards

### In Progress / Next
- ✅ **Issue #5** — Goals screen: goal cards with checkboxes, add goal dialog, delete, empty state
- 🔲 **Issue #6** — Goals API integration
- 🔲 **Issue #7–8** — Journal screen UI + API integration
- 🔲 **Issue #9–10** — Analysis screen UI + API integration
- 🔲 **Issue #15–16** — Buildozer Android build + device testing

**Milestone "POC Ready"** = Issues #1–10, then #15–16 to get on phone.

## Authentication Flow

1. App starts → checks `~/.coach_assistant_token.json` for a saved token
2. If token found → navigates directly to Home (auto-login)
3. If no token → shows Login screen
4. Login/Register → calls backend API in a background thread → saves JWT access token on success
5. Logout → clears token from memory and disk

## Backend

This app requires the `coach-assistant-backend` Django REST API. See that repository for setup instructions. The backend exposes:

- `POST /api/auth/login/` and `/api/auth/register/`
- `GET/POST /api/goals/`
- `GET/POST /api/journal/`
- `POST /api/analysis/generate/`, `GET /api/analysis/latest/`

Token format: `{ "tokens": { "access": "...", "refresh": "..." } }`

## Troubleshooting

**"Connection refused" error**
- Ensure the backend is running (`python manage.py runserver`)
- Check `API_BASE_URL` in `services/api_client.py`
- Use your computer's local IP when testing on a phone (not `localhost`)

**Buildozer errors**
- Must be on Linux or WSL
- Install system deps: `sudo apt-get install -y python3-pip build-essential git python3-dev`

## License

Private — All rights reserved
