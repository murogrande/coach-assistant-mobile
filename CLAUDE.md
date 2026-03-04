# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands

**Install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Desktop development:**
```bash
python main.py
```

**Android build (requires Linux or WSL):**
```bash
pip install buildozer
buildozer init
buildozer -v android debug
buildozer android deploy run
```

**Run tests:**
```bash
python -m pytest tests/
python -m pytest tests/ -q   # quiet
python -m pytest tests/ -v   # verbose
```

**Screenshot (for UI debugging):**
```bash
import -window root /tmp/screenshot.png
```

## Architecture

KivyMD mobile app (Python) connecting to a Django REST backend for personal coaching and goal tracking.

### Tech Stack
- **UI Framework**: KivyMD 2.0.1.dev0 (Material Design 3) on Kivy 2.3.1
- **HTTP Client**: requests
- **Backend**: Django REST API (separate repository: `coach-assistant-backend`)
- **Target Platform**: Android via Buildozer

### Code Structure

- `main.py` - App entry point with `CoachAssistantApp(MDApp)` class; configures theme (Blue/Teal/Light) and ScreenManager
- `screens/` - UI screens (login, home, goals, journal, analysis)
- `services/api_client.py` - REST client singleton handling auth (Bearer token), goals, journal, and analysis endpoints
- `utils/` - Helper functions
- `tests/` - pytest tests with KivyMD headless setup in `conftest.py`

### API Client

Import the singleton: `from services.api_client import api_client`

Methods:
- Auth: `login()`, `register()`
- Goals: `get_goals()`, `create_goal()`, `update_goal()`
- Journal: `get_journal_entries()`, `get_journal_by_date()`, `create_journal_entry()`
- Analysis: `generate_analysis()`, `get_latest_analysis()`

**Backend URL**: Set `APIClient.API_BASE_URL` in `services/api_client.py`. For phone testing, use your computer's local IP instead of localhost.

**Token format**: Backend returns `tokens.access` and `tokens.refresh` (not `token`). Use `Authorization: Bearer <access_token>`.

## KivyMD 2.x Quirks

- **Full-width buttons**: `MDButton` requires `theme_width="Custom"` + `size_hint_x=1` to fill parent width. `size_hint_x=1` alone does not work.
- **TextField icons**: Use child widgets, not constructor args:
  ```python
  field.add_widget(MDTextFieldLeadingIcon(icon="account"))
  ```
- **`adaptive_width`** and **`leading_icon`** are NOT valid constructor parameters for MDButton/MDTextField in this version.
- **Threading**: API calls must run in background threads. Use `threading.Thread` + `Clock.schedule_once` to update UI from the main thread.

## Issue Progress

| Issue | Title | Status |
|-------|-------|--------|
| #1 | Setup KivyMD Project Configuration | ✅ Done |
| #2 | Implement Login Screen UI | ✅ Done |
| #3 | Implement Authentication Logic | ✅ Done |
| #4 | Create Home/Dashboard Screen | ✅ Done |
| #5 | Implement Weekly Goals Screen UI | ✅ Done |
| #6 | Implement Goals API Integration | 🔲 Next |
| #7 | Implement Daily Journal Screen UI | ✅ Done |
| #8 | Implement Journal API Integration | 🔲 Next |
| #9 | Implement Weekly Analysis Screen UI | ✅ Done |
| #10 | Implement Analysis API Integration | 🔲 Next |
| #15 | Setup Buildozer for Android Build | 🔲 Pending |
| #16 | Test on Android Device | 🔲 Pending |

**Milestone "POC Ready"** = Issues #1–10, then #15–16 to get on phone.

## Authentication (Issue #3)

- `api_client.login()` extracts token from `tokens.access` (JWT) or fallback `token` field
- Token saved to `~/.coach_assistant_token.json` via `save_token()` / `load_token()`
- `main.py` `on_start()` calls `load_token()` → auto-navigates to home if token exists
- API calls run in background threads; UI updates via `Clock.schedule_once`
- `logout()` clears token from memory and deletes the file

## Testing Guidelines

- Always mock API calls using `unittest.mock.patch`
- Use the `screen_manager` fixture from `conftest.py` for screen tests
- Tests run headlessly (SDL dummy driver configured in `conftest.py`)
- 41 tests currently passing
