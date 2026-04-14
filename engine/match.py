from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from engine.full_simulation import simulate_battle_full
from engine.positioning_ai import PositioningAI
from engine.unit import Unit


@dataclass(frozen=True)
class MatchConfig:
    rounds: int = 3


@dataclass
class MatchState:
    score: Dict[str, int] = field(default_factory=lambda: {"A": 0, "B": 0, "Draw": 0})
    history: List[str] = field(default_factory=list)


class MatchEngine:
    """Runs multi-round matches and between-round transitions."""

    def __init__(self, positioning_ai: PositioningAI | None = None, config: MatchConfig | None = None):
        self.positioning_ai = positioning_ai or PositioningAI()
        self.config = config or MatchConfig()

    def run_match(self, roster_a: Iterable[Unit], roster_b: Iterable[Unit]) -> MatchState:
        state = MatchState()

        for round_idx in range(1, self.config.rounds + 1):
            team_a = self.positioning_ai.choose_starting_positions(roster_a, side="A")
            team_b = self.positioning_ai.choose_starting_positions(roster_b, side="B")

            winner = simulate_battle_full(team_a, team_b)
            state.score[winner] += 1
            state.history.append(f"round_{round_idx}:{winner}")

            self._apply_between_round_transitions(roster_a, roster_b, winner)

        return state

    def _apply_between_round_transitions(self, roster_a: Iterable[Unit], roster_b: Iterable[Unit], winner: str) -> None:
        """Future hook for fatigue, economy, and adaptation logic."""
        if winner == "A":
            self._heal_roster(roster_a, amount=5)
        elif winner == "B":
            self._heal_roster(roster_b, amount=5)

    @staticmethod
    def _heal_roster(roster: Iterable[Unit], amount: int) -> None:
        for unit in roster:
            unit.hp = min(100, unit.hp + amount)
