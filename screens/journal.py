"""Journal Screen"""

import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField


BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)


class JournalScreen(MDScreen):
    """Screen for daily journal entries"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        root = MDBoxLayout(orientation="vertical")

        today = datetime.date.today()
        date_str = today.strftime("%A, %B %d")

        # --- Header ---
        header = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=130,
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
        self.date_label = MDLabel(
            text=date_str,
            font_style="Body",
            role="medium",
            theme_text_color="Custom",
            text_color=WHITE_DIM,
            adaptive_height=True,
        )
        header.add_widget(self.date_label)
        root.add_widget(header)

        # --- Content ---
        content = MDBoxLayout(
            orientation="vertical",
            padding=[16, 16, 16, 0],
            spacing=12,
            md_bg_color=BG,
        )

        prompt_label = MDLabel(
            text="How was your day?",
            font_style="Title",
            role="small",
            adaptive_height=True,
        )
        content.add_widget(prompt_label)

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
            height=80,
            padding=[16, 12, 16, 12],
            md_bg_color=BG,
        )
        self.save_btn = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.save_entry,
        )
        self.save_btn.add_widget(MDButtonText(text="Save Entry"))
        footer.add_widget(self.save_btn)
        root.add_widget(footer)

        self.add_widget(root)

    def go_back(self):
        self.manager.current = "home"

    def save_entry(self, *args):
        # TODO: Call api_client.create_journal_entry() (Issue #8)
        pass

    def load_entry(self, date):
        # TODO: Call api_client.get_journal_by_date() (Issue #8)
        pass
