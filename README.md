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
├── tests/
│   ├── conftest.py         # Headless KivyMD setup, screen_manager fixture
│   ├── test_screens.py     # Unit tests for all screens
│   ├── test_api_client.py  # Unit tests for API client
│   └── end_to_end.py       # End-to-end flow tests (journal + goals)
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

**System dependencies (one-time, Ubuntu/Debian):**
```bash
sudo apt-get install -y build-essential git python3-dev libffi-dev libssl-dev \
    libjpeg-dev libpng-dev zlib1g-dev pkg-config autoconf automake libtool
```

**Pre-flight: set the backend URL before building**

The URL is baked into the APK. Edit `services/api_client.py`:
```python
API_BASE_URL = "http://192.168.x.x:8000/api"   # your laptop's local IP
```

Find your IP with: `ip addr show | grep "inet 192"`

Also make sure the backend is reachable from the phone:
```bash
# In coach-assistant-backend, bind to all interfaces (not just localhost)
python manage.py runserver 0.0.0.0:8000
```
And add your laptop's IP to `ALLOWED_HOSTS` in the backend `.env`:
```
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.x.x
```

**Build:**
```bash
pip install buildozer
buildozer -v android debug       # First build: ~30–60 min (downloads SDK/NDK ~1 GB)
```

**Deploy to phone (USB, with USB debugging enabled):**
```bash
buildozer android deploy run
```

Or manually install the APK from `bin/coachassistant-0.1-debug.apk`.

### Run Tests

```bash
python -m pytest tests/
python -m pytest tests/ -q                  # quiet
python -m pytest tests/ -v                  # verbose
python -m pytest tests/end_to_end.py -v     # end-to-end flows only
```

## Current Status

### Done
- ✅ **Issue #1** — App structure, theme (Blue/Teal), ScreenManager, navigation
- ✅ **Issue #2** — Login screen UI: hero header, form card, field icons, validation, register toggle, password visibility toggle
- ✅ **Issue #3** — Authentication logic: login/register API calls (threaded), JWT token persistence, auto-login on start, error messages
- ✅ **Issue #4** — Home dashboard: greeting, username, stats cards (goals/journal), refresh button, navigation cards
- ✅ **Issue #5** — Goals screen: goal cards with checkboxes, add goal dialog, delete, empty state
- ✅ **Issue #6** — Goals API integration: load, create, toggle complete, delete (all threaded)
- ✅ **Issue #7** — Journal screen UI: text area, date navigation (prev/next), load existing entries, discard confirmation dialog
- ✅ **Issue #8** — Journal API integration: load entry by date, save (create/update), loading feedback, entry id tracking
- ✅ **Issue #9** — Analysis screen UI: week selector, 6 section cards (Summary, Achievements, Improvements, Time, Habits, Blind Spots), loading spinner, empty state, display helpers
- ✅ **Issue #10** — Analysis API integration: load latest on enter, generate with confirmation dialog, threaded API calls, section formatting (str/list/dict), stale-navigation guard (`_active` flag), week nav locked during generation

### Next
- ✅ **Issue #15** — Buildozer configured (`buildozer.spec` created)
- 🔲 **Issue #16** — Test on Android device
- 🔲 **Issue #21–23** — Multi-provider analysis (OpenAI / Claude / Local Qwen3) — requires backend #39–42 first

**Milestone "POC Ready"** = Issues #1–10, then #15–16 to get on phone.
**Milestone "Multi-Provider"** = Backend #39–42 → Mobile #21–23.

## Authentication Flow

1. App starts → checks `~/.coach_assistant_token.json` for a saved token
2. If token found → navigates directly to Home (auto-login)
3. If no token → shows Login screen
4. Login/Register → calls backend API in a background thread → saves JWT access token on success
5. Logout → clears token from memory and disk

## Backend

This app requires the `coach-assistant-backend` Django REST API. See that repository for setup instructions. The backend exposes:

- `POST /api/auth/login/` and `/api/auth/register/`
- `GET/POST /api/goals/`, `PATCH/DELETE /api/goals/{id}/`
- `GET/POST /api/journal/`, `GET /api/journal/by-date/{YYYY-MM-DD}/`, `PATCH /api/journal/{id}/`
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
