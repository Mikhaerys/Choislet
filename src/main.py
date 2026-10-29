"""Choislet - Decision making desktop application with Flet 1.0."""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure project root and src directory are in sys.path for reliable imports
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import flet as ft
from src.utils.constants import AppColors, get_asset_path, get_fs_asset_path
from src.views.home_view import HomeView
from src.views.roulette_view import RouletteView
from src.views.coin_view import CoinView
from src.views.dice_view import DiceView


class ChoisletApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        self._init_views()
        self._build_layout()
        self.switch_to_tab(0)

    def _setup_page(self) -> None:
        self.page.title = "Choislet"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.bgcolor = AppColors.OXFORD_BLUE

        # Configure responsive desktop window boundaries if running in desktop mode
        try:
            if hasattr(self.page, "window") and self.page.window:
                self.page.window.width = 1200
                self.page.window.height = 760
                self.page.window.min_width = 850
                self.page.window.min_height = 550
                ico_path = get_fs_asset_path("Choislet.ico")
                if Path(ico_path).exists():
                    self.page.window.icon = ico_path
        except Exception:
            pass

    def _init_views(self) -> None:
        self.home_view = HomeView(self.page, on_navigate=self.switch_to_tab)
        self.roulette_view = RouletteView(self.page)
        self.coin_view = CoinView(self.page)
        self.dice_view = DiceView(self.page)

        self.views = [
            self.home_view,
            self.roulette_view,
            self.coin_view,
            self.dice_view,
        ]

        # Initially show Home view, hide others
        for i, view in enumerate(self.views):
            view.visible = (i == 0)

    def _build_layout(self) -> None:
        # Navigation Rail sidebar with Material 3 styling
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=72,
            min_extended_width=180,
            bgcolor=AppColors.PRUSSIAN_BLUE,
            leading=ft.Container(
                content=ft.Image(
                    src=get_asset_path("Choislet.png"),
                    width=42,
                    height=42,
                    fit=ft.BoxFit.CONTAIN,
                ),
                padding=ft.Padding(top=16, bottom=12, left=10, right=10),
                tooltip="Choislet Home",
                on_click=lambda _: self.switch_to_tab(0),
            ),
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME_ROUNDED,
                    label="Home",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PIE_CHART_OUTLINE_ROUNDED,
                    selected_icon=ft.Icons.PIE_CHART_ROUNDED,
                    label="Roulette",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.TOLL_OUTLINED,
                    selected_icon=ft.Icons.TOLL_ROUNDED,
                    label="Coin",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CASINO_OUTLINED,
                    selected_icon=ft.Icons.CASINO_ROUNDED,
                    label="Dice",
                ),
            ],
            on_change=self._on_rail_change,
        )

        # Content stack keeps all views mounted in session tree, switching via visibility
        self.content_stack = ft.Stack(
            expand=True,
            controls=self.views,
        )

        self.content_area = ft.Container(
            expand=True,
            bgcolor=AppColors.OXFORD_BLUE,
            content=self.content_stack,
        )

        root_row = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self.rail,
                self.content_area,
            ],
        )

        self.page.add(root_row)

    @property
    def current_view(self):
        return self.views[self.rail.selected_index]

    def _on_rail_change(self, e: ft.ControlEvent) -> None:
        idx = int(e.control.selected_index)
        self.switch_to_tab(idx)

    def switch_to_tab(self, index: int) -> None:
        if 0 <= index < len(self.views):
            self.rail.selected_index = index
            for i, view in enumerate(self.views):
                is_active = (i == index)
                view.visible = is_active
                if is_active:
                    view.on_activate()
                else:
                    view.on_deactivate()
            self.page.update()


async def main(page: ft.Page) -> None:
    ChoisletApp(page)


if __name__ == "__main__":
    ft.run(main)
