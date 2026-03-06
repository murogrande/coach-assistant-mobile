"""Tests for screen modules"""

from unittest.mock import patch, MagicMock


class TestLoginScreen:
    """Tests for LoginScreen"""

    def test_login_screen_creation(self, screen_manager):
        """Test LoginScreen can be instantiated"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        assert screen.name == "login"
        assert screen_manager.current == "login"

    def test_login_screen_has_username_field(self, screen_manager):
        """Test LoginScreen has username input field"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "username_field")
        assert screen.username_field is not None

    def test_login_screen_has_password_field(self, screen_manager):
        """Test LoginScreen has password input field"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "password_field")
        assert screen.password_field is not None
        assert screen.password_field.password is True

    def test_login_screen_has_error_label(self, screen_manager):
        """Test LoginScreen has an error label"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "error_label")
        assert screen.error_label.text == ""

    def test_show_error_displays_message(self, screen_manager):
        """Test show_error sets error label text"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        screen.show_error("Invalid credentials")
        assert screen.error_label.text == "Invalid credentials"

    def test_clear_error_resets_message(self, screen_manager):
        """Test clear_error resets error label"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        screen.show_error("Some error")
        screen.clear_error()
        assert screen.error_label.text == ""

    def test_validate_empty_username(self, screen_manager):
        """Test validation fails with empty username"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        screen.username_field.text = ""
        screen.password_field.text = "password123"
        result = screen.validate()

        assert result is False
        assert "Username" in screen.error_label.text

    def test_validate_empty_password(self, screen_manager):
        """Test validation fails with empty password"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        screen.username_field.text = "testuser"
        screen.password_field.text = ""
        result = screen.validate()

        assert result is False
        assert "Password" in screen.error_label.text

    def test_validate_short_password(self, screen_manager):
        """Test validation fails with password under 6 characters"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        screen.username_field.text = "testuser"
        screen.password_field.text = "abc"
        result = screen.validate()

        assert result is False
        assert "6 characters" in screen.error_label.text

    def test_validate_success(self, screen_manager):
        """Test validation passes with valid inputs"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        screen.username_field.text = "testuser"
        screen.password_field.text = "password123"
        result = screen.validate()

        assert result is True

    def test_toggle_mode_switches_to_register(self, screen_manager):
        """Test toggle_mode switches to register mode"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        assert screen.is_register_mode is False
        screen.toggle_mode()
        assert screen.is_register_mode is True
        assert screen.form_title.text == "Create Account"

    def test_toggle_mode_switches_back_to_login(self, screen_manager):
        """Test toggle_mode switches back to login mode"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        screen.toggle_mode()
        screen.toggle_mode()
        assert screen.is_register_mode is False
        assert screen.form_title.text == "Sign In"

    def test_do_login_calls_api_and_navigates(self, screen_manager):
        """Test do_login calls api_client.login and navigates to home on success"""
        from screens.login import LoginScreen
        from screens.home import HomeScreen

        login = LoginScreen(name="login")
        home = HomeScreen(name="home")
        screen_manager.add_widget(login)
        screen_manager.add_widget(home)

        login.username_field.text = "testuser"
        login.password_field.text = "password123"

        with patch("screens.login.api_client"), \
             patch("screens.login.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            login.do_login()
            mock_thread.assert_called_once()
            assert login.action_btn.disabled is True

    def test_do_login_shows_error_on_failure(self, screen_manager):
        """Test _on_auth_error re-enables button and shows message"""
        from screens.login import LoginScreen

        login = LoginScreen(name="login")
        screen_manager.add_widget(login)

        login._on_auth_error("Invalid credentials")

        assert login.action_btn.disabled is False
        assert login.error_label.text == "Invalid credentials"

    def test_on_auth_success_navigates_to_home(self, screen_manager):
        """Test _on_auth_success navigates to home screen"""
        from screens.login import LoginScreen
        from screens.home import HomeScreen

        login = LoginScreen(name="login")
        home = HomeScreen(name="home")
        screen_manager.add_widget(login)
        screen_manager.add_widget(home)

        login._on_auth_success()

        assert screen_manager.current == "home"
        assert login.action_btn.disabled is False

    def test_parse_error_http_error_with_detail(self, screen_manager):
        """Test _parse_error extracts detail from HTTPError response"""
        import requests
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        mock_response = MagicMock()
        mock_response.json.return_value = {"detail": "No active account found."}
        mock_response.status_code = 401
        err = requests.HTTPError(response=mock_response)

        msg = screen._parse_error(err)
        assert msg == "No active account found."

    def test_parse_error_generic_exception(self, screen_manager):
        """Test _parse_error returns str for generic exceptions"""
        from screens.login import LoginScreen

        screen = LoginScreen(name="login")
        screen_manager.add_widget(screen)

        msg = screen._parse_error(ConnectionError("Network unreachable"))
        assert "Network unreachable" in msg

    def test_do_register_calls_api(self, screen_manager):
        """Test do_register calls api in a thread"""
        from screens.login import LoginScreen

        login = LoginScreen(name="login")
        screen_manager.add_widget(login)
        login.toggle_mode()

        login.username_field.text = "newuser"
        login.password_field.text = "password123"

        with patch("screens.login.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            login.do_register()
            mock_thread.assert_called_once()
            assert login.action_btn.disabled is True


class TestHomeScreen:
    """Tests for HomeScreen"""

    def test_home_screen_creation(self, screen_manager):
        """Test HomeScreen can be instantiated"""
        from screens.home import HomeScreen

        screen = HomeScreen(name="home")
        screen_manager.add_widget(screen)

        assert screen.name == "home"

    def test_home_screen_navigate(self, screen_manager):
        """Test HomeScreen navigation method"""
        from screens.home import HomeScreen
        from screens.goals import GoalsScreen

        home = HomeScreen(name="home")
        goals = GoalsScreen(name="goals")
        screen_manager.add_widget(home)
        screen_manager.add_widget(goals)

        home.navigate("goals")
        assert screen_manager.current == "goals"

    def test_home_screen_has_stats(self, screen_manager):
        """Test HomeScreen has goals and journal stat cards"""
        from screens.home import HomeScreen

        home = HomeScreen(name="home")
        screen_manager.add_widget(home)

        assert hasattr(home, "goals_stat")
        assert hasattr(home, "journal_stat")

    def test_on_pre_enter_sets_username(self, screen_manager):
        """Test on_pre_enter shows username from api_client"""
        from screens.home import HomeScreen

        home = HomeScreen(name="home")
        screen_manager.add_widget(home)

        with patch("screens.home.api_client") as mock_client, \
             patch("screens.home.threading.Thread") as mock_thread:
            mock_client.username = "testuser"
            mock_thread.return_value = MagicMock()
            home.on_pre_enter()

        assert "testuser" in home.username_label.text

    def test_update_stats_updates_labels(self, screen_manager):
        """Test _update_stats sets stat card values"""
        from screens.home import HomeScreen

        home = HomeScreen(name="home")
        screen_manager.add_widget(home)

        home._update_stats("3/5", "7")

        assert home.goals_stat.value_label.text == "3/5"
        assert home.journal_stat.value_label.text == "7"

    def test_do_logout_clears_token_and_navigates(self, screen_manager):
        """Test do_logout calls api_client.logout and goes to login"""
        from screens.home import HomeScreen
        from screens.login import LoginScreen

        home = HomeScreen(name="home")
        login = LoginScreen(name="login")
        screen_manager.add_widget(login)
        screen_manager.add_widget(home)
        screen_manager.current = "home"

        with patch("screens.home.api_client") as mock_client:
            home.do_logout()
            mock_client.logout.assert_called_once()

        assert screen_manager.current == "login"


class TestGoalsScreen:
    """Tests for GoalsScreen"""

    def test_goals_screen_creation(self, screen_manager):
        """Test GoalsScreen can be instantiated"""
        from screens.goals import GoalsScreen

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        assert screen.name == "goals"

    def test_goals_screen_has_list(self, screen_manager):
        """Test GoalsScreen has goals list"""
        from screens.goals import GoalsScreen

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "goals_list")
        assert screen.goals_list is not None

    def test_goals_screen_starts_empty(self, screen_manager):
        """Test GoalsScreen starts with no goal cards (loads from API on enter)"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert len(cards) == 0

    def test_delete_goal_removes_card(self, screen_manager):
        """Test deleting a goal (no API ID) removes it from the list"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        screen._add_goal_card("Test goal")
        cards_before = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        screen.delete_goal(cards_before[0])
        cards_after = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]

        assert len(cards_after) == len(cards_before) - 1

    def test_add_goal_card_adds_to_list(self, screen_manager):
        """Test _add_goal_card adds a new GoalCard"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        cards_before = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        screen._add_goal_card("New test goal")
        cards_after = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]

        assert len(cards_after) == len(cards_before) + 1

    def test_empty_state_shown_on_start(self, screen_manager):
        """Test empty label is visible when screen has no goals"""
        from screens.goals import GoalsScreen

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        assert screen.empty_label.opacity == 1

    def test_empty_state_hidden_when_goals_exist(self, screen_manager):
        """Test empty label is hidden when there are goals"""
        from screens.goals import GoalsScreen

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        screen._add_goal_card("A goal")
        assert screen.empty_label.opacity == 0

    def test_empty_state_shown_when_no_goals(self, screen_manager):
        """Test empty label is visible when all goals are deleted"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        screen._add_goal_card("Goal 1")
        screen._add_goal_card("Goal 2")
        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        for card in cards:
            screen.delete_goal(card)

        assert screen.empty_label.opacity == 1

    def test_confirm_add_goal_ignores_empty_text(self, screen_manager):
        """Test confirm_add_goal does not spawn a thread for empty input"""
        from screens.goals import GoalsScreen, GoalCard
        from kivymd.uix.textfield import MDTextField

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        cards_before = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        screen.new_goal_field = MDTextField(text="   ")
        screen._dialog = MagicMock()

        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.confirm_add_goal()
            mock_thread.assert_not_called()

        cards_after = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert len(cards_after) == len(cards_before)

    def test_confirm_add_goal_calls_api(self, screen_manager):
        """Test confirm_add_goal spawns a thread to call create_goal"""
        from screens.goals import GoalsScreen
        from kivymd.uix.textfield import MDTextField

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        screen.new_goal_field = MDTextField(text="Walk 10k steps")
        screen._dialog = MagicMock()

        with patch("screens.goals.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.confirm_add_goal()
            mock_thread.assert_called_once()

    def test_load_goals_calls_api_in_thread(self, screen_manager):
        """Test load_goals spawns a background thread"""
        from screens.goals import GoalsScreen

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        with patch("screens.goals.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.load_goals()
            mock_thread.assert_called_once()

    def test_populate_goals_renders_cards(self, screen_manager):
        """Test _populate_goals creates a GoalCard for each goal"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        goals = [
            {"id": 1, "goal_text": "Run 5k", "completed": False},
            {"id": 2, "goal_text": "Read book", "completed": True},
        ]
        screen._populate_goals(goals)

        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert len(cards) == 2

    def test_populate_goals_sets_completed_state(self, screen_manager):
        """Test _populate_goals reflects completed flag on the card checkbox"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        goals = [{"id": 1, "goal_text": "Done goal", "completed": True}]
        screen._populate_goals(goals)

        cards = [w for w in screen.goals_list.children if isinstance(w, GoalCard)]
        assert cards[0].checkbox.active is True

    def test_delete_goal_with_id_calls_api(self, screen_manager):
        """Test delete_goal calls api_client.delete_goal when card has an ID"""
        from screens.goals import GoalsScreen

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)
        screen._add_goal_card("API goal", goal_id=42)

        from screens.goals import GoalCard
        card = next(w for w in screen.goals_list.children if isinstance(w, GoalCard))

        with patch("screens.goals.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.delete_goal(card)
            mock_thread.assert_called_once()

    def test_toggle_goal_with_id_calls_api(self, screen_manager):
        """Test toggle_goal calls api_client.update_goal when card has an ID"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)
        screen._add_goal_card("API goal", goal_id=7)

        card = next(w for w in screen.goals_list.children if isinstance(w, GoalCard))

        with patch("screens.goals.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.toggle_goal(card, True)
            mock_thread.assert_called_once()

    def test_toggle_goal_without_id_skips_api(self, screen_manager):
        """Test toggle_goal does nothing when card has no ID"""
        from screens.goals import GoalsScreen, GoalCard

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)
        screen._add_goal_card("Local goal")

        card = next(w for w in screen.goals_list.children if isinstance(w, GoalCard))

        with patch("screens.goals.threading.Thread") as mock_thread:
            screen.toggle_goal(card, True)
            mock_thread.assert_not_called()

    def test_show_error_sets_status_label(self, screen_manager):
        """Test show_error updates the status label"""
        from screens.goals import GoalsScreen

        screen = GoalsScreen(name="goals")
        screen_manager.add_widget(screen)

        screen.show_error("Network error")
        assert screen.status_label.text == "Network error"


class TestJournalScreen:
    """Tests for JournalScreen"""

    def test_journal_screen_creation(self, screen_manager):
        """Test JournalScreen can be instantiated"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        assert screen.name == "journal"

    def test_journal_screen_has_text_field(self, screen_manager):
        """Test JournalScreen has journal text field"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "journal_field")
        assert screen.journal_field is not None

    def test_journal_screen_has_date_label(self, screen_manager):
        """Test JournalScreen has a date label"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "date_label")
        assert screen.date_label.text != ""

    def test_journal_screen_has_nav_buttons(self, screen_manager):
        """Test JournalScreen has prev and next navigation buttons"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "prev_btn")
        assert hasattr(screen, "next_btn")

    def test_next_button_disabled_for_today(self, screen_manager):
        """Test next button is disabled when current_date is today"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        assert screen.next_btn.disabled is True

    def test_navigate_to_previous_day_changes_date(self, screen_manager):
        """Test _do_navigate_date(-1) moves current_date one day back"""
        import datetime
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        initial_date = screen.current_date
        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen._do_navigate_date(-1)

        assert screen.current_date == initial_date - datetime.timedelta(days=1)

    def test_navigate_to_previous_day_enables_next_button(self, screen_manager):
        """Test navigating to a past day re-enables the next button"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen._do_navigate_date(-1)

        assert screen.next_btn.disabled is False

    def test_navigate_date_updates_date_label(self, screen_manager):
        """Test _do_navigate_date updates the date label text"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        original_label = screen.date_label.text
        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen._do_navigate_date(-1)

        assert screen.date_label.text != original_label

    def test_has_unsaved_changes_false_when_text_matches(self, screen_manager):
        """Test _has_unsaved_changes returns False when field matches original"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._original_text = "hello"
        screen.journal_field.text = "hello"

        assert screen._has_unsaved_changes() is False

    def test_has_unsaved_changes_true_when_text_differs(self, screen_manager):
        """Test _has_unsaved_changes returns True when field differs from original"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._original_text = ""
        screen.journal_field.text = "Something new"

        assert screen._has_unsaved_changes() is True

    def test_set_entry_text_updates_field_and_original(self, screen_manager):
        """Test _set_entry_text populates field and resets original text"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._set_entry_text("Today was great")

        assert screen.journal_field.text == "Today was great"
        assert screen._original_text == "Today was great"

    def test_load_entry_spawns_thread(self, screen_manager):
        """Test load_entry runs in a background thread"""
        import datetime
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.load_entry(datetime.date.today())
            mock_thread.assert_called_once()

    def test_save_entry_updates_original_text(self, screen_manager):
        """Test _on_save_success marks current text as saved"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.journal_field.text = "My journal entry"
        screen._on_save_success("My journal entry")

        assert screen._original_text == "My journal entry"
        assert screen._has_unsaved_changes() is False

    def test_go_back_without_changes_navigates_immediately(self, screen_manager):
        """Test go_back navigates directly when there are no unsaved changes"""
        from screens.journal import JournalScreen
        from screens.home import HomeScreen

        screen = JournalScreen(name="journal")
        home = HomeScreen(name="home")
        screen_manager.add_widget(screen)
        screen_manager.add_widget(home)

        screen._original_text = ""
        screen.journal_field.text = ""
        screen.go_back()

        assert screen_manager.current == "home"

    def test_go_back_with_changes_shows_discard_dialog(self, screen_manager):
        """Test go_back calls _show_discard_dialog when unsaved changes exist"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._original_text = ""
        screen.journal_field.text = "Unsaved text"

        with patch.object(screen, "_show_discard_dialog") as mock_show:
            screen.go_back()
            mock_show.assert_called_once()

    def test_navigate_date_with_changes_shows_discard_dialog(self, screen_manager):
        """Test navigate_date prompts for confirmation when unsaved changes exist"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._original_text = ""
        screen.journal_field.text = "Unsaved text"

        with patch.object(screen, "_show_discard_dialog") as mock_show:
            screen.navigate_date(-1)
            mock_show.assert_called_once()

    def test_navigate_date_without_changes_navigates_directly(self, screen_manager):
        """Test navigate_date moves directly when there are no unsaved changes"""
        import datetime
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._original_text = ""
        screen.journal_field.text = ""
        initial_date = screen.current_date

        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.navigate_date(-1)

        assert screen.current_date == initial_date - datetime.timedelta(days=1)

    def test_confirm_discard_calls_callback_and_closes_dialog(self, screen_manager):
        """Test _confirm_discard dismisses dialog and invokes the callback"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._dialog = MagicMock()
        callback = MagicMock()
        screen._confirm_discard(callback)

        callback.assert_called_once()
        assert screen._dialog is None

    def test_show_discard_dialog_does_not_stack_on_double_tap(self, screen_manager):
        """Test _show_discard_dialog is a no-op when a dialog is already open"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._original_text = ""
        screen.journal_field.text = "Unsaved text"

        existing_dialog = MagicMock()
        screen._dialog = existing_dialog

        screen._show_discard_dialog(on_discard=MagicMock())

        assert screen._dialog is existing_dialog

    def test_do_navigate_date_cannot_advance_past_today(self, screen_manager):
        """Test _do_navigate_date(1) is a no-op when already on today"""
        import datetime
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        assert screen.current_date == datetime.date.today()
        screen._do_navigate_date(1)
        assert screen.current_date == datetime.date.today()

    def test_set_entry_text_stores_entry_id(self, screen_manager):
        """Test _set_entry_text stores the entry id"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._set_entry_text("Some content", entry_id=42)

        assert screen._entry_id == 42

    def test_set_entry_text_clears_entry_id_for_empty(self, screen_manager):
        """Test _set_entry_text clears entry_id when no entry"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen._set_entry_text("", entry_id=None)

        assert screen._entry_id is None

    def test_save_entry_does_nothing_when_content_empty(self, screen_manager):
        """Test save_entry is a no-op when the text field is empty"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.journal_field.text = ""
        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.save_entry()
            mock_thread.assert_not_called()

    def test_save_entry_spawns_thread(self, screen_manager):
        """Test save_entry runs API call in a background thread"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.journal_field.text = "My entry"
        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.save_entry()
            mock_thread.assert_called_once()

    def test_save_entry_disables_button_while_saving(self, screen_manager):
        """Test save_entry disables the save button before the API call"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.journal_field.text = "My entry"
        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.save_entry()
            assert screen.save_btn.disabled is True

    def test_save_entry_calls_create_when_no_entry_id(self, screen_manager):
        """Test save_entry calls create_journal_entry when no entry_id is set"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.journal_field.text = "My entry"
        screen._entry_id = None

        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.save_entry()
        target_fn = mock_thread.call_args[1]["target"]
        with patch("screens.journal.api_client") as mock_api:
            mock_api.create_journal_entry.return_value = {"id": 10, "content": "My entry"}
            with patch("screens.journal.Clock"):
                target_fn()
                mock_api.create_journal_entry.assert_called_once()
                mock_api.update_journal_entry.assert_not_called()

    def test_save_entry_calls_update_when_entry_id_set(self, screen_manager):
        """Test save_entry calls update_journal_entry when entry_id is known"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.journal_field.text = "Updated entry"
        screen._entry_id = 42

        with patch("screens.journal.threading.Thread") as mock_thread:
            screen.save_entry()
        target_fn = mock_thread.call_args[1]["target"]
        with patch("screens.journal.api_client") as mock_api:
            mock_api.update_journal_entry.return_value = {"id": 42, "content": "Updated entry"}
            with patch("screens.journal.Clock"):
                target_fn()
                mock_api.update_journal_entry.assert_called_once_with(42, "Updated entry")
                mock_api.create_journal_entry.assert_not_called()

    def test_on_save_success_updates_state(self, screen_manager):
        """Test _on_save_success re-enables button and stores entry_id"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.save_btn.disabled = True
        screen._entry_id = None

        screen._on_save_success("My saved text", entry_id=99)

        assert screen._original_text == "My saved text"
        assert screen._entry_id == 99
        assert screen.save_btn.disabled is False
        assert screen.status_label.text == "Saved"

    def test_on_save_error_re_enables_button(self, screen_manager):
        """Test _on_save_error re-enables the save button and shows a friendly message"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.save_btn.disabled = True

        screen._on_save_error()

        assert screen.save_btn.disabled is False
        assert screen.status_label.text == "Could not save. Please try again."

    def test_load_entry_shows_loading_status(self, screen_manager):
        """Test load_entry sets status label to Loading... before the API call"""
        import datetime
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.load_entry(datetime.date.today())

        assert screen.status_label.text == "Loading..."

    def test_set_entry_text_clears_loading_status(self, screen_manager):
        """Test _set_entry_text clears the loading status label"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.status_label.text = "Loading..."
        screen._set_entry_text("Some content", entry_id=1)

        assert screen.status_label.text == ""

    def test_save_entry_strips_whitespace_in_field(self, screen_manager):
        """Test save_entry syncs stripped content back to the text field"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        screen.journal_field.text = "  My entry   "
        with patch("screens.journal.threading.Thread") as mock_thread:
            mock_thread.return_value = MagicMock()
            screen.save_entry()

        assert screen.journal_field.text == "My entry"

    def test_on_save_success_clears_status_after_delay(self, screen_manager):
        """Test _on_save_success schedules status label clear after 2.5s"""
        from screens.journal import JournalScreen

        screen = JournalScreen(name="journal")
        screen_manager.add_widget(screen)

        with patch("screens.journal.Clock") as mock_clock:
            screen._on_save_success("text", entry_id=1)

        assert screen.status_label.text == "Saved"
        # Two Clock.schedule_once calls: one from the thread, one for the clear
        assert mock_clock.schedule_once.call_count == 1
        # Trigger the scheduled clear and verify it resets the label
        mock_clock.schedule_once.call_args[0][0](0)
        assert screen.status_label.text == ""

class TestAnalysisScreen:
    """Tests for AnalysisScreen"""

    def test_analysis_screen_creation(self, screen_manager):
        """Test AnalysisScreen can be instantiated"""
        from screens.analysis import AnalysisScreen

        screen = AnalysisScreen(name="analysis")
        screen_manager.add_widget(screen)

        assert screen.name == "analysis"

    def test_analysis_screen_has_text_label(self, screen_manager):
        """Test AnalysisScreen has analysis text label"""
        from screens.analysis import AnalysisScreen

        screen = AnalysisScreen(name="analysis")
        screen_manager.add_widget(screen)

        assert hasattr(screen, "analysis_text")
        assert screen.analysis_text is not None
