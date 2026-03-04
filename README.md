# Coach Assistant Mobile

KivyMD mobile application for personal coaching and goal tracking.

## Overview

This mobile app helps you:
- Set and track weekly goals
- Write daily journal entries
- Get AI-powered weekly analysis and insights
- Stay motivated with personalized coaching

## Technology Stack

- **Framework**: KivyMD 2.0.1.dev0 (Material Design 3)
- **UI Library**: Kivy 2.3.1
- **Platform**: Android via Buildozer
- **Backend**: Django REST API (`coach-assistant-backend`)
- **Language**: Python 3.10+

## Project Structure

```
coach-assistant-mobile/
├── main.py                 # App entry point, theme, ScreenManager
├── screens/                # UI screens
│   ├── login.py            # Login + Register UI with validation
│   ├── home.py             # Navigation hub
│   ├── goals.py            # Weekly goals management
│   ├── journal.py          # Daily journal entries
│   └── analysis.py         # AI weekly analysis display
├── services/
│   └── api_client.py       # REST API client singleton
├── utils/                  # Helper functions
├── assets/                 # Images, fonts, icons
├── tests/                  # Test suite (29 tests)
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

Edit `services/api_client.py` to set your backend API URL:

```python
API_BASE_URL = "http://your-backend-url:8000/api"
```

For testing on a phone, use your computer's local IP instead of localhost.

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
python -m pytest tests/ -v
```

## Current Status

### Done
- ✅ **Issue #1** — App structure, theme (Blue/Teal), ScreenManager, navigation
- ✅ **Issue #2** — Login screen UI: hero header, form card, icons in fields, validation, error messages, register toggle

### In Progress / Next
- 🔲 **Issue #3** — Authentication logic (connect to backend API, token storage, auto-login)
- 🔲 **Issue #4** — Home/Dashboard screen
- 🔲 **Issue #5-6** — Goals screen UI + API integration
- 🔲 **Issue #7-8** — Journal screen UI + API integration
- 🔲 **Issue #9-10** — Analysis screen UI + API integration
- 🔲 **Issue #15-16** — Buildozer Android build + device testing

**Milestone "POC Ready"** = Issues #1–10, then #15–16 to get on phone.

## Screenshots

_Coming soon_

## Backend

This app requires the `coach-assistant-backend` Django REST API. See that repository for setup instructions. The backend exposes:
- `POST /api/auth/login/` and `/api/auth/register/`
- `GET/POST /api/goals/`
- `GET/POST /api/journal/`
- `POST /api/analysis/generate/`, `GET /api/analysis/latest/`

## Troubleshooting

**"Connection refused" error**
- Ensure the backend API is running (`python manage.py runserver`)
- Check `API_BASE_URL` in `services/api_client.py`
- Use your computer's local IP when testing on phone (not `localhost`)

**Buildozer errors**
- Must be on Linux or WSL
- Install: `sudo apt-get install -y python3-pip build-essential git python3-dev`

## License

Private - All rights reserved

## Author

Mauro Grande

## Acknowledgments

- KivyMD team for the UI framework
- OpenAI for GPT-5.2 API (used in backend analysis)
