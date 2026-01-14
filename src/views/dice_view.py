import random
import time
import threading
import flet as ft
from views.base_view import BaseView
from utils.constants import AppColors


class DiceView(BaseView):
    def build(self):
        # Dice game interface
        game_title = ft.Text(
            "Dice Game",
            color=AppColors.SAFFRON,
            size=40,
            weight=ft.FontWeight.BOLD
        )

        self.players_input = ft.TextField(
            bgcolor=AppColors.PRUSSIAN_BLUE,
            multiline=True,
            width=440,
            height=450,
            label='Write players (one per line)',
            color=AppColors.COLUMBIA_BLUE,
            border_radius=20,
        )

        self.result_text = ft.Text(
            size=30,
            color=AppColors.SAFFRON,
        )

        # Dice container
        self.dice_container = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        roll_button = ft.ElevatedButton(
            content=ft.Text("Roll Dice", size=24),
            bgcolor=AppColors.CERULEAN,
            color=AppColors.COLUMBIA_BLUE,
            width=275,
            height=80,
            on_click=self.roll_dice
        )

        input_section = ft.Column([
            ft.Container(
                content=game_title,
                width=500,
                height=100,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=self.players_input,
                width=500,
                height=470,
                alignment=ft.alignment.center
            ),
            ft.Container(
                content=roll_button,
                width=500,
                height=150,
                alignment=ft.alignment.center,
                # Add some top margin for better spacing
                margin=ft.margin.only(top=10),
            )
        ], alignment=ft.MainAxisAlignment.CENTER)  # Center align the column contents

        dice_section = ft.Column([
            ft.Container(
                content=self.dice_container,
                alignment=ft.alignment.center,
                width=700,
                height=350,
            ),
            ft.Container(
                content=self.result_text,
                alignment=ft.alignment.center,
                width=700,
                height=350,
            )
        ])

        # Game container
        game = ft.Container(
            content=dice_section,
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

    def roll_dice(self, _):  # Using underscore to indicate unused parameter
        players_text = self.players_input.value
        if not players_text:
            dlg = ft.AlertDialog(title=ft.Text("Please enter players first"))
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            return

        players = players_text.splitlines()

        # Create dice visuals
        self.dice_container.controls = []
        for _ in range(2):
            self.dice_container.controls.append(
                ft.Container(
                    width=100,
                    height=100,
                    bgcolor=AppColors.COLUMBIA_BLUE,
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Text("?", size=40, color=AppColors.OXFORD_BLUE),
                )
            )
        self.page.update()

        # Show progress bar
        self.page.splash = ft.ProgressBar()
        self.page.update()

        # Function to animate dice and show results
        def dice_game_action():
            # Animate the dice first (simulate)
            for _ in range(10):
                # In a separate thread we cannot animate directly,
                # so this part is simulated
                time.sleep(0.1)

            # Play the dice game
            scores = {}
            winners = []
            current_players = players.copy()
            final_dice1 = 1  # Initialize with default values
            final_dice2 = 1  # Initialize with default values
            result_text = ""

            while True:
                scores = {}
                for player in current_players:
                    dice1 = random.randint(1, 6)
                    dice2 = random.randint(1, 6)
                    total = dice1 + dice2
                    scores[player] = total

                    # Last player for final dice values
                    if player == current_players[-1]:
                        final_dice1 = dice1
                        final_dice2 = dice2

                max_value = max(scores.values())
                winners = [player for player,
                           value in scores.items() if value == max_value]

                result_text += "Round results:\n"
                for player, score in scores.items():
                    result_text += f"{player}: {score}\n"

                if len(winners) == 1:
                    break

                result_text += f"\nTie between: {', '.join(winners)}\nStarting another round...\n\n"
                current_players = winners

            result_text += f"\nWinner: {winners[0]} with a score of {max_value}!"
            final_winner = winners[0]
            final_score = max_value

            # Schedule the UI update in the main thread
            def update_ui():
                # Update the dice with final values
                self.dice_container.controls[0].content = ft.Text(
                    str(final_dice1), size=40, color=AppColors.OXFORD_BLUE)
                self.dice_container.controls[1].content = ft.Text(
                    str(final_dice2), size=40, color=AppColors.OXFORD_BLUE)

                # Update result text
                self.result_text.value = result_text
                self.page.splash = None

                # Show a dialog with the winner
                dlg = ft.AlertDialog(
                    title=ft.Text("We have a winner!"),
                    content=ft.Column([
                        ft.Text("The winner is:", size=18),
                        ft.Text(f"{final_winner}", size=24,
                                color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            f"with a score of {final_score}", size=18)
                    ],
                        tight=True,
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER),
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
                # Alternative: execute directly
                update_ui()

        # Execute in a separate thread to not block the UI
        threading.Thread(target=dice_game_action).start()
