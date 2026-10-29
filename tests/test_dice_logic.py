import pytest
from src.logic.dice_logic import parse_players, play_tournament, roll_single_die


def test_parse_players():
    raw = " Alice \n Bob \n\n Alice \n Charlie \n"
    players = parse_players(raw)
    assert players == ["Alice", "Bob", "Charlie"]
    assert parse_players("") == []


def test_roll_single_die():
    for _ in range(50):
        val = roll_single_die()
        assert 1 <= val <= 6


def test_play_tournament_determines_champion():
    players = ["Player 1", "Player 2", "Player 3"]
    result = play_tournament(players)
    assert result.champion in players
    assert 2 <= result.final_score <= 12
    assert 1 <= result.final_die1 <= 6
    assert 1 <= result.final_die2 <= 6
    assert len(result.rounds) >= 1
    # Check that final round had exactly 1 winner
    assert len(result.rounds[-1].winners) == 1
    assert result.rounds[-1].winners[0] == result.champion


def test_play_tournament_empty_error():
    with pytest.raises(ValueError):
        play_tournament([])
