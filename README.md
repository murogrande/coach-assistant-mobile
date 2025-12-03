# Coach Assistant Mobile

KivyMD mobile application for personal coaching and goal tracking.

## Overview

This mobile app helps you:
- Set and track weekly goals
- Write daily journal entries
- Get AI-powered weekly analysis and insights
- Stay motivated with personalized coaching

## Technology Stack

- **Framework**: KivyMD 2.x
- **UI Library**: Kivy 2.x
- **Platform**: Android
- **Backend**: Django REST API
- **Language**: Python 3.10+

## Project Structure

```
coach-assistant-mobile/
├── main.py                 # App entry point
├── screens/                # UI screens
│   ├── login.py
│   ├── home.py
│   ├── goals.py
│   ├── journal.py
│   └── analysis.py
├── services/               # Backend communication
│   └── api_client.py
├── utils/                  # Helper functions
├── assets/                 # Images, fonts, etc.
├── buildozer.spec          # Android build configuration
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- pip
- For Android build: Buildozer (Linux) or Kivy Buildozer (Windows/Mac)

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd coach-assistant-mobile

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Edit `services/api_client.py` to set your backend API URL:

```python
API_BASE_URL = "http://your-backend-url:8000/api"
```

### 4. Run on Desktop (Development)

```bash
python main.py
```

### 5. Build for Android

```bash
# Install buildozer (Linux only)
pip install buildozer

# Initialize buildozer
buildozer init

# Build APK (first build takes ~30 minutes)
buildozer -v android debug

# Deploy to connected device
buildozer android deploy run
```

## Features

### Current Features (POC)
- ✅ User registration and login
- ✅ Create and manage weekly goals
- ✅ Mark goals as complete
- ✅ Write daily journal entries
- ✅ Generate AI-powered weekly analysis
- ✅ View analysis results

### Planned Features
- Edit/delete goals and journal entries
- View past analyses
- Calendar view for journal entries
- Progress statistics
- Notifications and reminders

## Screenshots

_Coming soon_

## Backend Setup

This mobile app requires the Coach Assistant Backend to be running. See the backend repository for setup instructions.

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines.

## Troubleshooting

### Common Issues

**"Connection refused" error**
- Ensure the backend API is running
- Check the API_BASE_URL in `services/api_client.py`
- If testing on phone, use your computer's local IP (not localhost)

**Buildozer errors**
- Make sure you're on Linux (or use WSL on Windows)
- Install dependencies: `sudo apt-get install -y python3-pip build-essential git python3-dev`

## Contributing

This is a personal project, but suggestions are welcome!

## License

Private - All rights reserved

## Author

Mauro Grande

## Acknowledgments

- KivyMD team for the amazing UI framework
- OpenAI for GPT-5.1 API
