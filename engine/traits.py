from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from data.traits import TRAITS


@dataclass(frozen=True)
class TraitEffectDescriptor:
    trait: str
    tier: int
    effect_type: str
    targets: str
    modifiers: Dict[str, float]
    triggers: List[str]


class TraitSubsystem:
    """Resolves trait tiers and applies trait effects in a lifecycle-safe way."""

    def __init__(self):
        self._active_effects = []
        self._unit_modifiers = defaultdict(lambda: defaultdict(dict))

    def compute_active_tiers(self, team_units: Iterable) -> Dict[str, int]:
        trait_counts = Counter(
            trait for unit in team_units for trait in getattr(unit, "traits", [])
        )

        active = {}
        for trait, thresholds in TRAITS.items():
            count = trait_counts.get(trait, 0)
            tier = 0
            for threshold in sorted(thresholds):
                if count >= threshold:
                    tier = threshold
            if tier > 0:
                active[trait] = tier

        return active

    def get_effect_descriptors(self, team_units: Iterable) -> List[TraitEffectDescriptor]:
        active_tiers = self.compute_active_tiers(team_units)
        descriptors: List[TraitEffectDescriptor] = []

        ace_tier = active_tiers.get("Ace")
        if ace_tier:
            # Tier values are deliberately conservative for initial integration.
            dps_multiplier = 1.15 if ace_tier == 2 else 1.3
            descriptors.append(
                TraitEffectDescriptor(
                    trait="Ace",
                    tier=ace_tier,
                    effect_type="buff",
                    targets="trait:Ace",
                    modifiers={"dps_multiplier": dps_multiplier},
                    triggers=[],
                )
            )

        undead_tier = active_tiers.get("Undead")
        if undead_tier:
            hp_multiplier = 1.12 if undead_tier == 2 else 1.25
            descriptors.append(
                TraitEffectDescriptor(
                    trait="Undead",
                    tier=undead_tier,
                    effect_type="modifier",
                    targets="trait:Undead",
                    modifiers={"max_hp_multiplier": hp_multiplier},
                    triggers=["unit_death"],
                )
            )

        return descriptors

    def apply_battle_start_effects(self, team_a: List, team_b: List) -> None:
        self._active_effects = []

        for side, team, enemies in (
            ("A", team_a, team_b),
            ("B", team_b, team_a),
        ):
            for descriptor in self.get_effect_descriptors(team):
                self._active_effects.append((side, descriptor))
                self._apply_descriptor_to_team(descriptor, team, enemies)

    def handle_event(
        self,
        event_name: str,
        team_a: List,
        team_b: List,
        payload: Optional[Dict] = None,
    ) -> None:
        """Entry point for dynamic trait behavior during ticks.

        For current scope, only trigger wiring is implemented. Effect payload logic can
        be added trait-by-trait without touching the simulation loop.
        """

        payload = payload or {}
        for side, descriptor in self._active_effects:
            if event_name not in descriptor.triggers:
                continue

            if descriptor.trait == "Undead" and event_name == "unit_death":
                fallen_unit = payload.get("unit")
                if fallen_unit and fallen_unit in (team_a if side == "A" else team_b):
                    # Placeholder for future dynamic Undead logic (e.g. resurrection).
                    # Keeping this in subsystem avoids combat loop hardcoding.
                    _ = fallen_unit

    def remove_all_effects(self, all_units: Iterable) -> None:
        for unit in all_units:
            self._recompute_unit_stats(unit, clear=True)

        self._active_effects = []
        self._unit_modifiers = defaultdict(lambda: defaultdict(dict))

    def _apply_descriptor_to_team(self, descriptor: TraitEffectDescriptor, team: List, enemies: List) -> None:
        del enemies  # Reserved for traits that target enemy team.

        for unit in self._resolve_targets(descriptor.targets, team):
            source_key = f"{descriptor.trait}:{descriptor.tier}"
            for modifier, value in descriptor.modifiers.items():
                self._unit_modifiers[unit][modifier][source_key] = value

            self._recompute_unit_stats(unit)

    def _resolve_targets(self, target_selector: str, team: List) -> List:
        if target_selector.startswith("trait:"):
            trait = target_selector.split(":", maxsplit=1)[1]
            return [u for u in team if trait in getattr(u, "traits", [])]
        if target_selector == "team":
            return list(team)
        return []

    def _recompute_unit_stats(self, unit, clear: bool = False) -> None:
        if not hasattr(unit, "_base_dps"):
            unit._base_dps = unit.dps
        if not hasattr(unit, "_base_range"):
            unit._base_range = unit.range
        if not hasattr(unit, "_base_max_hp"):
            unit._base_max_hp = getattr(unit, "max_hp", unit.hp)
        if not hasattr(unit, "max_hp"):
            unit.max_hp = unit.hp

        if clear:
            unit.dps = unit._base_dps
            unit.range = unit._base_range
            prior_max_hp = unit.max_hp
            unit.max_hp = unit._base_max_hp
            # Preserve current health ratio when undoing effects.
            ratio = unit.hp / prior_max_hp if prior_max_hp > 0 else 0
            unit.hp = max(0, unit.max_hp * ratio)
            return

        mods = self._unit_modifiers.get(unit, {})

        dps_multiplier = 1.0
        for value in mods.get("dps_multiplier", {}).values():
            dps_multiplier *= value

        range_bonus = sum(mods.get("range_bonus", {}).values())

        max_hp_multiplier = 1.0
        for value in mods.get("max_hp_multiplier", {}).values():
            max_hp_multiplier *= value

        old_max_hp = unit.max_hp
        unit.dps = unit._base_dps * dps_multiplier
        unit.range = unit._base_range + range_bonus
        unit.max_hp = unit._base_max_hp * max_hp_multiplier

        if old_max_hp > 0:
            ratio = unit.hp / old_max_hp
            unit.hp = min(unit.max_hp, unit.max_hp * ratio)
        else:
            unit.hp = unit.max_hp
