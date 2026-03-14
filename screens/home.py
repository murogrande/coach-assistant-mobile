"""Home Screen - Issue #4: Home/Dashboard Screen"""

import threading
import datetime

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.icon_definitions import md_icons

from services.api_client import api_client


BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)


def _greeting() -> str:
    """Return a time-appropriate greeting string based on the current hour."""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    if 12 <= hour < 18:
        return "Good afternoon"
    if 18 <= hour < 22:
        return "Good evening"
    return "Good night"


class StatCard(MDCard):
    """Small stats card for the dashboard"""

    def __init__(self, icon: str, value: str, label: str, **kwargs):
        """Build the stat card with an icon, a numeric value, and a label.

        Args:
            icon: Material Design icon name.
            value: Initial value string (e.g. "3/5").
            label: Descriptive label shown below the value.
        """
        super().__init__(
            orientation="vertical",
            padding=[16, 14, 16, 14],
            spacing=4,
            size_hint=(1, None),
            height=90,
            elevation=1,
            style="elevated",
            **kwargs,
        )
        top_row = MDBoxLayout(orientation="horizontal", spacing=8, size_hint=(1, 0.55))
        top_row.add_widget(MDLabel(
            text=md_icons.get(icon, ""),
            font_style="Icon",
            font_size="20sp",
            size_hint=(None, 1),
            width=24,
            theme_text_color="Custom",
            text_color=BLUE,
            valign="center",
        ))
        self.value_label = MDLabel(
            text=value,
            font_style="Title",
            role="large",
            size_hint=(1, 1),
            theme_text_color="Custom",
            text_color=BLUE,
            valign="center",
        )
        top_row.add_widget(self.value_label)
        self.add_widget(top_row)
        self.add_widget(MDLabel(
            text=label,
            font_style="Body",
            role="small",
            theme_text_color="Secondary",
            size_hint=(1, 0.45),
            valign="top",
            halign="left",
        ))


class NavCard(MDCard):
    """Tappable card for home screen navigation"""

    def __init__(self, icon: str, title: str, subtitle: str, on_tap, **kwargs):
        """Build the navigation card with icon, title, subtitle, and chevron.

        Args:
            icon: Material Design icon name.
            title: Bold primary text.
            subtitle: Secondary descriptive text.
            on_tap: Callable invoked when the card is tapped.
        """
        super().__init__(
            orientation="horizontal",
            padding=[20, 18, 20, 18],
            spacing=20,
            size_hint=(1, None),
            height=130,
            elevation=1,
            style="elevated",
            ripple_behavior=True,
            **kwargs,
        )
        self._on_tap = on_tap

        self.add_widget(MDLabel(
            text=md_icons.get(icon, ""),
            font_style="Icon",
            font_size="32sp",
            size_hint=(None, 1),
            width=48,
            halign="center",
            theme_text_color="Custom",
            text_color=BLUE,
        ))

        text_col = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            padding=[0, 10, 0, 10],
        )
        text_col.add_widget(MDLabel(
            text=title,
            font_style="Title",
            role="medium",
            size_hint_y=0.55,
            valign="bottom",
            halign="left",
        ))
        text_col.add_widget(MDLabel(
            text=subtitle,
            font_style="Body",
            role="small",
            theme_text_color="Secondary",
            size_hint_y=0.45,
            valign="top",
            halign="left",
        ))
        self.add_widget(text_col)

        self.add_widget(MDLabel(
            text=md_icons.get("chevron-right", ""),
            font_style="Icon",
            font_size="24sp",
            size_hint=(None, 1),
            width=32,
            halign="center",
            theme_text_color="Secondary",
        ))

    def on_touch_down(self, touch):
        """Invoke the tap callback when the card is touched."""
        if self.collide_point(*touch.pos):
            self._on_tap()
            return True
        return super().on_touch_down(touch)


