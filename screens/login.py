"""Login Screen"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel


class LoginScreen(MDScreen):
    """Login screen for user authentication"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, None),
            height=400,
        )

        # Title
        title = MDLabel(
            text="Coach Assistant",
            halign="center",
            font_style="Display",
        )
        layout.add_widget(title)

        # Username field
        self.username_field = MDTextField(
            mode="outlined",
            size_hint_x=1,
        )
        self.username_field.hint_text = "Username"
        layout.add_widget(self.username_field)

        # Password field
        self.password_field = MDTextField(
            mode="outlined",
            password=True,
            size_hint_x=1,
        )
        self.password_field.hint_text = "Password"
        layout.add_widget(self.password_field)

        # Login button
        login_btn = MDButton(
            style="filled",
            pos_hint={"center_x": 0.5},
            on_release=self.do_login,
        )
        login_btn.add_widget(MDButtonText(text="Login"))
        layout.add_widget(login_btn)

        # Register button
        register_btn = MDButton(
            style="outlined",
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_register,
        )
        register_btn.add_widget(MDButtonText(text="Register"))
        layout.add_widget(register_btn)

        self.add_widget(layout)

    def do_login(self, *args):
        """Handle login button press"""
        username = self.username_field.text
        password = self.password_field.text
        if username and password:
            # TODO: Call api_client.login()
            self.manager.current = "home"

    def go_to_register(self, *args):
        """Navigate to register screen"""
        # TODO: Implement register screen
        pass
