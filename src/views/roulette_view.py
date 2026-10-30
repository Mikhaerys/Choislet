"""Roulette view with modern canvas rendering and smooth async animations."""

from __future__ import annotations
import asyncio
import math
import flet as ft
import flet.canvas as cv
from src.views.base_view import BaseView
from src.utils.constants import AppColors, get_text_field_border
from src.logic.roulette_logic import (
    parse_candidates,
    calculate_sectors,
    determine_winner,
    generate_spin_target,
    RouletteSector,
)


class RouletteView(BaseView):
    def __init__(self, page: ft.Page):
        self.raw_text_default = "Pizza\nTacos\nBurgers\nSushi\nPasta\nSalad"
        self.candidates: list[str] = parse_candidates(self.raw_text_default)
        self.sectors: list[RouletteSector] = calculate_sectors(self.candidates)
        self.current_rotation: float = 0.0
        self.is_spinning: bool = False
        self._spin_event: asyncio.Event | None = None

        self._app_page_ref = page
        self.canvas_size = self._get_responsive_size()
        self.center = self.canvas_size / 2.0
        self.wheel_radius = self.canvas_size * 0.46

        self.is_web = getattr(page, "web", False)
        self.spin_duration_ms = 5200 if self.is_web else 4000
        self.spin_curve = ft.AnimationCurve.EASE_OUT_CUBIC

        super().__init__(page)

    def _get_responsive_size(self) -> float:
        try:
            page = getattr(self, "app_page", None) or getattr(self, "_app_page_ref", None)
            pw = getattr(page, "width", None)
            if pw is not None and isinstance(pw, (int, float)) and pw > 0:
                if pw >= 992:
                    return 500.0
                available = float(pw) - 112.0
                return max(280.0, min(500.0, available))
        except Exception:
            pass
        return 500.0

    def _create_pointer_shapes(self) -> list[cv.Shape]:
        arrow_w = max(20.0, self.canvas_size * 0.064)
        arrow_h = max(24.0, self.canvas_size * 0.064)
        return [
            cv.Path(
                [
                    cv.Path.MoveTo(self.canvas_size, self.center - (arrow_h / 2.0)),
                    cv.Path.LineTo(self.canvas_size, self.center + (arrow_h / 2.0)),
                    cv.Path.LineTo(self.canvas_size - arrow_w, self.center),
                    cv.Path.Close(),
                ],
                paint=ft.Paint(color=AppColors.SAFFRON, style=ft.PaintingStyle.FILL),
            ),
            cv.Path(
                [
                    cv.Path.MoveTo(self.canvas_size, self.center - (arrow_h / 2.0)),
                    cv.Path.LineTo(self.canvas_size, self.center + (arrow_h / 2.0)),
                    cv.Path.LineTo(self.canvas_size - arrow_w, self.center),
                    cv.Path.Close(),
                ],
                paint=ft.Paint(color=AppColors.OXFORD_BLUE, stroke_width=2, style=ft.PaintingStyle.STROKE),
            ),
        ]

    def _apply_size(self, size: float) -> None:
        self.canvas_size = size
        self.center = self.canvas_size / 2.0
        self.wheel_radius = self.canvas_size * 0.46

        self.wheel_container.width = self.canvas_size
        self.wheel_container.height = self.canvas_size

        self.pointer_canvas.shapes = self._create_pointer_shapes()
        self.pointer_canvas.width = self.canvas_size
        self.pointer_canvas.height = self.canvas_size

        self.wheel_stack.width = self.canvas_size
        self.wheel_stack.height = self.canvas_size

        self._render_wheel()

    def on_resize(self) -> None:
        if self.is_spinning:
            return
        new_size = self._get_responsive_size()
        if abs(new_size - self.canvas_size) > 10:
            self._apply_size(new_size)
            try:
                self.app_page.update()
            except Exception:
                pass

    def _on_animation_end(self, _: ft.ControlEvent) -> None:
        if self._spin_event and not self._spin_event.is_set():
            self._spin_event.set()

    def init_view(self) -> ft.Control:
        # Canvas control holding wheel shapes
        self.wheel_canvas = cv.Canvas(
            shapes=[],
            width=self.canvas_size,
            height=self.canvas_size,
        )

        # Container for the rotating wheel
        self.wheel_container = ft.Container(
            content=self.wheel_canvas,
            width=self.canvas_size,
            height=self.canvas_size,
            alignment=ft.Alignment.CENTER,
            rotate=0.0,
            animate_rotation=ft.Animation(self.spin_duration_ms, self.spin_curve),
            on_animation_end=self._on_animation_end,
        )

        # Fixed pointer arrow canvas on top
        self.pointer_canvas = cv.Canvas(
            shapes=self._create_pointer_shapes(),
            width=self.canvas_size,
            height=self.canvas_size,
        )

        self.wheel_stack = ft.Stack(
            controls=[
                self.wheel_container,
                self.pointer_canvas,
            ],
            width=self.canvas_size,
            height=self.canvas_size,
            alignment=ft.Alignment.CENTER,
        )

        # Result badge
        self.result_badge = ft.Container(
            content=ft.Text(
                "Spin the wheel to make a choice!",
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

        left_section = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                self.wheel_stack,
                self.result_badge,
            ],
        )

        # User input controls
        self.candidates_input = ft.TextField(
            value=self.raw_text_default,
            multiline=True,
            min_lines=8,
            max_lines=12,
            label="Candidates (one per line)",
            label_style=ft.TextStyle(color=AppColors.COLUMBIA_BLUE),
            color=AppColors.TEXT_LIGHT,
            bgcolor=AppColors.CARD_BG,
            border=get_text_field_border(12),
            cursor_color=AppColors.SAFFRON,
            on_change=self._on_input_changed,
        )

        self.spin_button = ft.FilledButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=AppColors.OXFORD_BLUE),
                    ft.Text("Spin Wheel", size=18, weight=ft.FontWeight.BOLD, color=AppColors.OXFORD_BLUE),
                ],
            ),
            style=ft.ButtonStyle(
                bgcolor=AppColors.SAFFRON,
                padding=ft.Padding(left=24, right=24, top=16, bottom=16),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            width=280,
            height=54,
            on_click=self._spin_click,
        )

        clear_button = ft.OutlinedButton(
            content=ft.Text("Clear", color=AppColors.TEXT_MUTED),
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, AppColors.PRUSSIAN_BLUE),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self._clear_input,
        )

        preset_button = ft.OutlinedButton(
            content=ft.Text("Load Sample", color=AppColors.COLUMBIA_BLUE),
            style=ft.ButtonStyle(
                side=ft.BorderSide(1, AppColors.PRUSSIAN_BLUE),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=self._load_sample,
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
                        "Roulette Options",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.SAFFRON,
                    ),
                    ft.Text(
                        "Type or paste your options below. The wheel updates automatically.",
                        size=13,
                        color=AppColors.TEXT_MUTED,
                    ),
                    self.candidates_input,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[preset_button, clear_button],
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[self.spin_button],
                    ),
                ],
            ),
        )

        self._render_wheel()

        return ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=32,
            run_spacing=24,
            controls=[
                ft.Container(
                    col={"xs": 12, "sm": 12, "md": 12, "lg": 6, "xl": 6},
                    content=left_section,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(
                    col={"xs": 12, "sm": 12, "md": 12, "lg": 6, "xl": 5},
                    content=right_panel,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
        )

    def _render_wheel(self) -> None:
        shapes: list[cv.Shape] = []
        center = self.center
        r = self.wheel_radius
        d = r * 2.0
        x_left = center - r
        y_top = center - r

        if not self.candidates or not self.sectors:
            # Empty wheel placeholder
            shapes.append(
                cv.Circle(center, center, r, paint=ft.Paint(color=AppColors.CARD_BG, style=ft.PaintingStyle.FILL))
            )
            shapes.append(
                cv.Circle(
                    center,
                    center,
                    r,
                    paint=ft.Paint(color=AppColors.PRUSSIAN_BLUE, stroke_width=3, style=ft.PaintingStyle.STROKE),
                )
            )
            shapes.append(
                cv.Text(
                    x=center,
                    y=center,
                    value="Add candidates to start",
                    style=ft.TextStyle(size=16, color=AppColors.TEXT_MUTED, weight=ft.FontWeight.BOLD),
                    text_align=ft.TextAlign.CENTER,
                )
            )
            self.wheel_canvas = cv.Canvas(
                shapes=shapes,
                width=self.canvas_size,
                height=self.canvas_size,
            )
            self.wheel_container.content = self.wheel_canvas
            return

        num_colors = len(AppColors.ROULETTE_COLORS)
        num_candidates = len(self.candidates)

        font_scale = self.canvas_size / 500.0
        base_font = 13 if num_candidates <= 8 else (11 if num_candidates <= 14 else 9)
        font_size = max(8, int(base_font * font_scale))

        for s in self.sectors:
            color = AppColors.ROULETTE_COLORS[s.index % num_colors]

            # Wedge slice
            shapes.append(
                cv.Path(
                    [
                        cv.Path.Arc(x_left, y_top, d, d, s.start_angle, s.sweep_angle),
                        cv.Path.LineTo(center, center),
                        cv.Path.Close(),
                    ],
                    paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                )
            )

            # Wedge border
            shapes.append(
                cv.Path(
                    [
                        cv.Path.Arc(x_left, y_top, d, d, s.start_angle, s.sweep_angle),
                        cv.Path.LineTo(center, center),
                        cv.Path.Close(),
                    ],
                    paint=ft.Paint(color=AppColors.OXFORD_BLUE, stroke_width=1.5, style=ft.PaintingStyle.STROKE),
                )
            )

            # Label text
            mid_angle = s.start_angle + (s.sweep_angle / 2.0)
            text_distance = r * 0.65
            text_x = center + (text_distance * math.cos(mid_angle))
            text_y = center + (text_distance * math.sin(mid_angle))

            label = s.candidate
            if len(label) > 16:
                label = label[:14] + ".."

            shapes.append(
                cv.Text(
                    x=text_x,
                    y=text_y,
                    value=label,
                    style=ft.TextStyle(
                        weight=ft.FontWeight.BOLD,
                        size=font_size,
                        color=AppColors.OXFORD_BLUE,
                    ),
                    text_align=ft.TextAlign.CENTER,
                    rotate=mid_angle + math.pi,
                )
            )

        # Outer rim
        shapes.append(
            cv.Circle(
                center,
                center,
                r,
                paint=ft.Paint(color=AppColors.PRUSSIAN_BLUE, stroke_width=4, style=ft.PaintingStyle.STROKE),
            )
        )

        # Center hub
        hub_outer = max(16.0, self.canvas_size * 0.052)
        hub_inner = max(5.0, self.canvas_size * 0.016)
        shapes.append(
            cv.Circle(center, center, hub_outer, paint=ft.Paint(color=AppColors.OXFORD_BLUE, style=ft.PaintingStyle.FILL))
        )
        shapes.append(
            cv.Circle(
                center,
                center,
                hub_outer,
                paint=ft.Paint(color=AppColors.SAFFRON, stroke_width=2.5, style=ft.PaintingStyle.STROKE),
            )
        )
        shapes.append(
            cv.Circle(center, center, hub_inner, paint=ft.Paint(color=AppColors.SAFFRON, style=ft.PaintingStyle.FILL))
        )

        self.wheel_canvas = cv.Canvas(
            shapes=shapes,
            width=self.canvas_size,
            height=self.canvas_size,
        )
        self.wheel_container.content = self.wheel_canvas

    def _on_input_changed(self, e: ft.ControlEvent) -> None:
        if self.is_spinning:
            return
        self.candidates = parse_candidates(e.control.value)
        self.sectors = calculate_sectors(self.candidates)
        self._render_wheel()
        self.app_page.update()

    def _clear_input(self, _: ft.ControlEvent) -> None:
        if self.is_spinning:
            return
        self.candidates_input.value = ""
        self.candidates = []
        self.sectors = []
        self._render_wheel()
        self.app_page.update()

    def _load_sample(self, _: ft.ControlEvent) -> None:
        if self.is_spinning:
            return
        self.candidates_input.value = self.raw_text_default
        self.candidates = parse_candidates(self.raw_text_default)
        self.sectors = calculate_sectors(self.candidates)
        self._render_wheel()
        self.app_page.update()

    async def _spin_click(self, _: ft.ControlEvent) -> None:
        if self.is_spinning:
            return

        if not self.candidates:
            dlg = ft.AlertDialog(
                title=ft.Text("No Candidates"),
                content=ft.Text("Please enter at least one candidate before spinning the wheel."),
                actions=[ft.TextButton("OK", on_click=lambda _: self.app_page.close(dlg))],
            )
            self.app_page.open(dlg)
            return

        self.is_spinning = True
        self.spin_button.disabled = True
        self.spin_button.content = ft.ProgressRing(
            width=22,
            height=22,
            stroke_width=2.5,
            color=AppColors.OXFORD_BLUE,
        )
        self.result_badge.content = ft.Text(
            "Spinning... Let fate decide!",
            size=18,
            weight=ft.FontWeight.W_600,
            color=AppColors.COLUMBIA_BLUE,
            text_align=ft.TextAlign.CENTER,
        )
        self.app_page.update()

        # Calibrate rotation count according to platform
        is_web = getattr(self.app_page, "web", False)
        min_rot = 3 if is_web else 4
        max_rot = 5 if is_web else 6

        # Calculate spin destination
        spin_radians = generate_spin_target(min_rotations=min_rot, max_rotations=max_rot)
        new_rotation = self.current_rotation + spin_radians

        self._spin_event = asyncio.Event()

        # Trigger smooth rotation
        self.wheel_container.rotate = new_rotation
        self.app_page.update()

        # Wait for client animation to finish (with fallback timeout)
        try:
            await asyncio.wait_for(
                self._spin_event.wait(),
                timeout=(self.spin_duration_ms / 1000.0) + 0.3,
            )
        except asyncio.TimeoutError:
            pass

        winner = determine_winner(self.sectors, new_rotation)
        self.current_rotation = new_rotation

        # Present winner
        self.result_badge.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, color=AppColors.SAFFRON, size=24),
                ft.Text(
                    f"Winner: {winner}!",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.SAFFRON,
                ),
            ],
        )

        # Restore spin button
        self.spin_button.disabled = False
        self.spin_button.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=AppColors.OXFORD_BLUE),
                ft.Text("Spin Wheel", size=18, weight=ft.FontWeight.BOLD, color=AppColors.OXFORD_BLUE),
            ],
        )
        self.is_spinning = False
        self.app_page.update()
