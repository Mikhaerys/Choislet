import flet as ft
from views.roulette_view import RouletteView
from views.coin_view import CoinView
from views.dice_view import DiceView
from utils.constants import AppColors

# -------------------------------- App --------------------------------


class ChoisletApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.init_views()
        self.setup_navigation()
        self.show_default_view()

    def setup_page(self):
        self.page.title = "Choislet"
        self.page.window.width = 1295
        self.page.window.height = 758
        self.page.padding = 0

    def init_views(self):
        self.roulette_view = RouletteView(self.page)
        self.coin_view = CoinView(self.page)
        self.dice_view = DiceView(self.page)
        self.views = [self.roulette_view, self.coin_view, self.dice_view]

    def setup_navigation(self):
        # Icons for navigation
        app_icon = ft.Image(
            src="./Icons/Choislet.png",
            fit=ft.ImageFit.CONTAIN,
            width=50,
            height=50
        )

        roulette_icon = ft.Image(
            src="./Icons/ruleta.png",
            fit=ft.ImageFit.CONTAIN,
            width=50,
            height=50
        )

        coin_icon = ft.Image(
            src="./Icons/moneda.png",
            fit=ft.ImageFit.CONTAIN,
            width=50,
            height=50
        )

        dice_icon = ft.Image(
            src="./Icons/dado.png",
            fit=ft.ImageFit.CONTAIN,
            width=50,
            height=50
        )

        # Navigation buttons
        self.nav_buttons = [
            ft.Container(
                content=app_icon,
                width=50, height=50,
                margin=ft.margin.only(top=20, left=15, right=15),
                on_click=lambda _: self.switch_view(None)
            ),
            ft.Container(
                content=roulette_icon,
                width=50, height=50,
                margin=ft.margin.only(top=20, left=15, right=15),
                on_click=lambda _: self.switch_view(self.roulette_view)
            ),
            ft.Container(
                content=coin_icon,
                width=50, height=50,
                margin=ft.margin.only(top=20, left=15, right=15),
                on_click=lambda _: self.switch_view(self.coin_view)
            ),
            ft.Container(
                content=dice_icon,
                width=50, height=50,
                margin=ft.margin.only(top=20, left=15, right=15),
                on_click=lambda _: self.switch_view(self.dice_view)
            )
        ]

        # Make containers clickable
        for button in self.nav_buttons:
            button.on_hover = self.on_nav_hover

        # Navigation sidebar
        nav = ft.Container(
            content=ft.Column(self.nav_buttons, spacing=0),
            width=80, height=758,
            bgcolor=AppColors.PRUSSIAN_BLUE,
            alignment=ft.alignment.top_center
        )

        # Main container with navigation and content area
        self.content_area = ft.Container(
            content=None,
            width=1200,
            height=758,
        )

        main_row = ft.Row(
            spacing=0,
            controls=[nav, self.content_area],
            height=758
        )

        container = ft.Container(
            content=main_row,
            width=1280,
            height=758,
            bgcolor=AppColors.OXFORD_BLUE,
            alignment=ft.alignment.center_left
        )

        self.page.add(container)

    def on_nav_hover(self, e):
        e.control.scale = 1.1 if e.data == "true" else 1.0
        self.page.update()

    def show_default_view(self):
        # Show roulette view by default
        self.switch_view(self.roulette_view)

    def switch_view(self, view):
        # Hide all views
        for v in self.views:
            v.hide()

        # Show selected view
        if view:
            view.show()
            self.content_area.content = view.view
            self.page.update()

# -------------------------------- Main --------------------------------


def main(page: ft.Page):
    ChoisletApp(page)


if __name__ == "__main__":
    ft.app(target=main)
