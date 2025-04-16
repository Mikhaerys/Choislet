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
        self.division_angles = []
        self.final_position = 0
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

        # Store division angles for determining winner later
        self.division_angles = []

        for _, candidate in enumerate(self.candidates):
            # Add colored sector
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

            # Add sector border
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

            text_angle = division_start + (division_angle / 2)
            radius = 290
            text_x = 300 + radius * math.cos(text_angle)
            text_y = 300 + radius * math.sin(text_angle)

            # Calculate the rotation so that the text points towards the center
            # Invert the angle and add 90 degrees for correct orientation
            text_rotation = text_angle + math.pi  # Rotate 180° to point to the center

            # Store the start and end angles for this candidate
            self.division_angles.append({
                'candidate': candidate,
                'start': division_start,
                'end': division_start + division_angle
            })

            # Add the text
            self.roulette_divisions.append(
                cv.Text(
                    text=candidate,
                    x=text_x,
                    y=text_y,
                    style=ft.TextStyle(
                        font_family="Roboto",
                        weight=ft.FontWeight.BOLD,
                        size=10,
                        color=ft.Colors.BLACK,
                    ),
                    text_align=ft.TextAlign.CENTER,
                    rotate=text_rotation,
                )
            )

            division_start += division_angle
            color_index = (color_index + 1) % number_of_colors

        # Center circle
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

    def determine_winner_from_position(self, position):
        # Need to normalize angle for comparison (0 to 2π)
        normalized_position = position % (2 * math.pi)

        # Find which division contains the position
        for division in self.division_angles:
            if division['start'] <= normalized_position < division['end']:
                return division['candidate']

        # Edge case: if position is exactly at 2π, it should match the first division
        if abs(normalized_position - (2 * math.pi)) < 0.0001:
            for division in self.division_angles:
                if division['start'] == 0:
                    return division['candidate']

        return self.candidates[0]  # Fallback to first candidate

    def spin_roulette(self, _):  # Using underscore to indicate unused parameter
        if not self.candidates or self.candidates == ["No candidates"]:
            dlg = ft.AlertDialog(title=ft.Text(
                "Please enter candidates first"))
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            return

        # Reset the roulette to angle 0 before spinning to avoid cumulative errors
        current_container = self.roulette_stack[0]

        # Generate random number of rotations (between 5-8) for visual effect
        total_rotations = random.randint(5, 8)

        # Generate random final angle in radians (this determines the winner)
        final_angle_rad = random.uniform(0, 2*math.pi)

        # Total rotation angle = complete rotations + final position
        total_angle = (total_rotations * 2*math.pi) + final_angle_rad

        # The arrow points at 0 radians (right), and the wheel rotates counterclockwise
        # So we need to calculate the final position for determining the winner
        self.final_position = (2*math.pi) - (final_angle_rad % (2*math.pi))

        current_container.animate_rotation = ft.animation.Animation(50)

        current_container.rotate = None
        self.page.update()

        # Small delay to ensure the above update is processed
        time.sleep(0.05)

        # Now set up the new animation with the calculated angle
        current_container.rotate = ft.transform.Rotate(
            angle=total_angle,
            alignment=ft.alignment.center
        )

        # Apply animation settings - longer duration for better visual effect
        current_container.animate_rotation = ft.animation.Animation(
            5000, ft.AnimationCurve.DECELERATE
        )

        # Update UI to start the animation
        self.page.update()

        # Show progress indicator
        self.page.splash = ft.ProgressBar()
        self.page.update()

        # Schedule the delayed action using threading to announce winner when animation completes
        def delayed_action():
            # Wait for the animation to complete
            # Slightly longer than animation to ensure it completes
            time.sleep(5.5)

            # Pre-determine the winner based on final position
            winner = self.determine_winner_from_position(self.final_position)

            def update_ui():
                self.text_winner.value = f"Winner: {winner}"
                self.page.splash = None

                # Create a dialog to announce the winner
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

            # Execute UI update
            if hasattr(self.page, 'add_future'):
                self.page.add_future(update_ui)
            else:
                update_ui()

        # Execute in a separate thread
        threading.Thread(target=delayed_action).start()
