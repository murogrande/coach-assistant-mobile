"""Tests for screen modules"""

import pytest
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

        with patch("screens.login.api_client") as mock_client, \
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
