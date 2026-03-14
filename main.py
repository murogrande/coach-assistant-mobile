"""
Coach Assistant Mobile App
Main entry point for the KivyMD application
"""

from kivy.config import Config

Config.set("input", "mouse", "mouse,disable_multitouch")
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "800")

from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from screens import (
    LoginScreen,
    HomeScreen,
    GoalsScreen,
    JournalScreen,
    AnalysisScreen,
)
from services.api_client import api_client


class CoachAssistantApp(MDApp):
    """Main application class"""

    def build(self):
        """Build and return the root widget"""
        Window.minimum_width = 320
        Window.minimum_height = 500
        Window.softinput_mode = "below_target"
        self._resize_trigger = Clock.create_trigger(self._on_resize_settle, 0.15)
        Window.bind(on_resize=lambda *_: self._resize_trigger())
        Window.bind(on_keyboard=self._on_keyboard)

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        # Screen manager
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(GoalsScreen(name="goals"))
        sm.add_widget(JournalScreen(name="journal"))
        sm.add_widget(AnalysisScreen(name="analysis"))

        return sm

    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle the Android hardware back button (key 27 = ESC/back)."""
        if key == 27:
            current = self.root.current
            if current in ("goals", "journal", "analysis"):
                self.root.current = "home"
                return True  # consume — prevents the app from exiting
        return False

    def _on_resize_settle(self, dt):
        """Called once after the window stops being resized (debounced 150 ms)."""
        if self.root:
            self.root.do_layout()

    def on_start(self):
        """Called when the application starts"""
        print("Coach Assistant App started")
        if api_client.load_token():
            self.root.current = "home"


if __name__ == "__main__":
    CoachAssistantApp().run()