class HomeScreen(MDScreen):
    """Main home screen with navigation to other sections"""

    def __init__(self, **kwargs):
        """Initialise and build the home screen UI."""
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Construct the full screen layout (header, stats, nav cards, logout)."""
        root = MDBoxLayout(orientation="vertical")

        # --- Hero header ---
        header = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=160,
            padding=[24, 28, 24, 16],
            spacing=4,
            md_bg_color=BLUE,
        )

        top_row = MDBoxLayout(orientation="horizontal", adaptive_height=True)
        title_col = MDBoxLayout(orientation="vertical", spacing=4, size_hint_x=1, adaptive_height=True)
        self.greeting_label = MDLabel(
            text=f"{_greeting()}!",
            font_style="Display",
            role="small",
            theme_text_color="Custom",
            text_color=WHITE,
            adaptive_height=True,
        )
        self.username_label = MDLabel(
            text="",
            font_style="Body",
            role="large",
            theme_text_color="Custom",
            text_color=WHITE_DIM,
            adaptive_height=True,
        )
        title_col.add_widget(self.greeting_label)
        title_col.add_widget(self.username_label)
        top_row.add_widget(title_col)

        self.refresh_btn = MDIconButton(
            icon="refresh",
            theme_icon_color="Custom",
            icon_color=WHITE,
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self.load_stats(),
        )
        top_row.add_widget(self.refresh_btn)
        header.add_widget(top_row)
        root.add_widget(header)

        # --- Content ---
        content_bg = MDBoxLayout(orientation="vertical", md_bg_color=BG)
        scroll = MDScrollView()
        inner = MDBoxLayout(
            orientation="vertical",
            padding=[16, 16, 16, 16],
            spacing=18,
            adaptive_height=True,
        )

        # Stats row
        stats_row = MDBoxLayout(
            orientation="horizontal",
            spacing=12,
            size_hint=(1, None),
            height=90,
        )
        self.goals_stat = StatCard(icon="flag-checkered", value="—", label="Goals this week")
        self.journal_stat = StatCard(icon="notebook", value="—", label="Journal entries")
        stats_row.add_widget(self.goals_stat)
        stats_row.add_widget(self.journal_stat)
        inner.add_widget(stats_row)

        # Nav cards
        inner.add_widget(NavCard(
            icon="flag-checkered",
            title="My Goals",
            subtitle="Track your weekly goals",
            on_tap=lambda: self.navigate("goals"),
        ))
        inner.add_widget(NavCard(
            icon="notebook",
            title="Journal",
            subtitle="Write your daily entry",
            on_tap=lambda: self.navigate("journal"),
        ))
        inner.add_widget(NavCard(
            icon="chart-bar",
            title="Weekly Analysis",
            subtitle="Review your progress",
            on_tap=lambda: self.navigate("analysis"),
        ))

        # Logout
        logout_row = MDBoxLayout(size_hint=(1, None), height=80, padding=[0, 40, 0, 0])
        logout_btn = MDButton(
            style="text",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.do_logout,
        )
        logout_btn.add_widget(MDButtonText(text="Logout"))
        logout_row.add_widget(logout_btn)
        inner.add_widget(logout_row)

        scroll.add_widget(inner)
        content_bg.add_widget(scroll)
        root.add_widget(content_bg)
        self.add_widget(root)

    def on_pre_enter(self, *args):
        """Refresh user info and stats every time the screen is shown"""
        self.greeting_label.text = f"{_greeting()}!"
        name = api_client.username or ""
        self.username_label.text = f"Welcome back, {name}" if name else "What would you like to do today?"
        self.load_stats()

    def load_stats(self):
        """Load goal and journal counts from API in background thread"""
        def _fetch():
            goals_value = "—"
            journal_value = "—"
            try:
                goals = api_client.get_goals()
                completed = sum(1 for g in goals if g.get("completed"))
                goals_value = f"{completed}/{len(goals)}"
            except Exception:
                pass
            try:
                entries = api_client.get_journal_entries()
                journal_value = str(len(entries))
            except Exception:
                pass
            Clock.schedule_once(lambda dt: self._update_stats(goals_value, journal_value))

        threading.Thread(target=_fetch, daemon=True).start()

    def _update_stats(self, goals_value: str, journal_value: str):
        """Update the goals and journal stat card values on the main thread."""
        self.goals_stat.value_label.text = goals_value
        self.journal_stat.value_label.text = journal_value

    def navigate(self, screen_name):
        """Navigate to the given screen by name."""
        self.manager.current = screen_name

    def do_logout(self, *args):
        """Clear the auth token and return to the login screen."""
        api_client.logout()
        self.manager.current = "login"
