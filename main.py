import random
import flet as ft


def main(page: ft.Page):
    page.title = "Choislet"
    page.window_width = 1295
    page.window_height = 758
    page.window_resizable = False
    page.padding = 0

    # Colors
    oxford_blue = "#10192c"
    prussian_blue = "#1e3b5c"
    saffron = "#fec965"
    columbia_blue = "#d6efff"
    cerulean = "#1d7d9e"

    app_icon = ft.Image(
        src="./Icons/Choislet.png", fit=ft.ImageFit.CONTAIN,
        width=50, height=50
    )
    roulette_icon = ft.Image(
        src="./Icons/ruleta.png", fit=ft.ImageFit.CONTAIN,
        width=50, height=50
    )
    coin_icon = ft.Image(
        src="./Icons/moneda.png", fit=ft.ImageFit.CONTAIN,
        width=50, height=50
    )
    dice_icon = ft.Image(
        src="./Icons/dado.png", fit=ft.ImageFit.CONTAIN,
        width=50, height=50
    )

    items_nav = [
        ft.Container(
            content=app_icon,
            image_src="/Icons/ruleta.png",
            width=50, height=50,
            margin=ft.margin.only(top=20, left=15, right=15),
            border=ft.border.all()
        ),
        ft.Container(
            content=roulette_icon,
            width=50, height=50,
            margin=ft.margin.only(top=20, left=15, right=15),
            border=ft.border.all()
        ),
        ft.Container(
            content=coin_icon,
            width=50, height=50,
            margin=ft.margin.only(top=20, left=15, right=15),
            border=ft.border.all()
        ),
        ft.Container(
            content=dice_icon,
            width=50, height=50,
            margin=ft.margin.only(top=20, left=15, right=15),
            border=ft.border.all()
        )
    ]

    game_title = ft.Text("Roulette", color=saffron,
                         size=40, weight=ft.FontWeight.BOLD)

    text_input = ft.TextField(
        bgcolor=prussian_blue,
        multiline=True, width=440, height=450,
        label='Escribe las opciones',
        color=columbia_blue,
        border_radius=20
    )

    start_button = ft.ElevatedButton(
        content=ft.Text("Spin", size=24),
        bgcolor=cerulean,
        color=columbia_blue,
        width=275,
        height=80
    )

    items_user_input = [
        ft.Container(content=game_title, width=500, height=100,
                     alignment=ft.alignment.center, border=ft.border.all()),
        ft.Container(content=text_input, width=500,
                     height=470, alignment=ft.alignment.center, border=ft.border.all()),
        ft.Container(content=start_button, width=500, height=150,
                     alignment=ft.alignment.center, border=ft.border.all())
    ]

    nav = ft.Container(
        content=ft.Column(items_nav, spacing=0),
        width=80, height=720, bgcolor=prussian_blue,
        alignment=ft.alignment.top_center, border=ft.border.all()
    )
    game = ft.Container(
        width=700, height=720, border=ft.border.all()
    )
    user_input = ft.Container(
        content=ft.Column(items_user_input, spacing=0),
        width=500, height=720, border=ft.border.all()
    )

    row = ft.Row(spacing=0, controls=[nav, game, user_input])

    container = ft.Container(
        content=row, width=1280, height=720,
        bgcolor=oxford_blue, alignment=ft.alignment.center_left
    )

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
