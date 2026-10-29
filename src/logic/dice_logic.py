"""Dice game tournament engine with multi-round tie breaking."""

from __future__ import annotations
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerRoll:
    player: str
    die1: int
    die2: int

    @property
    def total(self) -> int:
        return self.die1 + self.die2


@dataclass(frozen=True)
class TournamentRound:
    round_number: int
    rolls: list[PlayerRoll]
    highest_score: int
    winners: list[str]

    @property
    def is_tie(self) -> bool:
        return len(self.winners) > 1


@dataclass(frozen=True)
class TournamentResult:
    rounds: list[TournamentRound]
    champion: str
    final_score: int
    final_die1: int
    final_die2: int


def parse_players(raw_text: str | None) -> list[str]:
    """Parse multiline string into cleaned unique player list."""
    if not raw_text:
        return []
    cleaned: list[str] = []
    seen: set[str] = set()
    for line in raw_text.splitlines():
        name = line.strip()
        if name and name not in seen:
            seen.add(name)
            cleaned.append(name)
    return cleaned


def roll_single_die() -> int:
    return random.randint(1, 6)


def play_tournament(players: list[str], max_rounds: int = 100) -> TournamentResult:
    """Simulate a complete 2-dice tournament with tie-breaking rounds."""
    if not players:
        raise ValueError("At least one player is required to play.")

    current_players = list(players)
    rounds: list[TournamentRound] = []
    round_idx = 1

    last_winning_roll: PlayerRoll | None = None

    while round_idx <= max_rounds:
        rolls: list[PlayerRoll] = []
        for p in current_players:
            r = PlayerRoll(player=p, die1=roll_single_die(), die2=roll_single_die())
            rolls.append(r)

        highest_score = max(r.total for r in rolls)
        tied_rolls = [r for r in rolls if r.total == highest_score]
        winners = [r.player for r in tied_rolls]

        round_data = TournamentRound(
            round_number=round_idx,
            rolls=rolls,
            highest_score=highest_score,
            winners=winners,
        )
        rounds.append(round_data)

        if len(winners) == 1:
            last_winning_roll = tied_rolls[0]
            break

        # Tie: tied players advance to next round
        current_players = winners
        round_idx += 1

    if not last_winning_roll:
        # Fallback if somehow hit max rounds
        last_winning_roll = rounds[-1].rolls[0]

    return TournamentResult(
        rounds=rounds,
        champion=last_winning_roll.player,
        final_score=last_winning_roll.total,
        final_die1=last_winning_roll.die1,
        final_die2=last_winning_roll.die2,
    )
