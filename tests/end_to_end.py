"""
End-to-end tests for key user flows.

These tests mock the API layer but exercise the full screen logic:
load → interact → save, verifying the correct API calls are made
with the correct arguments (e.g. the right endpoint and entry id).
"""

import datetime
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Journal flows
# ---------------------------------------------------------------------------


class TestJournalE2E:
    """End-to-end flows for the journal screen."""

    def test_load_existing_entry_then_edit_and_save(self, screen_manager):
        """
        Load an existing entry, edit it, save — must PATCH by id.

        Covers the bug where GET /journal/{date}/ and PATCH /journal/{date}/
        both returned 404. The correct endpoints are:
          - GET  /journal/by-date/{date}/
          - PATCH /journal/{id}/
        """
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        # Step 1: load_entry calls get_journal_by_date (by-date endpoint)
        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.load_entry(datetime.date(2026, 3, 6))
        load_target = mock_thread.call_args[1]["target"]

        with patch("screens.journal.api_client") as mock_api:
            mock_api.get_journal_by_date.return_value = {
                "id": 158,
                "date": "2026-03-06",
                "content": "Today was a great day!",
            }
            load_target()
            mock_api.get_journal_by_date.assert_called_once_with("2026-03-06")

        # Clock callback delivers text and id to the screen
        screen._set_entry_text("Today was a great day!", entry_id=158)

        assert screen.journal_field.text == "Today was a great day!"
        assert screen._entry_id == 158

        # Step 2: user edits the entry
        screen.journal_field.text = "Today was a great day! (edited)"

        # Step 3: save must call PATCH by id, not POST
        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.save_entry()
        save_target = mock_thread.call_args[1]["target"]

        with patch("screens.journal.api_client") as mock_api:
            mock_api.update_journal_entry.return_value = {
                "id": 158,
                "content": "Today was a great day! (edited)",
            }
            with patch("screens.journal.Clock"):
                save_target()

        mock_api.update_journal_entry.assert_called_once_with(158, "Today was a great day! (edited)")
        mock_api.create_journal_entry.assert_not_called()

    def test_new_entry_create_then_edit_and_save(self, screen_manager):
        """
        No existing entry → create it → edit → save again uses PATCH with
        the id returned from the original POST.
        """
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        # Step 1: load finds no entry for today
        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.load_entry(datetime.date(2026, 3, 6))
        load_target = mock_thread.call_args[1]["target"]

        with patch("screens.journal.api_client") as mock_api:
            mock_api.get_journal_by_date.return_value = None
            load_target()

        screen._set_entry_text("", entry_id=None)

        assert screen.journal_field.text == ""
        assert screen._entry_id is None

        # Step 2: user types a new entry
        screen.journal_field.text = "My first entry"

        # Step 3: first save → POST create, backend returns id=99
        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.save_entry()
        save_target = mock_thread.call_args[1]["target"]

        with patch("screens.journal.api_client") as mock_api:
            mock_api.create_journal_entry.return_value = {"id": 99, "content": "My first entry"}
            with patch("screens.journal.Clock"):
                save_target()

        mock_api.create_journal_entry.assert_called_once()
        mock_api.update_journal_entry.assert_not_called()

        # Success callback stores the new id
        screen._on_save_success("My first entry", entry_id=99)
        assert screen._entry_id == 99

        # Step 4: user edits and saves again → must PATCH with id=99
        screen.journal_field.text = "My first entry (updated)"

        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.save_entry()
        save_target2 = mock_thread.call_args[1]["target"]

        with patch("screens.journal.api_client") as mock_api:
            mock_api.update_journal_entry.return_value = {"id": 99, "content": "My first entry (updated)"}
            with patch("screens.journal.Clock"):
                save_target2()

        mock_api.update_journal_entry.assert_called_once_with(99, "My first entry (updated)")
        mock_api.create_journal_entry.assert_not_called()

    def test_navigate_to_past_day_loads_that_entry(self, screen_manager):
        """
        Navigate to a past day → load_entry is called for that date,
        text and entry_id are updated.
        """
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        with patch("screens.journal.threading.Thread") as mock_thread:
            screen._do_navigate_date(-1)
        load_target = mock_thread.call_args[1]["target"]

        past_date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

        with patch("screens.journal.api_client") as mock_api:
            mock_api.get_journal_by_date.return_value = {
                "id": 55,
                "date": past_date,
                "content": "Yesterday's thoughts",
            }
            load_target()
            mock_api.get_journal_by_date.assert_called_once_with(past_date)

        screen._set_entry_text("Yesterday's thoughts", entry_id=55)

        assert screen.journal_field.text == "Yesterday's thoughts"
        assert screen._entry_id == 55


# ---------------------------------------------------------------------------
# Goals flows
# ---------------------------------------------------------------------------


