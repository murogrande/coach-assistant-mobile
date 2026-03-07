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
python -m pytest tests/test_screens.py::TestLoginScreen::test_login_screen_creation  # single test
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
- Goals: `get_goals()`, `create_goal()`, `update_goal()`, `delete_goal()`
- Journal: `get_journal_entries()`, `get_journal_by_date(date_str)`, `create_journal_entry(date_str, content)`, `update_journal_entry(entry_id, content)`
- Analysis: `generate_analysis(week_start_date)`, `get_latest_analysis()`

**Backend URL**: Set `APIClient.API_BASE_URL` in `services/api_client.py`. For phone testing, use your computer's local IP instead of localhost.

**Token format**: Backend returns `tokens.access` and `tokens.refresh` (not `token`). Use `Authorization: Bearer <access_token>`.

### Backend API endpoints (verified)

Always check `../coach-assistant-backend/api/views.py` before implementing new API calls.

| Resource | Endpoint | Notes |
|---|---|---|
| Journal list/create | `GET/POST /api/journal/` | |
| Journal by date | `GET /api/journal/by-date/{YYYY-MM-DD}/` | Returns single entry or 404 |
| Journal by ID | `GET/PATCH/DELETE /api/journal/{id}/` | Use numeric id, NOT date |
| Goals | `GET/POST /api/goals/`, `PATCH /api/goals/{id}/` | |
| Analysis generate | `POST /api/analysis/generate/` | Body: `{week_start_date, provider}` (provider optional, default `"openai"`) |
| Analysis latest | `GET /api/analysis/latest/` | Query: `?provider=openai\|anthropic\|local` (optional) |
| Analysis list | `GET /api/analysis/` | Returns all analyses (pending backend #42) |

## Screen Layout Pattern

All screens follow this consistent structure:
1. **Blue header** (`md_bg_color=BLUE`, `height=130`): horizontal top row with `MDIconButton(icon="arrow-left")` back button + title `MDLabel`, plus subtitle label below
2. **Light gray content** (`md_bg_color=BG`): `MDScrollView` wrapping an `MDBoxLayout(adaptive_height=True)` with the main content
3. **Fixed footer** (`md_bg_color=BG`, `height=80`): primary action `MDButton(style="filled", theme_width="Custom", size_hint_x=1)`

**Analysis screen exception**: has an extra blue strip (`height=48`) below the header for the week selector (`<` / `>` navigation + week range label).

Color constants used in every screen:
```python
BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)
```

## KivyMD 2.x Quirks

- **Full-width buttons**: `MDButton` requires `theme_width="Custom"` + `size_hint_x=1` to fill parent width. `size_hint_x=1` alone does not work.
- **TextField icons**: Use child widgets, not constructor args:
  ```python
  field.add_widget(MDTextFieldLeadingIcon(icon="account"))
  ```
- **`MDTextFieldTrailingIcon`** does not receive touch events (parent `MDTextField` consumes them) — use a standalone `MDIconButton` positioned over the field instead.
- **`adaptive_width`** and **`leading_icon`** are NOT valid constructor parameters for MDButton/MDTextField in this version.
- **Threading**: API calls must run in background threads. Use `threading.Thread` + `Clock.schedule_once` to update UI from the main thread.
- **`MDTextField multiline=True`** has rendering issues (text may not appear) — use native Kivy `TextInput` for multiline content areas instead.

## Issue Progress

| Issue | Title | Status |
|-------|-------|--------|
| #1 | Setup KivyMD Project Configuration | ✅ Done |
| #2 | Implement Login Screen UI | ✅ Done |
| #3 | Implement Authentication Logic | ✅ Done |
| #4 | Create Home/Dashboard Screen | ✅ Done |
| #5 | Implement Weekly Goals Screen UI | ✅ Done |
| #6 | Implement Goals API Integration | ✅ Done |
| #7 | Implement Daily Journal Screen UI | ✅ Done |
| #8 | Implement Journal API Integration | ✅ Done |
| #9 | Implement Weekly Analysis Screen UI | ✅ Done |
| #10 | Implement Analysis API Integration | ✅ Done |
| #15 | Setup Buildozer for Android Build | 🔲 Pending |
| #16 | Test on Android Device | 🔲 Pending |
| #21 | Multi-Provider Support in API Client | 🔲 Pending |
| #22 | Provider Selector UI on Analysis Screen | 🔲 Pending |
| #23 | Compare Analyses from Multiple Providers | 🔲 Pending |

**Milestone "POC Ready"** = Issues #1–10, then #15–16 to get on phone.
**Milestone "Multi-Provider"** = Issues #21–23 (mobile) + #39–42 (backend). Requires backend work first.

### Analysis screen (Issues #9 + #10) — what's implemented

- Blue header + week selector strip (`<` week range `>`)
- 6 section cards (hidden until data loads): Summary, Goal Achievements, Improvement Suggestions, Time Analysis, Habits Analysis, Blind Spots
- Loading spinner (`MDCircularProgressIndicator`) + message
- Empty state card with placeholder text
- Display helpers: `show_analysis(data)`, `show_loading(bool)`, `show_empty_state()`
- `analysis_text` attribute preserved for test compatibility
- `on_enter` calls `load_latest()` automatically; `on_leave` clears `_active` flag
- `_active` flag guards all `Clock.schedule_once` callbacks — UI skipped if user navigated away
- Week nav buttons (`_prev_btn`, `_next_btn`) disabled during generation; week label replaced with "Week navigation unavailable during generation"
- `generate_analysis()` shows confirmation dialog before calling API
- `_do_generate()` unwraps `{"analysis": {...}}` wrapper (200) or uses response directly (201)
- `_on_error(message, context)` handles load/generate errors with 401 detection
- `_format_section(value)` handles str, list, dict-of-lists for display

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
- 95 tests currently passing
- Unit tests: `tests/test_screens.py`, `tests/test_api_client.py`
- End-to-end flow tests: `tests/end_to_end.py` (journal and goals full cycles)
