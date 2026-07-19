"""Goals Screen - Issue #5/#6: Weekly Goals Screen UI + API Integration"""

import threading
from datetime import date, timedelta

from kivy.clock import Clock
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

from services.api_client import api_client
from utils.debounce import debounce
from utils.week import monday_of, week_range_text


BLUE = (0.129, 0.588, 0.953, 1)
WHITE = (1, 1, 1, 1)
WHITE_DIM = (1, 1, 1, 0.85)
BG = (0.96, 0.96, 0.96, 1)


class GoalCard(MDCard):
    """Card representing a single goal with checkbox and delete button"""

    def __init__(self, goal_text: str, goal_id, on_delete, on_toggle, on_edit=None, completed: bool = False, **kwargs):
        """Build the card with checkbox, label, edit button, and delete button.

        Args:
            goal_text: Text to display for the goal.
            goal_id: Backend ID used for API calls, or None for local-only cards.
            on_delete: Callback(card) invoked when the trash button is tapped.
            on_toggle: Callback(card, completed) invoked when the checkbox changes.
            on_edit: Callback(card) invoked when the pencil button is tapped.
            completed: Initial checked state.
        """
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
        self.goal_id = goal_id
        self.goal_text = goal_text
        self._on_delete = on_delete
        self._on_toggle = on_toggle
        self._on_edit = on_edit

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

        self.edit_btn = MDIconButton(
            icon="pencil-outline",
            theme_icon_color="Custom",
            icon_color=BLUE,
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_y": 0.5},
            on_release=self._handle_edit,
        )
        self.add_widget(self.edit_btn)

        self.delete_btn = MDIconButton(
            icon="trash-can-outline",
            theme_icon_color="Custom",
            icon_color=(0.7, 0.2, 0.2, 1),
            size_hint=(None, None),
            size=(40, 40),
            pos_hint={"center_y": 0.5},
            on_release=self._handle_delete,
        )
        self.add_widget(self.delete_btn)

    @debounce()
    def _handle_delete(self, *args):
        """Invoke the delete callback, debounced against Android's double on_release."""
        self._on_delete(self)

    @debounce()
    def _handle_edit(self, *args):
        """Invoke the edit callback, debounced against Android's double on_release."""
        if self._on_edit:
            self._on_edit(self)

    def set_text(self, text: str):
        """Update the goal's displayed text and stored value."""
        self.goal_text = text
        self.goal_label.text = text

    def on_touch_down(self, touch):
        """Toggle checkbox when the card body is tapped (excluding action buttons)."""
        if (
            self.collide_point(*touch.pos)
            and not self.delete_btn.collide_point(*touch.pos)
            and not self.edit_btn.collide_point(*touch.pos)
        ):
            self.checkbox.active = not self.checkbox.active
            return True
        return super().on_touch_down(touch)

    def on_checkbox_change(self, instance, value):
        """Update label style and notify the screen when the checkbox state changes."""
        self.goal_label.theme_text_color = "Secondary" if value else "Primary"
        self._on_toggle(self, value)


