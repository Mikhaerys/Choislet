"""Coin flip view with dynamic 3D-like flip animation and statistics."""

from __future__ import annotations
import asyncio
import flet as ft
from src.views.base_view import BaseView
from src.utils.constants import AppColors, get_text_field_border
from src.logic.coin_logic import flip_coin, CoinStats, CoinSide


class CoinView(BaseView):
    def __init__(self, page: ft.Page):
        self.stats = CoinStats()
        self.is_flipping: bool = False
        super().__init__(page)

    def init_view(self) -> ft.Control:
        # Coin visual container
        self.coin_label = ft.Text(
            "FLIP",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=AppColors.OXFORD_BLUE,
            text_align=ft.TextAlign.CENTER,
        )

        self.coin_container = ft.Container(
            width=220,
            height=220,
            border_radius=110,
            bgcolor=AppColors.SAFFRON,
            alignment=ft.Alignment.CENTER,
            border=ft.Border.all(6, AppColors.COLUMBIA_BLUE),
            scale=ft.Scale(scale_x=1.0, scale_y=1.0),
            animate_scale=ft.Animation(90, ft.AnimationCurve.EASE_IN_OUT),
            content=self.coin_label,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=16,
                color=ft.Colors.with_opacity(0.4, AppColors.SAFFRON),
                offset=ft.Offset(0, 6),
            ),
        )

        # Result badge
        self.result_badge = ft.Container(
            content=ft.Text(
                "Click 'Flip Coin' to toss!",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=AppColors.SAFFRON,
                text_align=ft.TextAlign.CENTER,
            ),
            padding=ft.Padding(left=20, right=20, top=12, bottom=12),
            bgcolor=AppColors.CARD_BG,
            border_radius=12,
            border=ft.Border.all(1, AppColors.PRUSSIAN_BLUE),
            alignment=ft.Alignment.CENTER,
        )

        # Statistics chips
        self.stats_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
            controls=[
                self._create_stat_badge("Total", "0"),
                self._create_stat_badge("Heads", "0"),
                self._create_stat_badge("Tails", "0"),
            ],
        )

        left_panel = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=28,
            controls=[
                self.coin_container,
                self.result_badge,
                self.stats_row,
            ],
        )

        # Custom inputs
        self.heads_input = ft.TextField(
            value="Heads",
            label="Heads Option",
            label_style=ft.TextStyle(color=AppColors.COLUMBIA_BLUE),
            color=AppColors.TEXT_LIGHT,
            bgcolor=AppColors.CARD_BG,
            border=get_text_field_border(12),
            prefix_icon=ft.Icons.RADIO_BUTTON_CHECKED,
        )

        self.tails_input = ft.TextField(
            value="Tails",
            label="Tails Option",
            label_style=ft.TextStyle(color=AppColors.COLUMBIA_BLUE),
            color=AppColors.TEXT_LIGHT,
            bgcolor=AppColors.CARD_BG,
            border=get_text_field_border(12),
            prefix_icon=ft.Icons.CHANGE_CIRCLE,
        )

        self.flip_button = ft.FilledButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.TOLL_ROUNDED, color=AppColors.OXFORD_BLUE),
                    ft.Text("Flip Coin", size=18, weight=ft.FontWeight.BOLD, color=AppColors.OXFORD_BLUE),
                ],
            ),
            style=ft.ButtonStyle(
                bgcolor=AppColors.SAFFRON,
                padding=ft.Padding(left=24, right=24, top=16, bottom=16),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=280,
            height=54,
            on_click=self._flip_click,
        )

        presets = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
            spacing=8,
            controls=[
                self._create_preset_chip("Yes / No", "Yes", "No"),
                self._create_preset_chip("Buy / Wait", "Buy", "Wait"),
                self._create_preset_chip("Left / Right", "Left", "Right"),
                self._create_preset_chip("Heads / Tails", "Heads", "Tails"),
            ],
        )

        right_panel = ft.Container(
            bgcolor=AppColors.SURFACE_VARIANT,
            border_radius=16,
            padding=ft.Padding(left=24, right=24, top=24, bottom=24),
            border=ft.Border.all(1, AppColors.PRUSSIAN_BLUE),
            content=ft.Column(
                spacing=18,
                controls=[
                    ft.Text(
                        "Coin Options",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.SAFFRON,
                    ),
                    ft.Text(
                        "Customize the names for each side of the coin or pick a quick preset.",
                        size=13,
                        color=AppColors.TEXT_MUTED,
                    ),
                    self.heads_input,
                    self.tails_input,
                    ft.Text("Quick Presets:", size=13, weight=ft.FontWeight.BOLD, color=AppColors.COLUMBIA_BLUE),
                    presets,
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[self.flip_button],
                    ),
                ],
            ),
        )

        return ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=32,
            run_spacing=24,
            controls=[
                ft.Container(
                    col={"xs": 12, "sm": 12, "md": 12, "lg": 6, "xl": 6},
                    content=left_panel,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(
                    col={"xs": 12, "sm": 12, "md": 12, "lg": 6, "xl": 5},
                    content=right_panel,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
        )

    def _create_stat_badge(self, label: str, value: str) -> ft.Control:
        return ft.Container(
            bgcolor=AppColors.CARD_BG,
            border_radius=10,
            padding=ft.Padding(left=16, right=16, top=10, bottom=10),
            border=ft.Border.all(1, AppColors.PRUSSIAN_BLUE),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=AppColors.COLUMBIA_BLUE),
                    ft.Text(label, size=12, color=AppColors.TEXT_MUTED),
                ],
            ),
        )

    def _create_preset_chip(self, label: str, heads_val: str, tails_val: str) -> ft.Control:
        return ft.OutlinedButton(
            content=ft.Text(label, size=12, color=AppColors.COLUMBIA_BLUE),
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, AppColors.PRUSSIAN_BLUE),
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding(left=10, right=10, top=6, bottom=6),
            ),
            on_click=lambda _: self._apply_preset(heads_val, tails_val),
        )

    def _apply_preset(self, heads: str, tails: str) -> None:
        self.heads_input.value = heads
        self.tails_input.value = tails
        self.app_page.update()

    def _update_stats_display(self) -> None:
        self.stats_row.controls = [
            self._create_stat_badge("Total", str(self.stats.total_flips)),
            self._create_stat_badge("Heads", str(self.stats.heads_count)),
            self._create_stat_badge("Tails", str(self.stats.tails_count)),
        ]

    async def _flip_click(self, _: ft.ControlEvent) -> None:
        if self.is_flipping:
            return

        self.is_flipping = True
        self.flip_button.disabled = True
        self.flip_button.content = ft.ProgressRing(
            width=22,
            height=22,
            stroke_width=2.5,
            color=AppColors.OXFORD_BLUE,
        )
        self.result_badge.content = ft.Text(
            "Coin in the air...",
            size=18,
            weight=ft.FontWeight.W_600,
            color=AppColors.COLUMBIA_BLUE,
            text_align=ft.TextAlign.CENTER,
        )
        self.app_page.update()

        # Decide final outcome upfront
        heads_name = self.heads_input.value or "Heads"
        tails_name = self.tails_input.value or "Tails"
        result = flip_coin(heads_name, tails_name)

        # Realistic 3D flip animation: squash and expand horizontally while flipping sides
        num_spins = 6
        current_side = CoinSide.HEADS

        for i in range(num_spins):
            # Collapse horizontally
            self.coin_container.scale = ft.Scale(scale_x=0.08, scale_y=1.0)
            self.app_page.update()
            await asyncio.sleep(0.09)

            # Alternate side visual at the apex of thinness
            current_side = CoinSide.TAILS if current_side == CoinSide.HEADS else CoinSide.HEADS
            self.coin_label.value = "HEADS" if current_side == CoinSide.HEADS else "TAILS"
            self.coin_container.bgcolor = AppColors.SAFFRON if current_side == CoinSide.HEADS else AppColors.COLUMBIA_BLUE
            self.coin_label.color = AppColors.OXFORD_BLUE

            # Expand horizontally
            self.coin_container.scale = ft.Scale(scale_x=1.0, scale_y=1.0)
            self.app_page.update()
            await asyncio.sleep(0.09)

        # Final landing
        self.coin_container.scale = ft.Scale(scale_x=0.08, scale_y=1.0)
        self.app_page.update()
        await asyncio.sleep(0.09)

        # Set actual winner state
        final_is_heads = result.side == CoinSide.HEADS
        self.coin_label.value = "HEADS" if final_is_heads else "TAILS"
        self.coin_container.bgcolor = AppColors.SAFFRON if final_is_heads else AppColors.COLUMBIA_BLUE
        self.coin_container.scale = ft.Scale(scale_x=1.0, scale_y=1.0)
        self.app_page.update()
        await asyncio.sleep(0.12)

        # Record statistics
        self.stats.record(result)
        self._update_stats_display()

        # Update result display
        self.result_badge.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=AppColors.SUCCESS, size=24),
                ft.Text(
                    f"Result: {result.label} ({result.side.value})",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.SAFFRON,
                ),
            ],
        )

        # Re-enable button
        self.flip_button.disabled = False
        self.flip_button.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.TOLL_ROUNDED, color=AppColors.OXFORD_BLUE),
                ft.Text("Flip Coin", size=18, weight=ft.FontWeight.BOLD, color=AppColors.OXFORD_BLUE),
            ],
        )
        self.is_flipping = False
        self.app_page.update()
