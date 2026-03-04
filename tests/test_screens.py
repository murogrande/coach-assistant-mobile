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
