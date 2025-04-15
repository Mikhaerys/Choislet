import flet as ft


class BaseView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.visible = False
        self.view = self.build()

    def build(self):
        """
        Builds the view interface. This method should be overridden
        by child classes.
        """
        return ft.Container()

    def show(self):
        """Shows the view"""
        self.visible = True
        self.view.visible = True
        self.page.update()

    def hide(self):
        """Hides the view"""
        self.visible = False
        self.view.visible = False
        self.page.update()
