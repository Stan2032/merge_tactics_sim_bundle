"""Trait effect placeholders.

These are architecture placeholders and should be replaced with sourced values.
"""

TRAIT_EFFECTS = {
    "Ace": {
        2: {"dps_mult": 1.10, "source": "placeholder_inferred"},
        4: {"dps_mult": 1.20, "source": "placeholder_inferred"},
    },
    "Undead": {
        2: {"hp_mult": 1.10, "source": "placeholder_inferred"},
        4: {"hp_mult": 1.20, "source": "placeholder_inferred"},
    },
}
