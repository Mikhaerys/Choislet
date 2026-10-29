"""Application constants, color palette, and asset helpers."""

from pathlib import Path


class AppColors:
    OXFORD_BLUE = "#10192c"
    PRUSSIAN_BLUE = "#1e3b5c"
    CARD_BG = "#182d4a"
    SURFACE_VARIANT = "#15243b"
    SAFFRON = "#fec965"
    COLUMBIA_BLUE = "#d6efff"
    CERULEAN = "#11495C"
    TEXT_MUTED = "#8fa3bf"
    TEXT_LIGHT = "#e8f1fc"
    SUCCESS = "#22c55e"
    ERROR = "#ef4444"

    ROULETTE_COLORS = [
        "#fec965",  # Saffron
        "#9bf6ff",  # Soft cyan
        "#caffbf",  # Soft green
        "#a0c4ff",  # Soft blue
        "#ffc6ff",  # Soft magenta
        "#ffd6a5",  # Soft orange
        "#fdffb6",  # Soft yellow
        "#bdb2ff",  # Soft purple
    ]


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def get_asset_path(filename: str) -> str:
    """Return standard web and desktop Flet asset URL path."""
    return f"/{filename.lstrip('/')}"


def get_fs_asset_path(filename: str) -> str:
    """Return absolute filesystem path for native OS window icon."""
    return str(ASSETS_DIR / filename)


def get_text_field_border(border_radius: int = 12) -> dict:
    """Return modern OutlineInputBorder styling map for Flet 1.0."""
    import flet as ft

    return {
        ft.ControlState.DEFAULT: ft.OutlineInputBorder(
            border_radius=border_radius,
            side=ft.BorderSide(1, AppColors.PRUSSIAN_BLUE),
        ),
        ft.ControlState.FOCUSED: ft.OutlineInputBorder(
            border_radius=border_radius,
            side=ft.BorderSide(1.5, AppColors.SAFFRON),
        ),
    }
