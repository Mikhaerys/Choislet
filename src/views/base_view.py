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
        self.content = self.init_view()

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
