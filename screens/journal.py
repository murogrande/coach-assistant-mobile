"""Journal Screen"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class JournalScreen(MDScreen):
    """Screen for daily journal entries"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
        )

        # Header with back button
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            spacing=10,
        )

        back_btn = MDButton(
            style="text",
            on_release=lambda x: self.go_back(),
        )
        back_btn.add_widget(MDButtonText(text="< Back"))
        header.add_widget(back_btn)

        title = MDLabel(
            text="Today's Journal",
            halign="center",
            font_style="Headline",
        )
        header.add_widget(title)

        layout.add_widget(header)

        # Date label
        self.date_label = MDLabel(
            text="Date: --",
            halign="center",
            size_hint_y=None,
            height=30,
        )
        layout.add_widget(self.date_label)

        # Journal text area
        self.journal_field = MDTextField(
            mode="outlined",
            multiline=True,
            size_hint=(1, 0.6),
        )
        self.journal_field.hint_text = "Write about your day..."
        layout.add_widget(self.journal_field)

        # Save button
        save_btn = MDButton(
            style="filled",
            pos_hint={"center_x": 0.5},
            on_release=self.save_entry,
        )
        save_btn.add_widget(MDButtonText(text="Save Entry"))
        layout.add_widget(save_btn)

        self.add_widget(layout)

    def go_back(self):
        """Return to home screen"""
        self.manager.current = "home"

    def save_entry(self, *args):
        """Save journal entry"""
        # TODO: Call api_client.create_journal_entry()
        pass

    def load_entry(self, date):
        """Load journal entry for date"""
        # TODO: Call api_client.get_journal_by_date()
        pass
