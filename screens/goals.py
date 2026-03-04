"""Goals Screen"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox


BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)

# Placeholder goals until API is connected (Issue #6)
_PLACEHOLDER_GOALS = [
    "Exercise for 30 minutes every day",
    "Read 20 pages of a book",
    "Drink 8 glasses of water",
]


class GoalCard(MDCard):
    """Card representing a single goal with a checkbox"""

    def __init__(self, goal_text: str, completed: bool = False, **kwargs):
        super().__init__(
            orientation="horizontal",
            padding=[16, 14, 16, 14],
            spacing=12,
            size_hint=(1, None),
            height=72,
            elevation=1,
            style="elevated",
            **kwargs,
        )
        self.completed = completed

        self.checkbox = MDCheckbox(
            size_hint=(None, None),
            size=(36, 36),
            pos_hint={"center_y": 0.5},
            active=completed,
        )
        self.checkbox.bind(active=self.on_checkbox_change)
        self.add_widget(self.checkbox)

        self.goal_label = MDLabel(
            text=goal_text,
            font_style="Body",
            role="large",
            theme_text_color="Secondary" if completed else "Primary",
            adaptive_height=True,
            pos_hint={"center_y": 0.5},
        )
        self.add_widget(self.goal_label)

    def on_checkbox_change(self, instance, value):
        self.goal_label.theme_text_color = "Secondary" if value else "Primary"


class GoalsScreen(MDScreen):
    """Screen for managing weekly goals"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
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
        top_row = MDBoxLayout(
            orientation="horizontal",
            adaptive_height=True,
            spacing=4,
        )
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda x: self.go_back(),
        )
        top_row.add_widget(back_btn)
        top_row.add_widget(MDLabel(
            text="My Goals",
            font_style="Headline",
            role="small",
            theme_text_color="Custom",
            text_color=WHITE,
            adaptive_height=True,
            pos_hint={"center_y": 0.5},
        ))
        header.add_widget(top_row)
        header.add_widget(MDLabel(
            text="This week's targets",
            font_style="Body",
            role="medium",
            theme_text_color="Custom",
            text_color=WHITE_DIM,
            adaptive_height=True,
        ))
        root.add_widget(header)

        # --- Content ---
        content_bg = MDBoxLayout(orientation="vertical", md_bg_color=BG)

        scroll = MDScrollView()
        self.goals_list = MDBoxLayout(
            orientation="vertical",
            padding=[16, 16, 16, 16],
            spacing=12,
            adaptive_height=True,
        )
        for goal_text in _PLACEHOLDER_GOALS:
            self.goals_list.add_widget(GoalCard(goal_text=goal_text))

        scroll.add_widget(self.goals_list)
        content_bg.add_widget(scroll)

        # --- Footer ---
        footer = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=80,
            padding=[16, 12, 16, 12],
            md_bg_color=BG,
        )
        add_btn = MDButton(
            style="filled",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.add_goal,
        )
        add_btn.add_widget(MDButtonText(text="Add Goal"))
        footer.add_widget(add_btn)

        root.add_widget(content_bg)
        root.add_widget(footer)
        self.add_widget(root)

    def go_back(self):
        self.manager.current = "home"

    def add_goal(self, *args):
        # TODO: Implement add goal dialog (Issue #6)
        pass

    def load_goals(self):
        # TODO: Call api_client.get_goals() (Issue #6)
        pass
