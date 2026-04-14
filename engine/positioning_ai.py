from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from engine.unit import Unit


Coordinate = Tuple[int, int]


@dataclass(frozen=True)
class PositioningConfig:
    """Configures preferred spawn rows for each side of the board."""

    front_row_a: int = 0
    back_row_a: int = 2
    front_row_b: int = 6
    back_row_b: int = 4


class PositioningAI:
    """Role/trait-based starting placement strategy.

    Interface intentionally kept narrow so smarter solvers can replace this later.
    """

    ROLE_PRIORITY = {
        "Tank": 0,
        "Assassin": 1,
        "Support": 2,
        "DPS": 3,
    }

    TRAIT_BIAS: Dict[str, int] = {
        "Assassin": -1,
        "Ranger": +1,
        "Superstar": +1,
    }

    def __init__(self, config: PositioningConfig | None = None):
        self.config = config or PositioningConfig()

    def choose_starting_positions(self, roster: Iterable[Unit], side: str) -> List[Unit]:
        """Return positioned copies of units for one battle.

        Args:
            roster: Source units (kept unmodified).
            side: Either "A" or "B".
        """
        side = side.upper()
        if side not in {"A", "B"}:
            raise ValueError("side must be 'A' or 'B'")

        units = [self._copy_unit(u) for u in roster]
        units.sort(key=self._sort_key)

        if side == "A":
            front_y, back_y = self.config.front_row_a, self.config.back_row_a
        else:
            front_y, back_y = self.config.front_row_b, self.config.back_row_b

        for x, unit in enumerate(units):
            preferred = self._preferred_row(unit, front_y, back_y)
            unit.x = x
            unit.y = preferred

        return units

    def _sort_key(self, unit: Unit):
        return (
            self.ROLE_PRIORITY.get(unit.role, 99),
            sum(self.TRAIT_BIAS.get(trait, 0) for trait in unit.traits),
            unit.name,
        )

    def _preferred_row(self, unit: Unit, front_y: int, back_y: int) -> int:
        row = front_y if unit.role in {"Tank", "Assassin"} else back_y
        row += sum(self.TRAIT_BIAS.get(trait, 0) for trait in unit.traits)
        low, high = sorted((front_y, back_y))
        return max(low, min(high, row))

    @staticmethod
    def _copy_unit(unit: Unit) -> Unit:
        copy = Unit(unit.name, unit.x, unit.y)
        copy.hp = unit.hp
        copy.dps = unit.dps
        copy.range = unit.range
        copy.cooldown = unit.cooldown
        copy.locked_until = unit.locked_until
        return copy
