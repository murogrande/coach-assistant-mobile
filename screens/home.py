"""Home Screen"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.icon_definitions import md_icons

from services.api_client import api_client


class NavCard(MDCard):
    """Tappable card for home screen navigation"""

    def __init__(self, icon: str, title: str, subtitle: str, on_tap, **kwargs):
        super().__init__(
            orientation="horizontal",
            padding=[20, 18, 20, 18],
            spacing=20,
            size_hint=(1, None),
            height=88,
            elevation=1,
            style="elevated",
            ripple_behavior=True,
            **kwargs,
        )
        self._on_tap = on_tap

        icon_label = MDLabel(
            text=md_icons.get(icon, ""),
            font_style="Icon",
            font_size="32sp",
            size_hint=(None, 1),
            width=48,
            halign="center",
            theme_text_color="Custom",
            text_color=(0.129, 0.588, 0.953, 1),
        )
        self.add_widget(icon_label)

        text_col = MDBoxLayout(orientation="vertical", spacing=2)
        text_col.add_widget(MDLabel(
            text=title,
            font_style="Title",
            role="medium",
            adaptive_height=True,
        ))
        text_col.add_widget(MDLabel(
            text=subtitle,
            font_style="Body",
            role="small",
            theme_text_color="Secondary",
            adaptive_height=True,
        ))
        self.add_widget(text_col)

        chevron = MDLabel(
            text=md_icons.get("chevron-right", ""),
            font_style="Icon",
            font_size="24sp",
            size_hint=(None, 1),
            width=32,
            halign="center",
            theme_text_color="Secondary",
        )
        self.add_widget(chevron)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._on_tap()
            return True
        return super().on_touch_down(touch)


class HomeScreen(MDScreen):
    """Main home screen with navigation to other sections"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        root = MDBoxLayout(orientation="vertical")

        # --- Hero header ---
        header = MDBoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=160,
            padding=[32, 32, 32, 24],
            spacing=6,
            md_bg_color=(0.129, 0.588, 0.953, 1),
        )
        header.add_widget(MDLabel(
            text="Coach Assistant",
            font_style="Display",
            role="small",
            halign="left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            adaptive_height=True,
        ))
        header.add_widget(MDLabel(
            text="What would you like to do today?",
            font_style="Body",
            role="large",
            halign="left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.85),
            adaptive_height=True,
        ))
        root.add_widget(header)

        # --- Content area ---
        content_bg = MDBoxLayout(
            orientation="vertical",
            md_bg_color=(0.96, 0.96, 0.96, 1),
        )

        scroll = MDScrollView()
        inner = MDBoxLayout(
            orientation="vertical",
            padding=[20, 24, 20, 20],
            spacing=14,
            adaptive_height=True,
        )

        inner.add_widget(NavCard(
            icon="flag-checkered",
            title="My Goals",
            subtitle="Track your weekly goals",
            on_tap=lambda: self.navigate("goals"),
        ))
        inner.add_widget(NavCard(
            icon="notebook",
            title="Journal",
            subtitle="Write your daily entry",
            on_tap=lambda: self.navigate("journal"),
        ))
        inner.add_widget(NavCard(
            icon="chart-bar",
            title="Weekly Analysis",
            subtitle="Review your progress",
            on_tap=lambda: self.navigate("analysis"),
        ))

        # Logout button
        logout_row = MDBoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=56,
            padding=[0, 8, 0, 0],
        )
        logout_btn = MDButton(
            style="text",
            theme_width="Custom",
            size_hint_x=1,
            on_release=self.do_logout,
        )
        logout_btn.add_widget(MDButtonText(text="Logout"))
        logout_row.add_widget(logout_btn)
        inner.add_widget(logout_row)

        scroll.add_widget(inner)
        content_bg.add_widget(scroll)
        root.add_widget(content_bg)
        self.add_widget(root)

    def navigate(self, screen_name):
        self.manager.current = screen_name

    def do_logout(self, *args):
        api_client.logout()
        self.manager.current = "login"
