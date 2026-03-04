"""Login Screen - Issue #2: Login Screen UI"""

import threading

import requests
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

from services.api_client import api_client


class LoginScreen(MDScreen):
    """Login screen for user authentication"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_register_mode = False
        self.build_ui()

    def build_ui(self):
        # Root layout
        root = MDBoxLayout(orientation="vertical")

        # --- Hero header ---
        self.header = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 0.38),
            padding=[40, 40, 40, 20],
            spacing=8,
            md_bg_color=(0.129, 0.588, 0.953, 1),  # Blue 500
        )

        title = MDLabel(
            text="Coach Assistant",
            halign="center",
            font_style="Display",
            role="small",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        )
        subtitle = MDLabel(
            text="Your personal AI coach",
            halign="center",
            font_style="Body",
            role="large",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.85),
        )
        self.header.add_widget(title)
        self.header.add_widget(subtitle)
        root.add_widget(self.header)

        # --- Form area ---
        form_area = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 0.62),
            padding=[24, 16, 24, 24],
            md_bg_color=(0.96, 0.96, 0.96, 1),
        )

        # Card fills the form area
        card = MDCard(
            orientation="vertical",
            padding=[28, 24, 28, 24],
            spacing=14,
            size_hint=(1, 1),
            elevation=2,
            style="elevated",
        )

        self.form_title = MDLabel(
            text="Sign In",
            halign="center",
            font_style="Title",
            role="large",
            size_hint_y=None,
            height=36,
        )
        card.add_widget(self.form_title)

        self.username_field = MDTextField(
            mode="outlined",
            hint_text="Username",
            size_hint_x=1,
        )
        self.username_field.add_widget(MDTextFieldLeadingIcon(icon="account"))
        card.add_widget(self.username_field)

        password_row = MDBoxLayout(
            orientation="horizontal",
            spacing=4,
            size_hint_x=1,
            adaptive_height=True,
        )
        self.password_field = MDTextField(
            mode="outlined",
            hint_text="Password",
            password=True,
            size_hint_x=1,
        )
        self.password_field.add_widget(MDTextFieldLeadingIcon(icon="lock"))
        password_row.add_widget(self.password_field)

        self.eye_btn = MDIconButton(
            icon="eye",
            on_release=self.toggle_password_visibility,
        )
        password_row.add_widget(self.eye_btn)
        card.add_widget(password_row)

        # Error label
        self.error_label = MDLabel(
            text="",
            halign="center",
            font_style="Body",
            role="medium",
            theme_text_color="Custom",
            text_color=(0.8, 0.1, 0.1, 1),
            size_hint_y=None,
            height=24,
        )
        card.add_widget(self.error_label)

        # Primary action button
        self.action_btn = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.do_action,
        )
        self.action_btn_text = MDButtonText(text="Login")
        self.action_btn.add_widget(self.action_btn_text)
        card.add_widget(self.action_btn)

        # Toggle register / login
        self.toggle_btn = MDButton(
            style="text",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.toggle_mode,
        )
        self.toggle_btn_text = MDButtonText(
            text="Don't have an account? Register"
        )
        self.toggle_btn.add_widget(self.toggle_btn_text)
        card.add_widget(self.toggle_btn)

        form_area.add_widget(card)
        root.add_widget(form_area)
        self.add_widget(root)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self):
        username = self.username_field.text.strip()
        password = self.password_field.text

        if not username:
            self.show_error("Username is required")
            return False
        if not password:
            self.show_error("Password is required")
            return False
        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return False
        return True

    # ------------------------------------------------------------------
    # UI helpers
    # ------------------------------------------------------------------

    def show_error(self, message):
        self.error_label.text = message

    def clear_error(self):
        self.error_label.text = ""

    def toggle_password_visibility(self, *args):
        self.password_field.password = not self.password_field.password
        self.eye_btn.icon = "eye-off" if not self.password_field.password else "eye"

    def toggle_mode(self, *args):
        self.is_register_mode = not self.is_register_mode
        self.clear_error()
        if self.is_register_mode:
            self.form_title.text = "Create Account"
            self.action_btn_text.text = "Register"
            self.toggle_btn_text.text = "Already have an account? Sign In"
        else:
            self.form_title.text = "Sign In"
            self.action_btn_text.text = "Login"
            self.toggle_btn_text.text = "Don't have an account? Register"

    def _set_loading(self, loading: bool):
        """Disable/enable button during API call"""
        self.action_btn.disabled = loading

    def _parse_error(self, exception: Exception) -> str:
        """Extract a user-friendly message from a requests exception"""
        if isinstance(exception, requests.HTTPError):
            try:
                data = exception.response.json()
                for key in ("detail", "non_field_errors", "message", "error"):
                    if key in data:
                        val = data[key]
                        return val[0] if isinstance(val, list) else str(val)
                return f"Error {exception.response.status_code}"
            except Exception:
                return f"Error {exception.response.status_code}"
        return str(exception)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def do_action(self, *args):
        self.clear_error()
        if not self.validate():
            return
        if self.is_register_mode:
            self.do_register()
        else:
            self.do_login()

    def do_login(self):
        username = self.username_field.text.strip()
        password = self.password_field.text
        self._set_loading(True)

        def _login():
            try:
                api_client.login(username, password)
                Clock.schedule_once(lambda dt: self._on_auth_success())
            except Exception as e:
                msg = self._parse_error(e)
                Clock.schedule_once(lambda dt: self._on_auth_error(msg))

        threading.Thread(target=_login, daemon=True).start()

    def do_register(self):
        username = self.username_field.text.strip()
        password = self.password_field.text
        self._set_loading(True)

        def _register():
            try:
                api_client.register(username, password)
                api_client.login(username, password)
                Clock.schedule_once(lambda dt: self._on_auth_success())
            except Exception as e:
                msg = self._parse_error(e)
                Clock.schedule_once(lambda dt: self._on_auth_error(msg))

        threading.Thread(target=_register, daemon=True).start()

    def _on_auth_success(self):
        self._set_loading(False)
        self.manager.current = "home"

    def _on_auth_error(self, message: str):
        self._set_loading(False)
        self.show_error(message)
