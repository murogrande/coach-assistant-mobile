"""Goals Screen - Issue #5: Weekly Goals Screen UI"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.textfield import MDTextField


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
    """Card representing a single goal with checkbox and delete button"""

    def __init__(self, goal_text: str, on_delete, completed: bool = False, **kwargs):
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
        self._on_delete = on_delete

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

        self.delete_btn = MDIconButton(
            icon="trash-can-outline",
            theme_icon_color="Custom",
            icon_color=(0.7, 0.2, 0.2, 1),
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_y": 0.5},
            on_release=lambda x: self._on_delete(self),
        )
        self.add_widget(self.delete_btn)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.delete_btn.collide_point(*touch.pos):
            self.checkbox.active = not self.checkbox.active
            return True
        return super().on_touch_down(touch)

    def on_checkbox_change(self, instance, value):
        self.goal_label.theme_text_color = "Secondary" if value else "Primary"


class GoalsScreen(MDScreen):
    """Screen for managing weekly goals"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dialog = None
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
        top_row = MDBoxLayout(orientation="horizontal", adaptive_height=True, spacing=4)
        top_row.add_widget(MDIconButton(
            icon="arrow-left",
            theme_icon_color="Custom",
            icon_color=WHITE,
            on_release=lambda x: self.go_back(),
        ))
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

        # Empty state label (hidden when goals exist)
        self.empty_label = MDLabel(
            text="No goals yet.\nTap 'Add Goal' to get started!",
            halign="center",
            font_style="Body",
            role="large",
            theme_text_color="Secondary",
            adaptive_height=True,
            size_hint=(1, None),
        )
        self.goals_list.add_widget(self.empty_label)

        for goal_text in _PLACEHOLDER_GOALS:
            self._add_goal_card(goal_text)

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
            on_release=lambda x: self.show_add_dialog(),
        )
        add_btn.add_widget(MDButtonText(text="Add Goal"))
        footer.add_widget(add_btn)

        root.add_widget(content_bg)
        root.add_widget(footer)
        self.add_widget(root)
        self._refresh_empty_state()

    def _add_goal_card(self, goal_text: str, completed: bool = False):
        card = GoalCard(
            goal_text=goal_text,
            on_delete=self.delete_goal,
            completed=completed,
        )
        self.goals_list.add_widget(card)
        self._refresh_empty_state()

    def _refresh_empty_state(self):
        """Show empty label only when there are no goal cards"""
        goal_cards = [w for w in self.goals_list.children if isinstance(w, GoalCard)]
        self.empty_label.opacity = 0 if goal_cards else 1

    def delete_goal(self, card: GoalCard):
        self.goals_list.remove_widget(card)
        self._refresh_empty_state()

    def show_add_dialog(self):
        self.new_goal_field = MDTextField(
            mode="outlined",
            hint_text="Describe your goal...",
            size_hint_x=1,
        )

        cancel_btn = MDButton(style="text", on_release=self.close_dialog)
        cancel_btn.add_widget(MDButtonText(text="Cancel"))

        add_btn = MDButton(style="text", on_release=self.confirm_add_goal)
        add_btn.add_widget(MDButtonText(text="Add"))

        self._dialog = MDDialog(
            MDDialogHeadlineText(text="New Goal"),
            MDDialogContentContainer(
                self.new_goal_field,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                cancel_btn,
                add_btn,
            ),
        )
        self._dialog.open()

    def close_dialog(self, *args):
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None

    def confirm_add_goal(self, *args):
        text = self.new_goal_field.text.strip()
        if text:
            self._add_goal_card(text)
        self.close_dialog()

    def go_back(self):
        self.manager.current = "home"

    def load_goals(self):
        # TODO: Call api_client.get_goals() (Issue #6)
        pass
