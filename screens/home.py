"""Home Screen"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel


class HomeScreen(MDScreen):
    """Main home screen with navigation to other sections"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20,
        )

        # Title
        title = MDLabel(
            text="Welcome",
            halign="center",
            font_style="Display",
        )
        layout.add_widget(title)

        # Navigation buttons
        buttons_layout = MDBoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint=(0.8, None),
            height=250,
            pos_hint={"center_x": 0.5},
        )

        # Goals button
        goals_btn = MDButton(
            style="filled",
            size_hint_x=1,
            on_release=lambda x: self.navigate("goals"),
        )
        goals_btn.add_widget(MDButtonText(text="My Goals"))
        buttons_layout.add_widget(goals_btn)

        # Journal button
        journal_btn = MDButton(
            style="filled",
            size_hint_x=1,
            on_release=lambda x: self.navigate("journal"),
        )
        journal_btn.add_widget(MDButtonText(text="Journal"))
        buttons_layout.add_widget(journal_btn)

        # Analysis button
        analysis_btn = MDButton(
            style="filled",
            size_hint_x=1,
            on_release=lambda x: self.navigate("analysis"),
        )
        analysis_btn.add_widget(MDButtonText(text="Weekly Analysis"))
        buttons_layout.add_widget(analysis_btn)

        # Logout button
        logout_btn = MDButton(
            style="outlined",
            size_hint_x=1,
            on_release=lambda x: self.navigate("login"),
        )
        logout_btn.add_widget(MDButtonText(text="Logout"))
        buttons_layout.add_widget(logout_btn)

        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def navigate(self, screen_name):
        """Navigate to specified screen"""
        self.manager.current = screen_name
