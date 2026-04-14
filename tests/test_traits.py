import unittest

from data.trait_effects import TRAIT_EFFECTS
from engine.traits import apply_start_of_battle_traits, compute_active_trait_tiers
from engine.unit import Unit


class TraitTests(unittest.TestCase):
    def test_trait_effects_have_provenance_marker(self):
        self.assertEqual(TRAIT_EFFECTS["Ace"][2]["source"], "placeholder_inferred")

    def test_compute_active_trait_tiers(self):
        units = [Unit("Monk"), Unit("Executioner")]
        active = compute_active_trait_tiers(units)
        self.assertEqual(active.get("Ace"), 2)

    def test_apply_start_of_battle_traits_ace_dps_buff(self):
        units = [Unit("Monk"), Unit("Executioner")]
        base_dps = units[0].dps

        apply_start_of_battle_traits(units)

        self.assertGreater(units[0].dps, base_dps)
        self.assertAlmostEqual(units[0].dps, base_dps * 1.10, places=6)

    def test_apply_start_of_battle_traits_undead_hp_buff(self):
        units = [Unit("Witch"), Unit("Royal Ghost")]
        base_hp = units[0].hp

        apply_start_of_battle_traits(units)

        self.assertGreater(units[0].hp, base_hp)
        self.assertAlmostEqual(units[0].hp, base_hp * 1.10, places=6)


if __name__ == "__main__":
    unittest.main()
