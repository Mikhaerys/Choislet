import math
import time
import random
import threading
import flet as ft
from views.base_view import BaseView
from utils.constants import AppColors


class CoinView(BaseView):
    def build(self):
        # Coin flip interface
        game_title = ft.Text(
            "Coin Flip",
            color=AppColors.SAFFRON,
            size=40,
            weight=ft.FontWeight.BOLD
        )

        self.head_input = ft.TextField(
            bgcolor=AppColors.PRUSSIAN_BLUE,
            label='Heads option',
            color=AppColors.COLUMBIA_BLUE,
            border_radius=20,
            width=440,
        )

        self.tail_input = ft.TextField(
            bgcolor=AppColors.PRUSSIAN_BLUE,
            label='Tails option',
            color=AppColors.COLUMBIA_BLUE,
            border_radius=20,
            width=440,
        )

        self.result_text = ft.Text(
            size=30,
            color=AppColors.SAFFRON,
        )

        # Coin animation container
        self.coin_container = ft.Container(
            width=300,
            height=300,
            border_radius=150,
            bgcolor=AppColors.SAFFRON,
            alignment=ft.alignment.center,
            content=ft.Text("FLIP", size=40, color=AppColors.OXFORD_BLUE),
            animate=ft.animation.Animation(500, ft.AnimationCurve.BOUNCE_OUT),
        )

        flip_button = ft.ElevatedButton(
            content=ft.Text("Flip Coin", size=24),
            bgcolor=AppColors.CERULEAN,
            color=AppColors.COLUMBIA_BLUE,
            width=275,
            height=80,
            on_click=self.flip_coin
        )

        coin_section = ft.Column([
            ft.Container(
                content=self.coin_container,
                alignment=ft.alignment.center,
                width=700,
                height=350,
            ),
            ft.Container(
                content=self.result_text,
                alignment=ft.alignment.center,
                width=700,
                height=100,
            )
        ])

        input_section = ft.Column([
            ft.Container(
                content=game_title,
                width=500,
                height=100,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=ft.Column(
                    [self.head_input, self.tail_input], spacing=20),
                width=500,
                height=300,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=flip_button,
                width=500,
                height=150,
                alignment=ft.alignment.center,
                # Add some top margin for better spacing
                margin=ft.margin.only(top=10),
            )
        ], alignment=ft.MainAxisAlignment.CENTER)  # Center align the column contents

        # Game container
        game = ft.Container(
            content=coin_section,
            width=700,
            height=758,
            alignment=ft.alignment.center,
        )

        user_input = ft.Container(
            content=input_section,
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

    def flip_coin(self, _):  # Using underscore to indicate unused parameter
        head = self.head_input.value or "Heads"
        tail = self.tail_input.value or "Tails"

        # Animate the coin flip
        self.coin_container.rotate = ft.transform.Rotate(
            0, alignment=ft.alignment.center)
        self.page.update()

        # First flip animation
        self.coin_container.rotate = ft.transform.Rotate(
            angle=2 * math.pi,
            alignment=ft.alignment.center,
        )
        self.page.update()

        # Use a progress bar to indicate that something is happening
        self.page.splash = ft.ProgressBar()
        self.page.update()

        # Schedule the delayed action using threading
        def delayed_action():
            # Simulate the waiting time for the animation
            time.sleep(0.8)

            # Determine the result
            result = random.choice([head, tail])
            side = "HEADS" if result == head else "TAILS"

            # Schedule the UI update in the main thread
            def update_ui():
                self.coin_container.content = ft.Text(
                    side, size=30, color=AppColors.OXFORD_BLUE)
                self.result_text.value = f"Result: {result}"
                self.page.splash = None

                # Create a more visible dialog to show the result
                dlg = ft.AlertDialog(
                    title=ft.Text("Coin Result!"),
                    content=ft.Text(
                        f"The result is: {result}", size=24, color=ft.Colors.GREEN),
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
            if hasattr(self.page, 'add_future'):  # Check if the method exists
                self.page.add_future(update_ui)
            else:
                # Alternative: execute directly (less ideal)
                update_ui()

        # Execute the delayed action in a separate thread
        threading.Thread(target=delayed_action).start()
