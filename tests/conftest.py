"""Pytest configuration and fixtures for Kivy testing"""

import os
import pytest

# Set environment variables before importing Kivy
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

# Configure headless mode for CI (Linux sets DISPLAY via Xvfb; Windows/macOS don't).
# KIVY_DPI bypasses EventLoop.ensure_window() inside get_dpi(), which is called
# at import time by kivymd.font_definitions.  SDL2 dummy/offscreen drivers can't
# provide an OpenGL context, so we skip window creation entirely and supply a
# fixed DPI.  Widget/canvas tests still need a real display and run Linux-only.
if not os.environ.get("DISPLAY"):
    os.environ["KIVY_DPI"] = "96"
    os.environ["KIVY_METRICS_DENSITY"] = "1"
    os.environ["SDL_AUDIODRIVER"] = "dummy"

from kivy.config import Config
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "600")
Config.set("kivy", "log_level", "warning")


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

    On Linux CI (Xvfb) this succeeds fully.  On Windows/macOS CI there is no
    display so KivyMD's ThemeManager cannot access Window — we catch that and
    let the session continue.  The compat job only runs test_api_client.py
    which has no dependency on MDApp.
    """
    try:
        TestApp.get_app()
    except Exception:
        pass


@pytest.fixture
def screen_manager():
    """Create a ScreenManager for testing"""
    from kivy.uix.screenmanager import ScreenManager
    return ScreenManager()
