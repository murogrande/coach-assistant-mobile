"""
Coach Assistant Mobile App
Main entry point for the KivyMD application
"""

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from screens import (
    LoginScreen,
    HomeScreen,
    GoalsScreen,
    JournalScreen,
    AnalysisScreen,
)


class CoachAssistantApp(MDApp):
    """Main application class"""

    def build(self):
        """Build and return the root widget"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        # Screen manager
        sm = ScreenManager()

        # Add screens
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(GoalsScreen(name="goals"))
        sm.add_widget(JournalScreen(name="journal"))
        sm.add_widget(AnalysisScreen(name="analysis"))

        return sm

    def on_start(self):
        """Called when the application starts"""
        print("Coach Assistant App started")


if __name__ == "__main__":
    CoachAssistantApp().run()