class TestGoalsE2E:
    """End-to-end flows for the goals screen."""

    def test_load_goals_populates_cards_with_ids(self, screen_manager):
        """
        On enter, goals are fetched and a card is created for each,
        storing the backend id for later operations.
        """
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.load_goals()
        load_target = mock_thread.call_args[1]["target"]

        with patch("screens.goals.api_client") as mock_api:
            mock_api.get_goals.return_value = [
                {"id": 1, "goal_text": "Run 5km", "completed": False},
                {"id": 2, "goal_text": "Read a book", "completed": True},
            ]
            with patch("screens.goals.Clock") as mock_clock:
                load_target()
                cb = mock_clock.schedule_once.call_args[0][0]
                cb(0)

        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert len(cards) == 2
        goal_ids = {c.goal_id for c in cards}
        assert goal_ids == {1, 2}

    def test_add_goal_creates_via_api_and_stores_id(self, screen_manager):
        """
        Confirming the add-goal dialog calls create_goal and the resulting
        card has the id returned by the backend.
        """
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)
        screen.new_goal_field = MagicMock()
        screen.new_goal_field.text = "Exercise daily"
        screen._dialog = MagicMock()

        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.confirm_add_goal()
        add_target = mock_thread.call_args[1]["target"]

        with patch("screens.goals.api_client") as mock_api:
            mock_api.create_goal.return_value = {"id": 10, "goal_text": "Exercise daily"}
            with patch("screens.goals.Clock") as mock_clock:
                add_target()
                cb = mock_clock.schedule_once.call_args[0][0]
                cb(0)

        mock_api.create_goal.assert_called_once_with("Exercise daily")
        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert any(c.goal_id == 10 for c in cards)

    def test_toggle_goal_calls_update_with_correct_id(self, screen_manager):
        """
        Checking a goal's checkbox calls update_goal with the goal's backend id
        and the new completed state.
        """
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)
        screen._populate_goals([{"id": 7, "goal_text": "Meditate", "completed": False}])

        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        card = cards[0]
        assert card.goal_id == 7

        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.toggle_goal(card, completed=True)
        toggle_target = mock_thread.call_args[1]["target"]

        with patch("screens.goals.api_client") as mock_api:
            toggle_target()
            mock_api.update_goal.assert_called_once_with(7, completed=True)

    def test_delete_goal_calls_api_and_removes_card(self, screen_manager):
        """
        Tapping delete calls delete_goal with the backend id and removes
        the card from the list.
        """
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)
        screen._populate_goals([{"id": 3, "goal_text": "Write journal", "completed": False}])

        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        card = cards[0]

        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.delete_goal(card)
        delete_target = mock_thread.call_args[1]["target"]

        with patch("screens.goals.api_client") as mock_api:
            with patch("screens.goals.Clock") as mock_clock:
                delete_target()
                mock_api.delete_goal.assert_called_once_with(3)
                cb = mock_clock.schedule_once.call_args[0][0]
                cb(0)

        remaining = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert len(remaining) == 0

    def test_full_flow_add_toggle_delete(self, screen_manager):
        """
        Full cycle: load goals → add one → toggle it complete → delete it.
        Verifies the correct id is used at every step.
        """
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        # Step 1: load — empty list
        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.load_goals()
        with patch("screens.goals.api_client") as mock_api:
            mock_api.get_goals.return_value = []
            with patch("screens.goals.Clock") as mock_clock:
                mock_thread.call_args[1]["target"]()
                mock_clock.schedule_once.call_args[0][0](0)

        assert len([w for w in screen.goals_list.children if isinstance(w, GoalCard)]) == 0

        # Step 2: add a goal — backend returns id=42
        screen.new_goal_field = MagicMock()
        screen.new_goal_field.text = "Sleep 8 hours"
        screen._dialog = MagicMock()

        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.confirm_add_goal()
        with patch("screens.goals.api_client") as mock_api:
            mock_api.create_goal.return_value = {"id": 42, "goal_text": "Sleep 8 hours"}
            with patch("screens.goals.Clock") as mock_clock:
                mock_thread.call_args[1]["target"]()
                mock_clock.schedule_once.call_args[0][0](0)

        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert len(cards) == 1
        card = cards[0]
        assert card.goal_id == 42

        # Step 3: toggle complete — must use id=42
        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.toggle_goal(card, completed=True)
        with patch("screens.goals.api_client") as mock_api:
            mock_thread.call_args[1]["target"]()
            mock_api.update_goal.assert_called_once_with(42, completed=True)

        # Step 4: delete — must use id=42 and remove the card
        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.delete_goal(card)
        with patch("screens.goals.api_client") as mock_api:
            with patch("screens.goals.Clock") as mock_clock:
                mock_thread.call_args[1]["target"]()
                mock_api.delete_goal.assert_called_once_with(42)
                mock_clock.schedule_once.call_args[0][0](0)

        assert len([w for w in screen.goals_list.children if isinstance(w, GoalCard)]) == 0
