import math
import random
import time
import threading
import flet as ft
import flet.canvas as cv
from views.base_view import BaseView
from utils.constants import AppColors


class RouletteView(BaseView):
    def __init__(self, page: ft.Page):
        self.candidates = ["No candidates"]
        self.roulette_divisions = []
        self.text_winner = ft.Text(color=AppColors.SAFFRON, size=30)
        super().__init__(page)

    def build(self):
        # Roulette interface
        self.roulette_canva = cv.Canvas(
            self.roulette_divisions, width=600, height=600)
        triangle = [
            cv.Path(
                [
                    cv.Path.MoveTo(600, 280),
                    cv.Path.LineTo(600, 320),
                    cv.Path.LineTo(580, 300)
                ],
                paint=ft.Paint(color=ft.Colors.RED)
            )
        ]
        self.roulette_stack = [
            ft.Container(
                content=self.roulette_canva,
                width=600, height=600,
                rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
                animate_rotation=ft.animation.Animation(
                    5000, ft.AnimationCurve.DECELERATE)
            ),
            cv.Canvas(triangle, width=600, height=600)
        ]

        roulette_section = [
            ft.Container(
                content=ft.Stack(self.roulette_stack),
                width=700, height=600,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=self.text_winner,
                width=700, height=100,
                alignment=ft.alignment.center
            )
        ]

        # User input interface
        game_title = ft.Text(
            "Roulette",
            color=AppColors.SAFFRON,
            size=40,
            weight=ft.FontWeight.BOLD
        )

        self.text_input = ft.TextField(
            bgcolor=AppColors.PRUSSIAN_BLUE,
            multiline=True,
            width=440,
            height=450,
            label='Write the candidates',
            color=AppColors.COLUMBIA_BLUE,
            border_radius=20,
            on_change=self.draw_roulette
        )

        spin_button = ft.ElevatedButton(
            content=ft.Text("Spin", size=24),
            bgcolor=AppColors.CERULEAN,
            color=AppColors.COLUMBIA_BLUE,
            width=275,
            height=80,
            on_click=self.spin_roulette
        )

        items_user_input = [
            ft.Container(
                content=game_title,
                width=500,
                height=100,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=self.text_input,
                width=500,
                height=470,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=spin_button,
                width=500,
                height=150,
                alignment=ft.alignment.center,
                # Add some top margin for better spacing
                margin=ft.margin.only(top=10),
            )
        ]

        # User input column with centered elements
        user_input_column = ft.Column(
            items_user_input,
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER  # Center align elements vertically
        )

        # Game container
        game = ft.Container(
            content=ft.Column(roulette_section, spacing=0),
            width=700,
            height=758,
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=10)
        )

        user_input = ft.Container(
            content=user_input_column,
            width=500,
            height=758,
        )

        row = ft.Row(spacing=0, controls=[game, user_input])

        container = ft.Container(
            content=row,
            width=1200,
            height=758,
            bgcolor=AppColors.OXFORD_BLUE,
            visible=self.visible
        )

        return container

    def draw_roulette(self, e):
        self.candidates = e.control.value.splitlines()
        if not self.candidates:
            return

        self.roulette_divisions = []
        number_of_colors = len(AppColors.ROULETTE_COLORS)
        color_index = 0
        division_start = 0
        division_angle = (2*math.pi) / len(self.candidates)

        for _ in self.candidates:
            self.roulette_divisions.append(
                cv.Path(
                    [
                        cv.Path.Arc(
                            0, 0, 600, 600,
                            division_start, division_angle
                        ),
                        cv.Path.LineTo(300, 300),
                    ],
                    paint=ft.Paint(
                        color=AppColors.ROULETTE_COLORS[color_index])
                )
            )
            self.roulette_divisions.append(
                cv.Path(
                    [
                        cv.Path.Arc(
                            0, 0, 600, 600,
                            division_start, division_angle
                        ),
                        cv.Path.LineTo(300, 300),
                        cv.Path.Close()
                    ],
                    paint=ft.Paint(style=ft.PaintingStyle.STROKE)
                )
            )

            division_start += division_angle
            color_index = (color_index + 1) % number_of_colors

        self.roulette_divisions.append(
            cv.Circle(300, 300, 20, ft.Paint(color=ft.Colors.WHITE))
        )

        # Update the canvas with new divisions
        self.roulette_canva.shapes = self.roulette_divisions
        self.page.update()

    def find_winner(self):
        scores = {key: 0 for key in self.candidates}

        while True:
            winner = random.choice(self.candidates)
            scores[winner] += 1
            if scores[winner] == 3:
                return winner

    def spin_roulette(self, _):  # Using underscore to indicate unused parameter
        if not self.candidates or self.candidates == ["No candidates"]:
            dlg = ft.AlertDialog(title=ft.Text(
                "Please enter candidates first"))
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            return

        angle_winner = math.radians(random.randint(1, 306))
        self.roulette_stack[0].rotate.angle += (5 * math.pi) + angle_winner
        self.page.update()

        # Use a progress bar to indicate that something is happening
        self.page.splash = ft.ProgressBar()
        self.page.update()

        # Schedule the delayed action using threading
        def delayed_action():
            # Simulate the waiting time for the animation
            time.sleep(5)

            # Find the winner
            winner = self.find_winner()

            # Update the winner text in the existing control
            def update_ui():
                self.text_winner.value = f"Winner: {winner}"
                self.page.splash = None

                # Create a more visible dialog
                dlg = ft.AlertDialog(
                    title=ft.Text("We have a winner!"),
                    content=ft.Text(
                        f"The winner is: {winner}", size=24, color=ft.Colors.GREEN),
                    actions=[
                        ft.TextButton(
                            "Accept", on_click=lambda _: close_dlg(dlg))
                    ],
                )

                def close_dlg(dialog):
                    dialog.open = False
                    self.page.update()

                self.page.dialog = dlg
                dlg.open = True
                self.page.update()

            # We need to execute the UI update in the main thread
            if hasattr(self.page, 'add_future'):  # Check if the method exists
                self.page.add_future(update_ui)
            else:
                # Alternative: execute directly
                update_ui()

        # Execute the delayed action in a separate thread
        threading.Thread(target=delayed_action).start()
