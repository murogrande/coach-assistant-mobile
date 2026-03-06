"""Journal Screen"""

import datetime
import threading

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.textfield import MDTextField

from services.api_client import api_client


BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)


class JournalScreen(MDScreen):
    """Screen for daily journal entries"""

    def __init__(self, **kwargs):
        """Initialise state and build the journal screen UI."""
        super().__init__(**kwargs)
        self.current_date = datetime.date.today()
        self._original_text = ""
        self._entry_exists = False
        self._dialog = None
        self.build_ui()

    def build_ui(self):
        """Construct the full screen layout (header, text area, save footer)."""
        root = MDBoxLayout(orientation="vertical")

        # --- Header ---
        header = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=160,
            padding=[16, 28, 16, 16],
            spacing=4,
            md_bg_color=BLUE,
        )
        top_row = MDBoxLayout(orientation="horizontal", adaptive_height=True, spacing=4)
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda x: self.go_back(),
        )
        top_row.add_widget(back_btn)
        top_row.add_widget(MDLabel(
            text="Daily Journal",
            font_style="Headline",
            role="small",
            theme_text_color="Custom",
            text_color=WHITE,
            adaptive_height=True,
            pos_hint={"center_y": 0.5},
        ))
        header.add_widget(top_row)

        # Date navigation row
        date_nav = MDBoxLayout(orientation="horizontal", adaptive_height=True, spacing=4)
        self.prev_btn = MDIconButton(
            icon="chevron-left",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda x: self.navigate_date(-1),
        )
        date_nav.add_widget(self.prev_btn)

        self.date_label = MDLabel(
            text=self._format_date(self.current_date),
            font_style="Body",
            role="medium",
            theme_text_color="Custom",
            text_color=WHITE_DIM,
            adaptive_height=True,
            halign="center",
            pos_hint={"center_y": 0.5},
        )
        date_nav.add_widget(self.date_label)

        self.next_btn = MDIconButton(
            icon="chevron-right",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda x: self.navigate_date(1),
        )
        date_nav.add_widget(self.next_btn)
        header.add_widget(date_nav)
        self._update_nav_buttons()
        root.add_widget(header)

        # --- Content ---
        content = MDBoxLayout(
            orientation="vertical",
            padding=[16, 16, 16, 0],
            spacing=12,
            md_bg_color=BG,
        )

        content.add_widget(MDLabel(
            text="How was your day?",
            font_style="Title",
            role="small",
            adaptive_height=True,
        ))

        card = MDCard(
            orientation="vertical",
            padding=[4, 4, 4, 4],
            style="elevated",
            elevation=1,
        )
        self.journal_field = MDTextField(
            mode="outlined",
            multiline=True,
            hint_text="Write about your day, thoughts, feelings...",
            size_hint=(1, 1),
        )
        card.add_widget(self.journal_field)
        content.add_widget(card)

        root.add_widget(content)

        # --- Footer ---
        footer = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=100,
            padding=[16, 8, 16, 12],
            spacing=4,
            md_bg_color=BG,
        )
        self.status_label = MDLabel(
            text="",
            font_style="Body",
            role="small",
            adaptive_height=True,
            halign="center",
        )
        footer.add_widget(self.status_label)
        self.save_btn = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.save_entry,
        )
        self.save_btn_text = MDButtonText(text="Save Entry")
        self.save_btn.add_widget(self.save_btn_text)
        footer.add_widget(self.save_btn)
        root.add_widget(footer)

        self.add_widget(root)

    def _format_date(self, date):
        """Return a human-readable date string."""
        return date.strftime("%A, %B %d")

    def _update_nav_buttons(self):
        """Disable the next button when already on today's date."""
        self.next_btn.disabled = self.current_date >= datetime.date.today()

    def on_pre_enter(self):
        """Load the journal entry for the current date each time the screen is shown."""
        self.load_entry(self.current_date)

    def navigate_date(self, delta):
        """Navigate to the previous (-1) or next (+1) day, prompting if unsaved changes exist."""
        if self._has_unsaved_changes():
            self._show_discard_dialog(on_discard=lambda: self._do_navigate_date(delta))
        else:
            self._do_navigate_date(delta)

    def _do_navigate_date(self, delta):
        """Apply a day offset, refresh the header and load the new entry."""
        new_date = self.current_date + datetime.timedelta(days=delta)
        if new_date > datetime.date.today():
            return
        self.current_date = new_date
        self.date_label.text = self._format_date(self.current_date)
        self._update_nav_buttons()
        self.journal_field.text = ""
        self._original_text = ""
        self.load_entry(self.current_date)

    def _has_unsaved_changes(self):
        """Return True if the text area content differs from the last saved/loaded text."""
        return self.journal_field.text.strip() != self._original_text.strip()

    def load_entry(self, date):
        """Load the journal entry for the given date from the API (Issue #8)."""
        date_str = date.isoformat()

        def _do():
            try:
                entry = api_client.get_journal_by_date(date_str)
                text = entry.get("content", "") if entry else ""
            except Exception:
                text = ""
            Clock.schedule_once(lambda dt: self._set_entry_text(text))

        threading.Thread(target=_do, daemon=True).start()

    def _set_entry_text(self, text):
        """Populate the text field and record the baseline for change detection."""
        self.journal_field.text = text
        self._original_text = text
        self._entry_exists = bool(text)

    def save_entry(self, *args):
        """Save the current journal entry via the API (Issue #8)."""
        content = self.journal_field.text.strip()
        if not content:
            return
        date_str = self.current_date.isoformat()
        exists = self._entry_exists

        self.save_btn.disabled = True
        self.save_btn_text.text = "Saving..."
        self.status_label.text = ""

        def _do():
            try:
                if exists:
                    api_client.update_journal_entry(date_str, content)
                else:
                    api_client.create_journal_entry(date_str, content)
                Clock.schedule_once(lambda dt: self._on_save_success(content))
            except Exception as e:
                err = str(e)
                Clock.schedule_once(lambda dt: self._on_save_error(err))

        threading.Thread(target=_do, daemon=True).start()

    def _on_save_success(self, content):
        """Handle successful save: update state and re-enable the button."""
        self._original_text = content
        self._entry_exists = True
        self.save_btn.disabled = False
        self.save_btn_text.text = "Save Entry"
        self.status_label.text = "Saved"

    def _on_save_error(self, error):
        """Handle save failure: show error and re-enable the button."""
        self.save_btn.disabled = False
        self.save_btn_text.text = "Save Entry"
        self.status_label.text = f"Error: {error}"

    def go_back(self):
        """Navigate back to home, showing a discard dialog if there are unsaved changes."""
        if self._has_unsaved_changes():
            self._show_discard_dialog(on_discard=self._navigate_back)
        else:
            self._navigate_back()

    def _navigate_back(self):
        """Perform the actual screen transition to home."""
        self.manager.current = "home"

    def _show_discard_dialog(self, on_discard):
        """Open a confirmation dialog before discarding unsaved changes."""
        if self._dialog:
            return
        keep_btn = MDButton(style="text", on_release=lambda x: self._close_dialog())
        keep_btn.add_widget(MDButtonText(text="Keep editing"))

        discard_btn = MDButton(style="text", on_release=lambda x: self._confirm_discard(on_discard))
        discard_btn.add_widget(MDButtonText(text="Discard"))

        self._dialog = MDDialog(
            MDDialogHeadlineText(text="Discard changes?"),
            MDDialogContentContainer(
                MDLabel(
                    text="Your unsaved changes will be lost.",
                    adaptive_height=True,
                ),
                orientation="vertical",
            ),
            MDDialogButtonContainer(keep_btn, discard_btn),
        )
        self._dialog.open()

    def _confirm_discard(self, on_discard):
        """Close the dialog and run the discard callback."""
        self._close_dialog()
        self._original_text = self.journal_field.text
        on_discard()

    def _close_dialog(self):
        """Dismiss the active dialog and clear the reference."""
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None
