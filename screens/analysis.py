"""Analysis Screen"""

import threading
from datetime import date, timedelta

from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.label import MDLabel
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from services.api_client import api_client


BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)

_EMPTY_STATE_TEXT = (
    "No analysis available yet.\n\n"
    "Once you have logged your goals and journal entries for the week, "
    "tap 'Generate Analysis' to receive AI-powered insights about your "
    "progress, patterns, and personalised recommendations."
)

# (field_key, display_title, icon_name)
_SECTIONS = [
    ("summary", "Summary", "text-box-outline"),
    ("achievements", "Goal Achievements", "trophy-outline"),
    ("improvements", "Improvement Suggestions", "lightbulb-outline"),
    ("time_analysis", "Time Analysis", "clock-outline"),
    ("habits_analysis", "Habits Analysis", "repeat"),
    ("blind_spots", "Blind Spots", "eye-outline"),
]


def _monday_of(d: date) -> date:
    return d - timedelta(days=d.weekday())


class AnalysisScreen(MDScreen):
    """Screen for viewing weekly AI analysis"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_week_start = _monday_of(date.today())
        self._section_cards = {}
        self._section_labels = {}
        self._dialog = None
        self._active = False
        self.build_ui()

    def build_ui(self):
        """Construct the full screen layout."""
        root = MDBoxLayout(orientation="vertical")

        # --- Header ---
        header = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=130,
            padding=[16, 28, 16, 8],
            spacing=4,
            md_bg_color=BLUE,
        )
        top_row = MDBoxLayout(orientation="horizontal", adaptive_height=True, spacing=4)
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda _: self.go_back(),
        )
        top_row.add_widget(back_btn)
        top_row.add_widget(MDLabel(
            text="Weekly Analysis",
            font_style="Headline",
            role="small",
            theme_text_color="Custom",
            text_color=WHITE,
            adaptive_height=True,
            pos_hint={"center_y": 0.5},
        ))
        header.add_widget(top_row)
        header.add_widget(MDLabel(
            text="AI-powered insights",
            font_style="Body",
            role="medium",
            theme_text_color="Custom",
            text_color=WHITE_DIM,
            adaptive_height=True,
        ))
        root.add_widget(header)

        # --- Week selector (blue strip) ---
        week_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=48,
            padding=[4, 0, 4, 0],
            md_bg_color=BLUE,
        )
        self._prev_btn = MDIconButton(
            icon="chevron-left",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda _: self._change_week(-1),
        )
        self.week_label = MDLabel(
            text=self._week_text(),
            font_style="Body",
            role="medium",
            theme_text_color="Custom",
            text_color=WHITE,
            halign="center",
            adaptive_height=True,
            pos_hint={"center_y": 0.5},
        )
        self._next_btn = MDIconButton(
            icon="chevron-right",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda _: self._change_week(1),
        )
        week_row.add_widget(self._prev_btn)
        week_row.add_widget(self.week_label)
        week_row.add_widget(self._next_btn)
        root.add_widget(week_row)

        # --- Scrollable content ---
        scroll = MDScrollView(md_bg_color=BG)
        scroll_inner = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=[16, 16, 16, 16],
            spacing=12,
            md_bg_color=BG,
        )

        # Empty state card
        self._empty_card = MDCard(
            orientation="vertical",
            padding=[20, 20, 20, 20],
            style="elevated",
            elevation=1,
            adaptive_height=True,
        )
        self.analysis_text = MDLabel(
            text=_EMPTY_STATE_TEXT,
            font_style="Body",
            role="large",
            halign="left",
            adaptive_height=True,
        )
        self._empty_card.add_widget(self.analysis_text)
        scroll_inner.add_widget(self._empty_card)

        # Analysis section cards (hidden until data loaded)
        for key, title, icon in _SECTIONS:
            card = MDCard(
                orientation="vertical",
                padding=[16, 12, 16, 16],
                style="elevated",
                elevation=1,
                adaptive_height=True,
                opacity=0,
            )
            title_row = MDBoxLayout(
                orientation="horizontal",
                adaptive_height=True,
                spacing=8,
                padding=[0, 0, 0, 8],
            )
            title_row.add_widget(MDIconButton(
                icon=icon,
                theme_icon_color="Custom",
                icon_color=BLUE,
                size_hint=(None, None),
                size=(36, 36),
            ))
            title_row.add_widget(MDLabel(
                text=title,
                font_style="Title",
                role="medium",
                adaptive_height=True,
                pos_hint={"center_y": 0.5},
            ))
            value_lbl = MDLabel(
                text="",
                font_style="Body",
                role="large",
                halign="left",
                adaptive_height=True,
            )
            card.add_widget(title_row)
            card.add_widget(value_lbl)
            self._section_cards[key] = card
            self._section_labels[key] = value_lbl
            scroll_inner.add_widget(card)

        # Loading state
        self._loading_box = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=[16, 40, 16, 40],
            spacing=16,
            opacity=0,
        )
        self._spinner = MDCircularProgressIndicator(
            size_hint=(None, None),
            size=(48, 48),
            pos_hint={"center_x": 0.5},
        )
        self._loading_label = MDLabel(
            text="Generating analysis…\nThis may take 10–30 seconds.",
            font_style="Body",
            role="large",
            halign="center",
            adaptive_height=True,
        )
        self._loading_box.add_widget(self._spinner)
        self._loading_box.add_widget(self._loading_label)
        scroll_inner.add_widget(self._loading_box)

        scroll.add_widget(scroll_inner)
        root.add_widget(scroll)

        # --- Footer ---
        footer = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=80,
            padding=[16, 12, 16, 12],
            md_bg_color=BG,
        )
        self.generate_btn = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.generate_analysis,
        )
        self.generate_btn.add_widget(MDButtonText(text="Generate Analysis"))
        footer.add_widget(self.generate_btn)
        root.add_widget(footer)

        self.add_widget(root)

    # --- Week navigation ---

    def _week_text(self) -> str:
        end = self._current_week_start + timedelta(days=6)
        s = self._current_week_start.strftime('%b %d').replace(' 0', ' ')
        e = end.strftime('%b %d, %Y').replace(' 0', ' ')
        return f"{s} – {e}"

    def _change_week(self, delta: int):
        self._current_week_start += timedelta(weeks=delta)
        self.week_label.text = self._week_text()

    # --- Display helpers ---

    def show_loading(self, loading: bool):
        """Show or hide the loading spinner."""
        self.generate_btn.disabled = loading
        self._prev_btn.disabled = loading
        self._next_btn.disabled = loading
        self._loading_box.opacity = 1 if loading else 0
        if loading:
            self._empty_card.opacity = 0
            self._hide_sections()
            self.week_label.text = "Week navigation unavailable during generation"
        else:
            self.week_label.text = self._week_text()

    @staticmethod
    def _format_section(value) -> str:
        """Format an analysis field value for display.

        Handles str, list, and nested dict-of-lists structures returned by the AI.
        Example for achievements: {"completed_goals": [...], "key_wins": [...]}
        """
        if not value:
            return "—"
        if isinstance(value, str):
            return value.strip() or "—"
        if isinstance(value, list):
            return "\n".join(f"• {item}" for item in value)
        if isinstance(value, dict):
            parts = []
            for k, v in value.items():
                title = k.replace("_", " ").title()
                if isinstance(v, list):
                    parts.append(title + ":")
                    parts.extend(f"  • {item}" for item in v)
                else:
                    parts.append(f"{title}: {v}")
            return "\n".join(parts) if parts else "—"
        return str(value).strip() or "—"

    def show_analysis(self, data: dict):
        """Populate and reveal all analysis section cards."""
        self._empty_card.opacity = 0
        self._loading_box.opacity = 0
        self.generate_btn.disabled = False
        self._prev_btn.disabled = False
        self._next_btn.disabled = False
        self.week_label.text = self._week_text()
        for key, _, _ in _SECTIONS:
            self._section_labels[key].text = self._format_section(data.get(key, ""))
            self._section_cards[key].opacity = 1

    def show_empty_state(self):
        """Show the empty state and hide sections and loading."""
        self._empty_card.opacity = 1
        self._loading_box.opacity = 0
        self.generate_btn.disabled = False
        self._prev_btn.disabled = False
        self._next_btn.disabled = False
        self.week_label.text = self._week_text()
        self._hide_sections()

    def _hide_sections(self):
        for key in self._section_cards:
            self._section_cards[key].opacity = 0

    # --- Navigation & API ---

    def go_back(self):
        """Navigate back to the home screen."""
        self.manager.current = "home"

    def on_enter(self, *_):
        """Load the latest analysis when the screen becomes active."""
        self._active = True
        self.load_latest()

    def on_leave(self, *_):
        self._active = False

    def load_latest(self):
        """Load the most recent analysis from the API."""
        self.show_loading(True)

        def _fetch():
            try:
                data = api_client.get_latest_analysis()
                if data:
                    Clock.schedule_once(lambda _: self._active and self.show_analysis(data))
                else:
                    Clock.schedule_once(lambda _: self._active and self.show_empty_state())
            except Exception as e:
                err = str(e)
                Clock.schedule_once(lambda _: self._active and self._on_error(err, "load"))

        threading.Thread(target=_fetch, daemon=True).start()

    def _on_error(self, message: str, context: str = "load"):
        self.show_empty_state()
        if "401" in message:
            self.analysis_text.text = (
                "Session expired.\n\nPlease go back and log out, then log in again."
            )
        else:
            self.analysis_text.text = f"Failed to {context} analysis.\n\n{message}"

    def generate_analysis(self, *_):
        """Show confirmation dialog before requesting a new analysis."""
        if self._dialog:
            return

        cancel_btn = MDButton(style="text", on_release=lambda _: self._close_dialog())
        cancel_btn.add_widget(MDButtonText(text="Cancel"))

        confirm_btn = MDButton(style="text", on_release=lambda _: self._do_generate())
        confirm_btn.add_widget(MDButtonText(text="Generate"))

        self._dialog = MDDialog(
            MDDialogHeadlineText(text="Generate Analysis?"),
            MDDialogContentContainer(
                MDLabel(
                    text=(
                        "This will call an AI API to analyse your week's goals and "
                        "journal entries. It may take 10–30 seconds and incurs a small cost."
                    ),
                    adaptive_height=True,
                ),
                orientation="vertical",
            ),
            MDDialogButtonContainer(cancel_btn, confirm_btn),
        )
        self._dialog.open()

    def _close_dialog(self):
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None

    def _do_generate(self):
        """Close the dialog and call the generate API in a background thread."""
        self._close_dialog()
        self.show_loading(True)
        week_start_str = self._current_week_start.isoformat()

        def _fetch():
            try:
                result = api_client.generate_analysis(week_start_str)
                # Backend returns the analysis directly (201) or wrapped in
                # {"message": ..., "analysis": {...}} (200 when already exists)
                data = result.get("analysis") or result
                Clock.schedule_once(lambda _: self._active and self.show_analysis(data))
            except Exception as e:
                err = str(e)
                Clock.schedule_once(lambda _: self._active and self._on_error(err, "generate"))

        threading.Thread(target=_fetch, daemon=True).start()
