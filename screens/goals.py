"""Goals Screen"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText


class GoalsScreen(MDScreen):
    """Screen for managing weekly goals"""

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
            text="Weekly Goals",
            halign="center",
            font_style="Headline",
        )
        header.add_widget(title)

        layout.add_widget(header)

        # Goals list placeholder
        self.goals_list = MDList()

        # Placeholder items
        for i in range(3):
            item = MDListItem()
            item.add_widget(MDListItemHeadlineText(text=f"Goal {i + 1} - Tap to edit"))
            self.goals_list.add_widget(item)

        layout.add_widget(self.goals_list)

        # Add goal button
        add_btn = MDButton(
            style="filled",
            pos_hint={"center_x": 0.5},
            on_release=self.add_goal,
        )
        add_btn.add_widget(MDButtonText(text="Add Goal"))
        layout.add_widget(add_btn)

        self.add_widget(layout)

    def go_back(self):
        """Return to home screen"""
        self.manager.current = "home"

    def add_goal(self, *args):
        """Add a new goal"""
        # TODO: Implement add goal dialog
        pass

    def load_goals(self):
        """Load goals from API"""
        # TODO: Call api_client.get_goals()
        pass