class GoalsScreen(MDScreen):
    """Screen for managing weekly goals"""

    def __init__(self, **kwargs):
        """Initialise state and build the UI."""
        super().__init__(**kwargs)
        self._dialog = None
        self._current_week_start = monday_of(date.today())
        self._editing_card = None
        self.build_ui()

    def build_ui(self):
        """Construct the full screen layout (header, content, footer)."""
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
            text="Your weekly targets",
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
            on_release=self._week_prev,
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
            on_release=self._week_next,
        )
        week_row.add_widget(self._prev_btn)
        week_row.add_widget(self.week_label)
        week_row.add_widget(self._next_btn)
        root.add_widget(week_row)

        # --- Content ---
        content_bg = MDBoxLayout(orientation="vertical", md_bg_color=BG)

        self.status_label = MDLabel(
            text="",
            halign="center",
            font_style="Body",
            role="medium",
            theme_text_color="Error",
            adaptive_height=True,
            size_hint=(1, None),
            padding=[16, 8, 16, 0],
        )
        content_bg.add_widget(self.status_label)

        scroll = MDScrollView()

        self.goals_list = MDBoxLayout(
            orientation="vertical",
            padding=[16, 16, 16, 16],
            spacing=12,
            adaptive_height=True,
        )

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

    def on_pre_enter(self):
        """Reset to the current week and reload its goals each time the screen is shown.

        Resetting avoids silently adding goals to a past/future week the user had
        navigated to on a previous visit, and keeps "current week" correct if the
        app has been open across a week boundary.
        """
        self._current_week_start = monday_of(date.today())
        self.week_label.text = self._week_text()
        self.load_goals()

    def load_goals(self):
        """Fetch goals for the selected week from the API and populate the list."""
        self.status_label.text = "Loading..."
        self._set_nav_enabled(False)
        week_start_str = self._current_week_start.isoformat()

        def _do():
            try:
                goals = api_client.get_goals(week_start_str)
                Clock.schedule_once(
                    lambda dt: self._populate_goals(goals, week_start_str)
                )
            except Exception as e:
                msg = str(e)
                Clock.schedule_once(lambda dt: self.show_error(msg))

        threading.Thread(target=_do, daemon=True).start()

    def _week_text(self) -> str:
        """Human-readable range for the selected week (e.g. 'Jul 14 – Jul 20, 2026')."""
        return week_range_text(self._current_week_start)

    def _set_nav_enabled(self, enabled: bool):
        """Enable/disable the week arrows (disabled while a week is loading).

        Serialising loads this way prevents overlapping fetches whose responses
        could arrive out of order and render the wrong week's goals.
        """
        self._prev_btn.disabled = not enabled
        self._next_btn.disabled = not enabled

    @debounce()
    def _week_prev(self, *args):
        """Go to the previous week. Debounced per-direction (see _week_next)."""
        self._change_week(-1)

    @debounce()
    def _week_next(self, *args):
        """Go to the next week.

        Prev/next are separate debounced methods so a quick ◀ then ▶ isn't
        collapsed into one — only genuine same-button double-fires are.
        """
        self._change_week(1)

    def _change_week(self, delta: int):
        """Move the selected week by ``delta`` weeks and reload its goals."""
        self._current_week_start += timedelta(weeks=delta)
        self.week_label.text = self._week_text()
        self.load_goals()

    def _populate_goals(self, goals, week_start_str=None):
        """Clear existing cards and render goals from API data.

        ``week_start_str`` is the week the fetch was issued for; if the user has
        since navigated to a different week, this (now stale) response is dropped.
        """
        if (
            week_start_str is not None
            and week_start_str != self._current_week_start.isoformat()
        ):
            return
        self._set_nav_enabled(True)
        for card in self._goal_cards():
            self.goals_list.remove_widget(card)
        self.status_label.text = ""
        for goal in goals:
            self._add_goal_card(
                goal_text=goal.get("goal_text", ""),
                goal_id=goal.get("id"),
                completed=goal.get("completed", False),
                refresh=False,
            )
        # Refresh once for the whole batch rather than per card.
        self._refresh_empty_state()

    def _add_goal_card(
        self, goal_text: str, goal_id=None, completed: bool = False, refresh: bool = True
    ):
        """Create a GoalCard and append it to the list.

        ``refresh`` lets bulk callers skip the per-card empty-state refresh and
        do it once at the end.
        """
        card = GoalCard(
            goal_text=goal_text,
            goal_id=goal_id,
            on_delete=self.delete_goal,
            on_toggle=self.toggle_goal,
            on_edit=self.show_edit_dialog,
            completed=completed,
        )
        self.goals_list.add_widget(card)
        if refresh:
            self._refresh_empty_state()

    def _goal_cards(self):
        """The GoalCard widgets currently in the list."""
        return [w for w in self.goals_list.children if isinstance(w, GoalCard)]

    def _refresh_empty_state(self):
        """Show empty label only when there are no goal cards."""
        self.empty_label.opacity = 0 if self._goal_cards() else 1

    def toggle_goal(self, card: "GoalCard", completed: bool):
        """Persist completed state to the API."""
        if card.goal_id is None:
            return

        def _do():
            try:
                api_client.update_goal(card.goal_id, completed=completed)
            except Exception as e:
                msg = str(e)
                Clock.schedule_once(lambda dt: self.show_error(msg))

        threading.Thread(target=_do, daemon=True).start()

    def delete_goal(self, card: "GoalCard"):
        """Delete goal from API then remove card, or remove locally if no ID."""
        if card.goal_id is None:
            self._remove_card(card)
            return

        def _do():
            try:
                api_client.delete_goal(card.goal_id)
                Clock.schedule_once(lambda dt: self._remove_card(card))
            except Exception as e:
                msg = str(e)
                Clock.schedule_once(lambda dt: self.show_error(msg))

        threading.Thread(target=_do, daemon=True).start()

    def _remove_card(self, card: "GoalCard"):
        """Remove a card from the list and update the empty state."""
        self.goals_list.remove_widget(card)
        self._refresh_empty_state()

    def show_error(self, message: str):
        """Display an error message in the status label and re-enable navigation."""
        self.status_label.text = message
        self._set_nav_enabled(True)

    def _open_goal_dialog(self, headline: str, initial: str, confirm_label: str, confirm_callback):
        """Open a goal text dialog shared by the add and edit flows."""
        self._goal_field = MDTextField(
            mode="outlined",
            hint_text="Describe your goal...",
            text=initial,
            size_hint_x=1,
        )

        cancel_btn = MDButton(style="text", on_release=self.close_dialog)
        cancel_btn.add_widget(MDButtonText(text="Cancel"))

        confirm_btn = MDButton(style="text", on_release=confirm_callback)
        confirm_btn.add_widget(MDButtonText(text=confirm_label))

        self._dialog = MDDialog(
            MDDialogHeadlineText(text=headline),
            MDDialogContentContainer(
                self._goal_field,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                cancel_btn,
                confirm_btn,
            ),
        )
        self._dialog.open()
        Clock.schedule_once(lambda dt: setattr(self._goal_field, "focus", True), 0.1)

    @debounce()
    def show_add_dialog(self):
        """Open the dialog for entering a new goal."""
        self._editing_card = None
        self._open_goal_dialog("New Goal", "", "Add", self.confirm_add_goal)

    @debounce()
    def show_edit_dialog(self, card: "GoalCard"):
        """Open the dialog for editing an existing goal's text."""
        self._editing_card = card
        self._open_goal_dialog("Edit Goal", card.goal_text, "Save", self.confirm_edit_goal)

    def close_dialog(self, *args):
        """Dismiss the active dialog and clear the reference."""
        if self._dialog:
            self._dialog.dismiss()
            self._dialog = None

    @debounce()
    def confirm_add_goal(self, *args):
        """Read the dialog input, close it, and create the goal for the selected week."""
        text = self._goal_field.text.strip()
        self.close_dialog()
        if not text:
            return
        week_start_str = self._current_week_start.isoformat()

        def _do():
            try:
                result = api_client.create_goal(text, week_start_date=week_start_str)
                goal_id = result.get("id")
                Clock.schedule_once(lambda dt: self._add_goal_card(text, goal_id=goal_id))
            except Exception as e:
                msg = str(e)
                Clock.schedule_once(lambda dt: self.show_error(msg))

        threading.Thread(target=_do, daemon=True).start()

    @debounce()
    def confirm_edit_goal(self, *args):
        """Read the dialog input, close it, and persist the goal's new text."""
        card = self._editing_card
        text = self._goal_field.text.strip()
        self.close_dialog()
        if card is None or not text or text == card.goal_text:
            return

        # Local-only card (not yet persisted): just update its text.
        if card.goal_id is None:
            card.set_text(text)
            return

        def _do():
            try:
                api_client.update_goal(card.goal_id, goal_text=text)
                Clock.schedule_once(lambda dt: card.set_text(text))
            except Exception as e:
                msg = str(e)
                Clock.schedule_once(lambda dt: self.show_error(msg))

        threading.Thread(target=_do, daemon=True).start()

    @debounce()
    def go_back(self):
        """Navigate back to the home screen."""
        self.manager.current = "home"
