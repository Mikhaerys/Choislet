"""Coin flip decision engine and statistics tracker."""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from enum import Enum


class CoinSide(str, Enum):
    HEADS = "HEADS"
    TAILS = "TAILS"


@dataclass
class FlipResult:
    side: CoinSide
    label: str


@dataclass
class CoinStats:
    total_flips: int = 0
    heads_count: int = 0
    tails_count: int = 0
    history: list[FlipResult] = field(default_factory=list)

    def record(self, result: FlipResult) -> None:
        self.total_flips += 1
        if result.side == CoinSide.HEADS:
            self.heads_count += 1
        else:
            self.tails_count += 1
        self.history.append(result)
        # Keep maximum 50 history entries
        if len(self.history) > 50:
            self.history.pop(0)

    def reset(self) -> None:
        self.total_flips = 0
        self.heads_count = 0
        self.tails_count = 0
        self.history.clear()


def flip_coin(heads_label: str = "Heads", tails_label: str = "Tails") -> FlipResult:
    """Perform a single unbiased 50/50 coin flip."""
    clean_heads = heads_label.strip() if heads_label and heads_label.strip() else "Heads"
    clean_tails = tails_label.strip() if tails_label and tails_label.strip() else "Tails"

    side = random.choice([CoinSide.HEADS, CoinSide.TAILS])
    label = clean_heads if side == CoinSide.HEADS else clean_tails
    return FlipResult(side=side, label=label)
