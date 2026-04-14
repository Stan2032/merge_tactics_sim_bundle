from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from data.troops import TROOPS
from engine.unit import Unit


@dataclass(frozen=True)
class DraftConfig:
    team_size: int = 3
    budget: int = 9


class DraftEngine:
    """Simple roster selector with economy-aware hooks."""

    ROLE_COST: Dict[str, int] = {
        "Tank": 4,
        "Assassin": 3,
        "Support": 2,
        "DPS": 3,
    }

    def __init__(self, config: DraftConfig | None = None):
        self.config = config or DraftConfig()

    def build_roster(self, pool: Iterable[str], budget: int | None = None, team_size: int | None = None) -> List[Unit]:
        budget = self.config.budget if budget is None else budget
        team_size = self.config.team_size if team_size is None else team_size

        ranked_pool = sorted(pool, key=self._draft_score, reverse=True)
        spent = 0
        chosen: List[Unit] = []

        for name in ranked_pool:
            cost = self.unit_cost(name)
            if spent + cost > budget:
                continue
            chosen.append(Unit(name))
            spent += cost
            if len(chosen) >= team_size:
                break

        return chosen

    def unit_cost(self, name: str) -> int:
        role = TROOPS[name]["role"]
        return self.ROLE_COST.get(role, 3)

    def _draft_score(self, name: str) -> int:
        troop = TROOPS[name]
        traits = troop["traits"]
        role = troop["role"]

        score = 0
        score += 4 if role == "Tank" else 2
        score += 2 if "Superstar" in traits else 0
        score += 1 if "Assassin" in traits else 0
        return score
