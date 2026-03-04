"""Tests for screen modules"""

import pytest


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
