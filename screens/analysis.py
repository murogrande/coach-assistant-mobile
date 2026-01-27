"""Analysis Screen"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard


class AnalysisScreen(MDScreen):
    """Screen for viewing weekly AI analysis"""

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
            text="Weekly Analysis",
            halign="center",
            font_style="Headline",
        )
        header.add_widget(title)

        layout.add_widget(header)

        # Analysis card
        self.analysis_card = MDCard(
            style="elevated",
            padding=20,
            size_hint=(1, 0.6),
        )

        self.analysis_text = MDLabel(
            text="No analysis available yet.\n\nGenerate your weekly analysis to get AI-powered insights about your goals and journal entries.",
            halign="left",
        )
        self.analysis_card.add_widget(self.analysis_text)
        layout.add_widget(self.analysis_card)

        # Generate button
        generate_btn = MDButton(
            style="filled",
            pos_hint={"center_x": 0.5},
            on_release=self.generate_analysis,
        )
        generate_btn.add_widget(MDButtonText(text="Generate Analysis"))
        layout.add_widget(generate_btn)

        self.add_widget(layout)

    def go_back(self):
        """Return to home screen"""
        self.manager.current = "home"

    def generate_analysis(self, *args):
        """Request new analysis from API"""
        # TODO: Call api_client.generate_analysis()
        pass

    def load_latest(self):
        """Load latest analysis"""
        # TODO: Call api_client.get_latest_analysis()
        pass
