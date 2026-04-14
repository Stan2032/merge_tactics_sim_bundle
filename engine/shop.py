from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List

from data.troops import TROOPS


@dataclass
class ShopState:
    gold: int = 5
    xp: int = 0
    level: int = 1
    bench: List[str] = field(default_factory=list)
    current_offer: List[str] = field(default_factory=list)
    locked: bool = False


class EconomyHooks:
    """Round-level economy hooks for orchestration layer."""

    BASE_INCOME: int = 5
    WIN_STREAK_BONUS: int = 1

    def start_round(self, state: ShopState, won_previous_round: bool) -> None:
        bonus = self.WIN_STREAK_BONUS if won_previous_round else 0
        state.gold += self.BASE_INCOME + bonus

    def buy_xp(self, state: ShopState, amount: int = 1, cost_per_xp: int = 2) -> bool:
        total_cost = amount * cost_per_xp
        if state.gold < total_cost:
            return False
        state.gold -= total_cost
        state.xp += amount
        while state.xp >= state.level * 4:
            state.xp -= state.level * 4
            state.level += 1
        return True


class Shop:
    OFFER_SIZE = 3

    def reroll(self, state: ShopState) -> List[str]:
        if state.locked and state.current_offer:
            return state.current_offer
        state.current_offer = random.sample(list(TROOPS.keys()), self.OFFER_SIZE)
        return state.current_offer

    def toggle_lock(self, state: ShopState, locked: bool) -> None:
        state.locked = locked

    def buy(self, state: ShopState, unit_name: str, cost: int) -> bool:
        if unit_name not in state.current_offer or state.gold < cost:
            return False
        state.gold -= cost
        state.bench.append(unit_name)
        state.current_offer.remove(unit_name)
        return True
