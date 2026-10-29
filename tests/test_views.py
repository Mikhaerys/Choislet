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
