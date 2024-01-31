import random
import flet as ft


def main(page: ft.Page):
    page.title = "Choislet"
    page.window_width = 1280
    page.window_height = 720
    page.window_resizable = False
    page.padding = 0

    # Colors
    oxford_blue = "#10192c"
    prussian_blue = "#1e3b5c"
    saffron = "#fec965"
    columbia_blue = "#d6efff"
    cerulean = "#1d7d9e"

    items_nav = [
        ft.Container(width=50, height=50, border=ft.border.all(),
                     margin=ft.margin.only(top=20, left=15, right=15, bottom=0)),
        ft.Container(width=50, height=50, border=ft.border.all(),
                     margin=ft.margin.only(top=20, left=15, right=15, bottom=0)),
        ft.Container(width=50, height=50, border=ft.border.all(),
                     margin=ft.margin.only(top=20, left=15, right=15, bottom=0)),
        ft.Container(width=50, height=50, border=ft.border.all(),
                     margin=ft.margin.only(top=20, left=15, right=15, bottom=0))
    ]

    nav = ft.Container(content=ft.Column(items_nav, spacing=0), width=80,
                       height=720, bgcolor=prussian_blue, alignment=ft.alignment.top_center)
    game = ft.Container(width=700, height=720, border=ft.border.all())
    user_input = ft.Container(width=500, height=720, border=ft.border.all())

    row = ft.Row(spacing=0, controls=[nav, game, user_input])

    container = ft.Container(row, width=1280, height=720,
                             bgcolor=oxford_blue, alignment=ft.alignment.center_left)

    page.add(container)


ft.app(target=main)


def roulette_winner(text):
    options = text.splitlines()
    scores = {key: 0 for key in options}

    while True:
        winner = random.choice(options)
        scores[winner] += 1
        if scores[winner] == 3:
            return winner


def flip_coin(head, tail):
    return random.choice([head, tail])


def dice_game(text):
    options = text.splitlines()
    scores = {key: 0 for key in options}

    while True:
        for option in options:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            scores[option] = dice1 + dice2

        max_value = max(scores.values())
        winners = [jugador for jugador,
                   value in scores.items() if value == max_value]

        if len(winners) == 1:
            return winners, max_value

        options = winners
