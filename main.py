import math
import time
import random
import flet as ft
import flet.canvas as cv

# -------------------------------- variables --------------------------------
OXFORD_BLUE = "#10192c"
PRUSSIAN_BLUE = "#1e3b5c"
SAFFRON = "#fec965"
COLUMBIA_BLUE = "#d6efff"
CERULEAN = "#11495C"
roulette_colors = ["#fdffb6", "#caffbf", "#9bf6ff", "#a0c4ff", "#ffc6ff",]

candidates = ["No candidates"]
roulette_divisions = []

# -------------------------------- App --------------------------------


def main(page: ft.Page):
    page.title = "Choislet"
    page.window_width = 1295
    page.window_height = 758
    page.window_resizable = False
    page.padding = 0

    # ------------------------------- Functions ---------------------------------
    def draw_roullete(e):
        global candidates
        candidates = e.control.value.splitlines()
        number_of_colors = len(roulette_colors)
        color_index = 0
        division_start = 0
        division_angle = (2*math.pi) / len(candidates)

        for _ in candidates:
            roulette_divisions.append(
                cv.Path(
                    [
                        cv.Path.Arc(
                            0, 0, 600, 600,
                            division_start, division_angle
                        ),
                        cv.Path.LineTo(300, 300),
                    ],
                    paint=ft.Paint(color=roulette_colors[color_index])
                )
            )
            roulette_divisions.append(
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

        roulette_divisions.append(
            cv.Circle(300, 300, 20, ft.Paint(color=ft.colors.WHITE))
        )
        page.update()

    def roulette_winner():
        scores = {key: 0 for key in candidates}

        while True:
            winner = random.choice(candidates)
            scores[winner] += 1
            if scores[winner] == 3:
                return winner

    def spin_roulette(e):
        angle_winner = math.radians(random.randint(1, 306))
        roulette_stack[0].rotate.angle += (5 * math.pi) + angle_winner
        page.update()

        time.sleep(5)

        winner = roulette_winner()
        text_winner.value = f"Winner: {winner}"
        dlg = ft.AlertDialog(title=ft.Text(f"The winner is {winner}"))
        page.dialog = dlg
        dlg.open = True

        page.update()

    def flip_coin(head, tail):
        return random.choice([head, tail])

    def dice_game(text):
        global candidates
        candidates = text.splitlines()
        scores = {key: 0 for key in candidates}

        while True:
            for candidate in candidates:
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                scores[candidate] = dice1 + dice2

            max_value = max(scores.values())
            winners = [jugador for jugador,
                       value in scores.items() if value == max_value]

            if len(winners) == 1:
                return winners, max_value

            candidates = winners
    # ------------------------------ Icons of Nav -------------------------------
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
            margin=ft.margin.only(top=20, left=15, right=15)
        ),
        ft.Container(
            content=roulette_icon,
            width=50, height=50,
            margin=ft.margin.only(top=20, left=15, right=15)
        ),
        ft.Container(
            content=coin_icon,
            width=50, height=50,
            margin=ft.margin.only(top=20, left=15, right=15)
        ),
        ft.Container(
            content=dice_icon,
            width=50, height=50,
            margin=ft.margin.only(top=20, left=15, right=15)
        )
    ]

    # ---------------------------- Roullete interface ----------------------------
    text_winner = ft.Text(color=SAFFRON, size=30)
    roulette_canva = cv.Canvas(roulette_divisions, width=600, height=600)
    triangle = [
        cv.Path(
            [
                cv.Path.MoveTo(600, 280),
                cv.Path.LineTo(600, 320),
                cv.Path.LineTo(580, 300)
            ],
            paint=ft.Paint(color=ft.colors.RED)
        )
    ]
    roulette_stack = [
        ft.Container(
            content=roulette_canva,
            width=600, height=600,
            rotate=ft.transform.Rotate(0, alignment=ft.alignment.center),
            animate_rotation=ft.animation.Animation(
                5000, ft.AnimationCurve.DECELERATE)),
        cv.Canvas(triangle, width=600, height=600)
    ]
    roulette_section = [
        ft.Container(
            content=ft.Stack(roulette_stack),
            width=700, height=600,
            alignment=ft.alignment.center
        ),
        ft.Container(
            content=text_winner,
            width=700, height=100,
            alignment=ft.alignment.center
        )
    ]

    # ---------------------------- User input interface ----------------------------
    game_title = ft.Text("Roulette", color=SAFFRON,
                         size=40, weight=ft.FontWeight.BOLD)

    text_input = ft.TextField(
        bgcolor=PRUSSIAN_BLUE,
        multiline=True, width=440, height=450,
        label='Write the candidates',
        color=COLUMBIA_BLUE,
        border_radius=20,
        on_change=draw_roullete
    )

    spin_button = ft.ElevatedButton(
        content=ft.Text("Spin", size=24),
        bgcolor=CERULEAN,
        color=COLUMBIA_BLUE,
        width=275,
        height=80,
        on_click=spin_roulette
    )

    items_user_input = [
        ft.Container(content=game_title, width=500, height=100,
                     alignment=ft.alignment.center),
        ft.Container(content=text_input, width=500,
                     height=470, alignment=ft.alignment.center),
        ft.Container(content=spin_button, width=500, height=150,
                     alignment=ft.alignment.center)
    ]

    # ---------------------------- Sections of the app ----------------------------
    nav = ft.Container(
        content=ft.Column(items_nav, spacing=0),
        width=80, height=720, bgcolor=PRUSSIAN_BLUE,
        alignment=ft.alignment.top_center
    )
    game = ft.Container(
        content=ft.Column(roulette_section, spacing=0),
        width=700, height=720,
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=10)
    )
    user_input = ft.Container(
        content=ft.Column(items_user_input, spacing=0),
        width=500, height=720
    )

    row = ft.Row(spacing=0, controls=[nav, game, user_input])

    # ----------------------------  Main Container ----------------------------
    container = ft.Container(
        content=row, width=1280, height=720,
        bgcolor=OXFORD_BLUE, alignment=ft.alignment.center_left
    )

    page.add(container)


ft.app(target=main)
