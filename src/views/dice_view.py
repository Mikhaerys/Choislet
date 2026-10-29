"""Dice tournament view with animated rolling dice and interactive scoreboard."""

from __future__ import annotations
import asyncio
import random
import flet as ft
from src.views.base_view import BaseView
from src.utils.constants import AppColors, get_text_field_border
from src.logic.dice_logic import (
    parse_players,
    play_tournament,
    TournamentResult,
    roll_single_die,
)


class DiceView(BaseView):
    def __init__(self, page: ft.Page):
        self.default_players = "Player 1\nPlayer 2\nPlayer 3\nPlayer 4"
        self.is_rolling: bool = False
        super().__init__(page)

    def _create_die_face(self, value: int) -> ft.Control:
        """Render a realistic die face with dot pips in a 3x3 pattern."""
        active_coords = {
            1: {(1, 1)},
            2: {(0, 2), (2, 0)},
            3: {(0, 2), (1, 1), (2, 0)},
            4: {(0, 0), (0, 2), (2, 0), (2, 2)},
            5: {(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)},
            6: {(0, 0), (1, 0), (2, 0), (0, 2), (1, 2), (2, 2)},
        }.get(value, {(1, 1)})

        rows: list[ft.Row] = []
        for r in range(3):
            cols: list[ft.Control] = []
            for c in range(3):
                if (r, c) in active_coords:
                    dot = ft.Container(
                        width=14,
                        height=14,
                        border_radius=7,
                        bgcolor=AppColors.OXFORD_BLUE,
                    )
                else:
                    dot = ft.Container(width=14, height=14)
                cols.append(dot)
            rows.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=cols,
                )
            )

        return ft.Container(
            width=92,
            height=92,
            border_radius=18,
            bgcolor=AppColors.COLUMBIA_BLUE,
            padding=ft.Padding(left=10, right=10, top=10, bottom=10),
            alignment=ft.Alignment.CENTER,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.3, "#000000"),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                controls=rows,
            ),
        )

    def init_view(self) -> ft.Control:
        # Two animated dice containers
        self.die_1_container = ft.Container(
            content=self._create_die_face(1),
            scale=ft.Scale(1.0),
            animate_scale=ft.Animation(80, ft.AnimationCurve.EASE_OUT),
        )
        self.die_2_container = ft.Container(
            content=self._create_die_face(1),
            scale=ft.Scale(1.0),
            animate_scale=ft.Animation(80, ft.AnimationCurve.EASE_OUT),
        )

        dice_row = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=24,
            controls=[self.die_1_container, self.die_2_container],
        )

        # Winner / Status banner
        self.status_banner = ft.Container(
            content=ft.Text(
                "Ready to roll! Enter players and click Roll Dice.",
                size=16,
                weight=ft.FontWeight.W_600,
                color=AppColors.SAFFRON,
                text_align=ft.TextAlign.CENTER,
            ),
            padding=ft.Padding(left=18, right=18, top=12, bottom=12),
            bgcolor=AppColors.CARD_BG,
            border_radius=12,
            border=ft.Border.all(1, AppColors.PRUSSIAN_BLUE),
            alignment=ft.Alignment.CENTER,
        )

        # Tournament scoreboard container
        self.scoreboard_column = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Text(
                    "Tournament rounds will appear here after rolling.",
                    size=13,
                    color=AppColors.TEXT_MUTED,
                    italic=True,
                )
            ],
        )

        scoreboard_card = ft.Container(
            height=260,
            bgcolor=AppColors.CARD_BG,
            border_radius=14,
            padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            border=ft.Border.all(1, AppColors.PRUSSIAN_BLUE),
            content=self.scoreboard_column,
        )

        left_panel = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                dice_row,
                self.status_banner,
                ft.Text("Round Breakdown", size=15, weight=ft.FontWeight.BOLD, color=AppColors.COLUMBIA_BLUE),
                scoreboard_card,
            ],
        )

        # User input section
        self.players_input = ft.TextField(
            value=self.default_players,
            multiline=True,
            min_lines=8,
            max_lines=12,
            label="Players (one per line)",
            label_style=ft.TextStyle(color=AppColors.COLUMBIA_BLUE),
            color=AppColors.TEXT_LIGHT,
            bgcolor=AppColors.CARD_BG,
            border=get_text_field_border(12),
            cursor_color=AppColors.SAFFRON,
        )

        self.roll_button = ft.FilledButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.CASINO_ROUNDED, color=AppColors.OXFORD_BLUE),
                    ft.Text("Roll Dice", size=18, weight=ft.FontWeight.BOLD, color=AppColors.OXFORD_BLUE),
                ],
            ),
            style=ft.ButtonStyle(
                bgcolor=AppColors.SAFFRON,
                padding=ft.Padding(left=24, right=24, top=16, bottom=16),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=280,
            height=54,
            on_click=self._roll_click,
        )

        preset_btn = ft.OutlinedButton(
            content=ft.Text("Load 4 Players", color=AppColors.COLUMBIA_BLUE),
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, AppColors.PRUSSIAN_BLUE),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda _: self._set_players(self.default_players),
        )

        clear_btn = ft.OutlinedButton(
            content=ft.Text("Clear", color=AppColors.TEXT_MUTED),
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, AppColors.PRUSSIAN_BLUE),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda _: self._set_players(""),
        )

        right_panel = ft.Container(
            bgcolor=AppColors.SURFACE_VARIANT,
            border_radius=16,
            padding=ft.Padding(left=24, right=24, top=24, bottom=24),
            border=ft.Border.all(1, AppColors.PRUSSIAN_BLUE),
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Text(
                        "Dice Tournament",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.SAFFRON,
                    ),
                    ft.Text(
                        "Add at least 2 players. Each rolls 2 dice. Tied leaders roll tie-breaker rounds until a single champion wins.",
                        size=13,
                        color=AppColors.TEXT_MUTED,
                    ),
                    self.players_input,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[preset_btn, clear_btn],
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[self.roll_button],
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

    def _set_players(self, text: str) -> None:
        if self.is_rolling:
            return
        self.players_input.value = text
        self.app_page.update()

    async def _roll_click(self, _: ft.ControlEvent) -> None:
        if self.is_rolling:
            return

        players = parse_players(self.players_input.value)
        if len(players) < 2:
            dlg = ft.AlertDialog(
                title=ft.Text("Not Enough Players"),
                content=ft.Text("Please enter at least 2 unique players to start a tournament."),
                actions=[ft.TextButton("OK", on_click=lambda _: self.app_page.close(dlg))],
            )
            self.app_page.open(dlg)
            return

        self.is_rolling = True
        self.roll_button.disabled = True
        self.roll_button.content = ft.ProgressRing(
            width=22,
            height=22,
            stroke_width=2.5,
            color=AppColors.OXFORD_BLUE,
        )
        self.status_banner.content = ft.Text(
            "Rolling dice...",
            size=18,
            weight=ft.FontWeight.W_600,
            color=AppColors.COLUMBIA_BLUE,
            text_align=ft.TextAlign.CENTER,
        )
        self.app_page.update()

        # Simulate tournament upfront
        tournament: TournamentResult = play_tournament(players)

        # Dynamic rolling animation (10 rapid shuffles)
        for _ in range(10):
            d1 = roll_single_die()
            d2 = roll_single_die()
            self.die_1_container.content = self._create_die_face(d1)
            self.die_2_container.content = self._create_die_face(d2)
            self.die_1_container.scale = ft.Scale(random.uniform(0.92, 1.08))
            self.die_2_container.scale = ft.Scale(random.uniform(0.92, 1.08))
            self.app_page.update()
            await asyncio.sleep(0.08)

        # Final landing
        self.die_1_container.scale = ft.Scale(1.0)
        self.die_2_container.scale = ft.Scale(1.0)
        self.die_1_container.content = self._create_die_face(tournament.final_die1)
        self.die_2_container.content = self._create_die_face(tournament.final_die2)

        # Populate scoreboard cleanly
        round_controls: list[ft.Control] = []
        for r in tournament.rounds:
            round_title = (
                f"Round {r.round_number}" if r.round_number == 1 else f"Tie-Breaker Round {r.round_number}"
            )
            round_controls.append(
                ft.Text(round_title, size=14, weight=ft.FontWeight.BOLD, color=AppColors.SAFFRON)
            )

            scores_row: list[ft.Control] = []
            for roll in r.rolls:
                is_leader = roll.player in r.winners
                chip = ft.Container(
                    bgcolor=AppColors.SURFACE_VARIANT if not is_leader else AppColors.CERULEAN,
                    border_radius=8,
                    padding=ft.Padding(left=10, right=10, top=6, bottom=6),
                    border=ft.Border.all(1, AppColors.SAFFRON if is_leader else AppColors.PRUSSIAN_BLUE),
                    content=ft.Text(
                        f"{roll.player}: {roll.total} ({roll.die1}+{roll.die2})",
                        size=12,
                        weight=ft.FontWeight.BOLD if is_leader else ft.FontWeight.NORMAL,
                        color=AppColors.TEXT_LIGHT,
                    ),
                )
                scores_row.append(chip)

            round_controls.append(
                ft.Row(
                    wrap=True,
                    spacing=6,
                    run_spacing=6,
                    controls=scores_row,
                )
            )

            if r.is_tie:
                round_controls.append(
                    ft.Text(
                        f"⚡ Tie between: {', '.join(r.winners)} (Score: {r.highest_score}). Next round!",
                        size=12,
                        color=AppColors.COLUMBIA_BLUE,
                        italic=True,
                    )
                )
            round_controls.append(ft.Divider(color=AppColors.PRUSSIAN_BLUE, height=12))

        self.scoreboard_column.controls = round_controls

        # Winner banner
        self.status_banner.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, color=AppColors.SAFFRON, size=24),
                ft.Text(
                    f"Champion: {tournament.champion} with score {tournament.final_score}!",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.SAFFRON,
                ),
            ],
        )

        # Restore roll button
        self.roll_button.disabled = False
        self.roll_button.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.CASINO_ROUNDED, color=AppColors.OXFORD_BLUE),
                ft.Text("Roll Dice", size=18, weight=ft.FontWeight.BOLD, color=AppColors.OXFORD_BLUE),
            ],
        )
        self.is_rolling = False
        self.app_page.update()
