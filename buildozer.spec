[app]

# App identity
title = Coach Assistant
package.name = coachassistant
package.domain = org.mauro
version = 0.1

# Source
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json
source.exclude_dirs = venv,.git,tests,.buildozer,htmlcov,.pytest_cache,.mypy_cache,.github,.claude
source.exclude_patterns = *.spec,*.pyc,*.pyo,test_*.py,conftest.py

# Requirements
# NOTE: Before building for phone, set API_BASE_URL in services/api_client.py
#       to your laptop's local IP (e.g. http://192.168.1.100:8000/api)
# KivyMD is pinned to GitHub master (same as requirements.txt) — not the PyPI release.
requirements = python3,kivy==2.3.1,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,asynckivy,asyncgui,requests,python-dateutil,certifi,urllib3,charset-normalizer,idna

# Icon / splash (uncomment once assets/icon.png exists)
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/splash.png

orientation = portrait
fullscreen = 0

# Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
# Allow plain HTTP to local backend (http://192.168.x.x:8000).
# Injects android:usesCleartextTraffic="true" into <application> in AndroidManifest.
# Remove this if you switch to HTTPS in production.
android.manifest.application_attributes = android:usesCleartextTraffic="true"

# python-for-android
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
