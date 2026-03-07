"""Pytest configuration and fixtures for Kivy testing"""

import os
import pytest

# Set environment variables before importing Kivy
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

# Configure headless mode for CI (Linux sets DISPLAY via Xvfb; Windows/macOS don't).
# KIVY_DPI bypasses EventLoop.ensure_window() inside get_dpi(), which is called
# at import time by kivymd.font_definitions.  Widget/canvas tests still need a
# real display and run Linux-only.
if not os.environ.get("DISPLAY"):
    os.environ["KIVY_DPI"] = "96"
    os.environ["KIVY_METRICS_DENSITY"] = "1"
    os.environ["SDL_AUDIODRIVER"] = "dummy"

# Kivy may not be installed in minimal CI environments (compat job installs only
# requests + pytest).  Guard all Kivy imports so test_api_client.py can still run.
try:
    from kivy.config import Config
    Config.set("graphics", "width", "400")
    Config.set("graphics", "height", "600")
    Config.set("kivy", "log_level", "warning")
    _KIVY_AVAILABLE = True
except ModuleNotFoundError:
    _KIVY_AVAILABLE = False


class TestApp:
    """Minimal app context for testing KivyMD widgets"""
    _instance = None

    def __init__(self):
        from kivymd.app import MDApp

        if TestApp._instance is None:
            self.app = MDApp()
            self.app.theme_cls.primary_palette = "Blue"
            TestApp._instance = self.app

    @classmethod
    def get_app(cls):
        if cls._instance is None:
            TestApp()
        return cls._instance


@pytest.fixture(scope="session", autouse=True)
def setup_app():
    """Initialize MDApp for testing.

    On Linux CI (Xvfb) this succeeds fully.  On Windows/macOS CI Kivy may not
    be installed at all, or the ThemeManager cannot access Window — both cases
    are caught so test_api_client.py (no GUI dependency) can still run.
    """
    if not _KIVY_AVAILABLE:
        return
    try:
        TestApp.get_app()
    except Exception:
        pass


@pytest.fixture
def screen_manager():
    """Create a ScreenManager for testing"""
    from kivy.uix.screenmanager import ScreenManager
    return ScreenManager()
