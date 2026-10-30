"""Roulette wheel decision engine and mathematical helpers."""

from __future__ import annotations
import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class RouletteSector:
    candidate: str
    index: int
    start_angle: float
    end_angle: float
    sweep_angle: float


def parse_candidates(raw_text: str | None) -> list[str]:
    """Parse multiline string into a cleaned list of candidate strings."""
    if not raw_text:
        return []
    lines = [line.strip() for line in raw_text.splitlines()]
    return [line for line in lines if line]


def calculate_sectors(candidates: list[str]) -> list[RouletteSector]:
    """Calculate angular sectors for each candidate on a 2*pi radian circle."""
    if not candidates:
        return []

    num_candidates = len(candidates)
    sweep_angle = (2.0 * math.pi) / num_candidates
    sectors: list[RouletteSector] = []

    for i, candidate in enumerate(candidates):
        start = i * sweep_angle
        end = (i + 1) * sweep_angle
        sectors.append(
            RouletteSector(
                candidate=candidate,
                index=i,
                start_angle=start,
                end_angle=end,
                sweep_angle=sweep_angle,
            )
        )
    return sectors


def determine_winner(sectors: list[RouletteSector], total_rotation_radians: float) -> str:
    """Determine the winning candidate under the pointer at angle 0.

    When the canvas rotates clockwise by total_rotation_radians,
    the angle on the unrotated wheel that lands at 0 radians is:
        effective_angle = (2*pi - (total_rotation_radians % 2*pi)) % (2*pi)
    """
    if not sectors:
        return ""

    two_pi = 2.0 * math.pi
    norm_rotation = total_rotation_radians % two_pi
    effective_angle = (two_pi - norm_rotation) % two_pi

    for sector in sectors:
        if sector.start_angle <= effective_angle < sector.end_angle:
            return sector.candidate

    # Fallback in case of floating-point precision boundary at 2*pi
    return sectors[0].candidate


def generate_spin_target(
    min_rotations: int = 4,
    max_rotations: int = 6,
    target_sector_index: int | None = None,
    sectors: list[RouletteSector] | None = None,
    current_rotation: float = 0.0,
) -> float:
    """Generate total rotation in radians with full spins plus random final offset."""
    full_rotations = random.randint(min_rotations, max_rotations)
    two_pi = 2.0 * math.pi

    if target_sector_index is not None and sectors and 0 <= target_sector_index < len(sectors):
        sector = sectors[target_sector_index]
        # Land somewhere in the middle 80% of the target sector
        target_effective = sector.start_angle + (sector.sweep_angle * random.uniform(0.1, 0.9))
        current_offset = current_rotation % two_pi
        needed_offset = (two_pi - target_effective - current_offset) % two_pi
        return (full_rotations * two_pi) + needed_offset

    # Completely random angle
    random_offset = random.uniform(0.0, two_pi)
    return (full_rotations * two_pi) + random_offset
