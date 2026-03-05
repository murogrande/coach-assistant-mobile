"""Analysis Screen"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.icon_definitions import md_icons


BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)

_PLACEHOLDER_TEXT = (
    "No analysis available yet.\n\n"
    "Once you have logged your goals and journal entries for the week, "
    "tap 'Generate Analysis' to receive AI-powered insights about your "
    "progress, patterns, and personalised recommendations."
)


class AnalysisScreen(MDScreen):
    """Screen for viewing weekly AI analysis"""

    def __init__(self, **kwargs):
        """Initialise and build the analysis screen UI."""
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """Construct the full screen layout (header, scrollable content, generate footer)."""
        root = MDBoxLayout(orientation="vertical")

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

        # --- Content ---
        content = MDBoxLayout(
            orientation="vertical",
            padding=[16, 16, 16, 0],
            spacing=12,
            md_bg_color=BG,
        )

        scroll = MDScrollView()
        card = MDCard(
            orientation="vertical",
            padding=[20, 20, 20, 20],
            style="elevated",
            elevation=1,
            adaptive_height=True,
        )
        self.analysis_text = MDLabel(
            text=_PLACEHOLDER_TEXT,
            font_style="Body",
            role="large",
            halign="left",
            adaptive_height=True,
        )
        card.add_widget(self.analysis_text)
        scroll.add_widget(card)
        content.add_widget(scroll)

        root.add_widget(content)

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

    def go_back(self):
        """Navigate back to the home screen."""
        self.manager.current = "home"

    def generate_analysis(self, *args):
        """Request a new weekly analysis from the API (Issue #10)."""
        # TODO: Call api_client.generate_analysis() (Issue #10)
        pass

    def load_latest(self):
        """Load the most recent analysis from the API (Issue #10)."""
        # TODO: Call api_client.get_latest_analysis() (Issue #10)
        pass
