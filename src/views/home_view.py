"""Home dashboard view with feature overview and quick navigation."""

from __future__ import annotations
from typing import Callable
import flet as ft
from src.views.base_view import BaseView
from src.utils.constants import AppColors, get_asset_path


class HomeView(BaseView):
    def __init__(self, page: ft.Page, on_navigate: Callable[[int], None]):
        self.on_navigate = on_navigate
        super().__init__(page)

    def _create_feature_card(
        self,
        title: str,
        description: str,
        icon_asset: str,
        target_index: int,
        button_text: str,
    ) -> ft.Control:
        return ft.Container(
            col={"xs": 12, "sm": 12, "md": 4, "lg": 4},
            bgcolor=AppColors.CARD_BG,
            border_radius=16,
            padding=ft.Padding(left=24, right=24, top=28, bottom=28),
            border=ft.Border.all(1, AppColors.PRUSSIAN_BLUE),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.Container(
                        width=72,
                        height=72,
                        border_radius=36,
                        bgcolor=AppColors.SURFACE_VARIANT,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Image(
                            src=get_asset_path(icon_asset),
                            width=44,
                            height=44,
                            fit=ft.BoxFit.CONTAIN,
                        ),
                    ),
                    ft.Text(
                        title,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.SAFFRON,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        description,
                        size=14,
                        color=AppColors.TEXT_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.FilledButton(
                        content=ft.Text(button_text, size=14, weight=ft.FontWeight.W_600),
                        style=ft.ButtonStyle(
                            bgcolor=AppColors.CERULEAN,
                            color=AppColors.COLUMBIA_BLUE,
                            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        on_click=lambda _: self.on_navigate(target_index),
                    ),
                ],
            ),
        )

    def init_view(self) -> ft.Control:
        header = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Image(
                    src=get_asset_path("Choislet.png"),
                    width=70,
                    height=70,
                    fit=ft.BoxFit.CONTAIN,
                ),
                ft.Text(
                    "Welcome to Choislet",
                    size=34,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.SAFFRON,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Your interactive assistant to make fast, fair, and fun random decisions.",
                    size=16,
                    color=AppColors.COLUMBIA_BLUE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        )

        cards = ft.ResponsiveRow(
            spacing=20,
            run_spacing=20,
            controls=[
                self._create_feature_card(
                    title="Roulette",
                    description="Enter custom candidates, spin the animated wheel, and let fate pick a winner.",
                    icon_asset="ruleta.png",
                    target_index=1,
                    button_text="Launch Roulette",
                ),
                self._create_feature_card(
                    title="Coin Flip",
                    description="Quick heads-or-tails coin toss with custom options and real-time statistics.",
                    icon_asset="moneda.png",
                    target_index=2,
                    button_text="Flip Coin",
                ),
                self._create_feature_card(
                    title="Dice Game",
                    description="Roll pairs of dice for a multiplayer tournament with automatic tie-breakers.",
                    icon_asset="dado.png",
                    target_index=3,
                    button_text="Start Game",
                ),
            ],
        )

        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=32,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Container(height=10),
                header,
                ft.Container(
                    content=cards,
                    padding=ft.Padding(left=20, right=20, top=10, bottom=20),
                ),
            ],
        )
