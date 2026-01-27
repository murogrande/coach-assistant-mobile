# Coach Assistant Mobile

KivyMD mobile application for personal coaching and goal tracking.

## Overview

This mobile app helps you:
- Set and track weekly goals
- Write daily journal entries
- Get AI-powered weekly analysis and insights
- Stay motivated with personalized coaching

## Technology Stack

- **Framework**: KivyMD 2.0 (Material Design 3)
- **UI Library**: Kivy 2.3+
- **Platform**: Android via Buildozer
- **Backend**: Django REST API
- **Language**: Python 3.10+

## Project Structure

```
coach-assistant-mobile/
├── main.py                 # App entry point
├── screens/                # UI screens
│   ├── login.py            # Login/authentication
│   ├── home.py             # Navigation hub
│   ├── goals.py            # Weekly goals management
│   ├── journal.py          # Daily journal entries
│   └── analysis.py         # AI weekly analysis
├── services/
│   └── api_client.py       # REST API client
├── tests/                  # Test suite
├── assets/                 # Images, fonts, icons
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
buildozer -v android debug
buildozer android deploy run
```

### Run Tests

```bash
python -m pytest tests/ -v
```

## Current Status

### Implemented
- Basic app structure with navigation
- Login, Home, Goals, Journal, and Analysis screens
- API client with auth, goals, journal, and analysis endpoints
- Test suite (20 tests)

### Pending
- Connect screens to API client
- Form validation and error handling
- Edit/delete functionality
- Calendar view for journal entries

## Troubleshooting

**"Connection refused" error**
- Ensure the backend API is running
- Check API_BASE_URL in `services/api_client.py`
- Use your computer's local IP when testing on phone

**Buildozer errors**
- Ensure you're on Linux or WSL
- Install: `sudo apt-get install -y python3-pip build-essential git python3-dev`

## License

Private - All rights reserved

## Author

Mauro Grande
