"""Pytest configuration and fixtures for Kivy testing"""

import os
import pytest

# Set environment variables before importing Kivy
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"

# Configure headless mode for CI
if not os.environ.get("DISPLAY"):
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    # get_dpi() calls EventLoop.ensure_window() which aborts on platforms
    # without a display (Windows/macOS CI). Patch it to return a fixed DPI.
    from kivy.metrics import MetricsBase
    MetricsBase.get_dpi = lambda self, force_recompute=False: 96.0

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
    """Initialize MDApp for testing"""
    TestApp.get_app()


@pytest.fixture
def screen_manager():
    """Create a ScreenManager for testing"""
    from kivy.uix.screenmanager import ScreenManager
    return ScreenManager()
