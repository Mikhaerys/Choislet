"""Tests for Flet views instantiation and navigation."""

from unittest.mock import MagicMock
import flet as ft
from src.main import ChoisletApp
from src.views.home_view import HomeView
from src.views.roulette_view import RouletteView
from src.views.coin_view import CoinView
from src.views.dice_view import DiceView


def test_views_instantiation_and_navigation():
    page = MagicMock(spec=ft.Page)
    page.window = MagicMock()
    page.add = MagicMock()
    page.update = MagicMock()

    app = ChoisletApp(page)
    assert len(app.views) == 4
    assert isinstance(app.views[0], HomeView)
    assert isinstance(app.views[1], RouletteView)
    assert isinstance(app.views[2], CoinView)
    assert isinstance(app.views[3], DiceView)

    # Test tab switches
    for idx in range(4):
        app.switch_to_tab(idx)
        assert app.rail.selected_index == idx
        assert app.views[idx].visible is True
        assert app.current_view == app.views[idx]


def test_roulette_view_input_update():
    page = MagicMock(spec=ft.Page)
    page.update = MagicMock()

    roulette = RouletteView(page)
    event = MagicMock(spec=ft.ControlEvent)
    event.control = MagicMock()
    event.control.value = "Option A\nOption B\nOption C"

    roulette._on_input_changed(event)
    assert roulette.candidates == ["Option A", "Option B", "Option C"]
    assert len(roulette.sectors) == 3


def test_coin_view_preset():
    page = MagicMock(spec=ft.Page)
    page.update = MagicMock()

    coin = CoinView(page)
    coin._apply_preset("Alpha", "Beta")
    assert coin.heads_input.value == "Alpha"
    assert coin.tails_input.value == "Beta"


def test_dice_view_player_setup():
    page = MagicMock(spec=ft.Page)
    page.update = MagicMock()

    dice = DiceView(page)
    dice._set_players("Player X\nPlayer Y")
    assert dice.players_input.value == "Player X\nPlayer Y"


def test_base_view_adaptive_scroll():
    page = MagicMock(spec=ft.Page)
    roulette = RouletteView(page)
    assert isinstance(roulette.content, ft.Column)
    assert roulette.content.scroll == ft.ScrollMode.ADAPTIVE


def test_roulette_view_responsive_sizing():
    # Wide screen (desktop)
    page_wide = MagicMock(spec=ft.Page)
    page_wide.width = 1200
    roulette_wide = RouletteView(page_wide)
    assert roulette_wide.canvas_size == 500.0

    # Mobile screen
    page_mobile = MagicMock(spec=ft.Page)
    page_mobile.width = 400
    roulette_mobile = RouletteView(page_mobile)
    assert roulette_mobile.canvas_size == 400 - 112

    # Responsive resize test
    page_wide.width = 400
    roulette_wide.on_resize()
    assert roulette_wide.canvas_size == 400 - 112


def test_roulette_view_web_vs_desktop_calibration():
    page_desktop = MagicMock(spec=ft.Page)
    page_desktop.web = False
    r_desktop = RouletteView(page_desktop)
    assert r_desktop.spin_duration_ms == 4000

    page_web = MagicMock(spec=ft.Page)
    page_web.web = True
    r_web = RouletteView(page_web)
    assert r_web.spin_duration_ms == 5200


async def test_roulette_view_monotonic_spins():
    import asyncio
    page = MagicMock(spec=ft.Page)
    page.update = MagicMock()
    page.web = False
    roulette = RouletteView(page)

    assert roulette.current_rotation == 0.0

    async def trigger_end():
        await asyncio.sleep(0.02)
        roulette._on_animation_end(MagicMock())

    # Simulate first spin
    event = MagicMock(spec=ft.ControlEvent)
    t1 = asyncio.create_task(trigger_end())
    await roulette._spin_click(event)
    await t1

    first_rotation = roulette.current_rotation
    assert first_rotation > 0.0

    # Simulate second spin
    t2 = asyncio.create_task(trigger_end())
    await roulette._spin_click(event)
    await t2

    second_rotation = roulette.current_rotation
    # Crucial test: second rotation must strictly exceed first rotation (never reset backwards!)
    assert second_rotation > first_rotation
    assert second_rotation - first_rotation >= 4 * 2 * 3.14
