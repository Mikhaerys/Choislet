"""Base view component for Choislet screens."""

from __future__ import annotations
import flet as ft
from src.utils.constants import AppColors


class BaseView(ft.Container):
    """Abstract base view providing responsive container layout and page reference."""

    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(
            expand=True,
            bgcolor=AppColors.OXFORD_BLUE,
            padding=ft.Padding(left=20, right=20, top=20, bottom=20),
            **kwargs,
        )
        self._app_page = page
        view_content = self.init_view()
        if isinstance(view_content, ft.Column) and view_content.scroll:
            self.content = view_content
        else:
            self.content = ft.Column(
                controls=[view_content],
                scroll=ft.ScrollMode.ADAPTIVE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )

    @property
    def app_page(self) -> ft.Page:
        """Return attached page or fallback stored reference."""
        try:
            return self.page or self._app_page
        except Exception:
            return self._app_page

    def init_view(self) -> ft.Control:
        """Construct and return the view's root control."""
        raise NotImplementedError("Subclasses of BaseView must implement init_view().")

    def on_activate(self) -> None:
        """Hook called when view becomes active."""
        pass

    def on_deactivate(self) -> None:
        """Hook called when view is navigated away from."""
        pass

    def on_resize(self) -> None:
        """Hook called when page window size changes."""
        pass
