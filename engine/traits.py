from collections import Counter

from data.traits import TRAITS
from data.trait_effects import TRAIT_EFFECTS


def compute_active_trait_tiers(units, thresholds=None):
    """Return the highest active tier per trait for the provided units."""
    thresholds = thresholds or TRAITS
    counts = Counter()
    for unit in units:
        for trait in unit.traits:
            counts[trait] += 1

    active = {}
    for trait, trait_thresholds in thresholds.items():
        count = counts.get(trait, 0)
        eligible = [tier for tier in trait_thresholds if count >= tier]
        if eligible:
            active[trait] = max(eligible)
    return active


def _apply_effect_to_unit(unit, effect):
    if "dps_mult" in effect:
        unit.dps *= effect["dps_mult"]
    if "hp_mult" in effect:
        unit.hp *= effect["hp_mult"]


def apply_start_of_battle_traits(units):
    """Apply one-time start-of-battle trait effects.

    Effects are intentionally minimal and only implemented for Ace/Undead.
    """
    active = compute_active_trait_tiers(units)
    for unit in units:
        if getattr(unit, "_trait_effects_applied", False):
            continue

        for trait in unit.traits:
            tier = active.get(trait)
            if not tier:
                continue
            effect = TRAIT_EFFECTS.get(trait, {}).get(tier)
            if effect:
                _apply_effect_to_unit(unit, effect)

        unit._trait_effects_applied = True

    return active
