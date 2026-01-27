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
```

## Architecture

KivyMD mobile app (Python) connecting to a Django REST backend for personal coaching and goal tracking.

### Tech Stack
- **UI Framework**: KivyMD 2.0.1.dev0 (Material Design 3) on Kivy 2.3.0
- **HTTP Client**: requests
- **Backend**: Django REST API (separate repository)
- **Target Platform**: Android via Buildozer

### Code Structure

- `main.py` - App entry point with `CoachAssistantApp(MDApp)` class; configures theme (Blue/Light) and ScreenManager
- `screens/` - UI screens (login, home, goals, journal, analysis)
- `services/api_client.py` - REST client singleton handling auth (Bearer token), goals, journal, and analysis endpoints
- `utils/` - Helper functions

### API Client

Import the singleton: `from services.api_client import api_client`

Methods:
- Auth: `login()`, `register()`
- Goals: `get_goals()`, `create_goal()`, `update_goal()`
- Journal: `get_journal_entries()`, `get_journal_by_date()`, `create_journal_entry()`
- Analysis: `generate_analysis()`, `get_latest_analysis()`

**Backend URL**: Set `APIClient.API_BASE_URL` in `services/api_client.py`. For phone testing, use your computer's local IP instead of localhost.
