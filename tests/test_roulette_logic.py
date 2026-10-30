import math
import pytest
from src.logic.roulette_logic import (
    parse_candidates,
    calculate_sectors,
    determine_winner,
    generate_spin_target,
)


def test_parse_candidates():
    raw = "  Alice \n\n Bob \n Charlie   \n   "
    candidates = parse_candidates(raw)
    assert candidates == ["Alice", "Bob", "Charlie"]
    assert parse_candidates(None) == []
    assert parse_candidates("") == []


def test_calculate_sectors():
    candidates = ["A", "B", "C", "D"]
    sectors = calculate_sectors(candidates)
    assert len(sectors) == 4
    sweep = 2.0 * math.pi / 4.0

    for i, s in enumerate(sectors):
        assert s.candidate == candidates[i]
        assert s.index == i
        assert pytest.approx(s.start_angle) == i * sweep
        assert pytest.approx(s.end_angle) == (i + 1) * sweep
        assert pytest.approx(s.sweep_angle) == sweep


def test_determine_winner_exact_angles():
    # 4 candidates:
    # Sector 0 [A]: [0, pi/2)
    # Sector 1 [B]: [pi/2, pi)
    # Sector 2 [C]: [pi, 3*pi/2)
    # Sector 3 [D]: [3*pi/2, 2*pi)
    candidates = ["A", "B", "C", "D"]
    sectors = calculate_sectors(candidates)

    # If rotation is 0, pointer at 0 points at Sector 0 (A)
    assert determine_winner(sectors, 0.0) == "A"

    # If rotated by pi/2 (90 deg clockwise), sector D (was at 3pi/2) moved to 0
    assert determine_winner(sectors, math.pi / 2.0) == "D"

    # If rotated by pi (180 deg clockwise), sector C (was at pi) moved to 0
    assert determine_winner(sectors, math.pi) == "C"

    # If rotated by 3*pi/2 (270 deg clockwise), sector B (was at pi/2) moved to 0
    assert determine_winner(sectors, 3.0 * math.pi / 2.0) == "B"


def test_generate_spin_target():
    sectors = calculate_sectors(["Option 1", "Option 2"])
    target_rotation = generate_spin_target(min_rotations=5, max_rotations=5, target_sector_index=0, sectors=sectors)
    # Total rotation should be >= 5 * 2*pi
    assert target_rotation >= 5 * 2 * math.pi
    # Winner should be Option 1
    winner = determine_winner(sectors, target_rotation)
    assert winner == "Option 1"


def test_generate_spin_target_default():
    target_rotation = generate_spin_target()
    assert target_rotation >= 4 * 2 * math.pi


def test_generate_spin_target_with_accumulated_rotation():
    sectors = calculate_sectors(["Option 1", "Option 2", "Option 3"])
    current_rot = 34.56
    target_rotation = generate_spin_target(
        min_rotations=4,
        max_rotations=4,
        target_sector_index=1,
        sectors=sectors,
        current_rotation=current_rot,
    )
    total_rot = current_rot + target_rotation
    winner = determine_winner(sectors, total_rot)
    assert winner == "Option 2"
