import unittest

from engine.traits import TraitSubsystem
from engine.unit import Unit


class TraitSubsystemTests(unittest.TestCase):
    def setUp(self):
        self.subsystem = TraitSubsystem()

    def test_compute_active_tiers_for_ace_and_undead(self):
        ace_team = [Unit("Monk"), Unit("Executioner")]
        undead_team = [Unit("Witch"), Unit("Royal Ghost")]

        ace_tiers = self.subsystem.compute_active_tiers(ace_team)
        undead_tiers = self.subsystem.compute_active_tiers(undead_team)

        self.assertEqual(ace_tiers.get("Ace"), 2)
        self.assertEqual(undead_tiers.get("Undead"), 2)

    def test_descriptor_generation_for_supported_traits(self):
        team = [Unit("Monk"), Unit("Executioner"), Unit("Witch"), Unit("Royal Ghost")]

        descriptors = self.subsystem.get_effect_descriptors(team)
        as_map = {d.trait: d for d in descriptors}

        self.assertIn("Ace", as_map)
        self.assertIn("Undead", as_map)
        self.assertEqual(as_map["Ace"].effect_type, "buff")
        self.assertEqual(as_map["Undead"].effect_type, "modifier")
        self.assertIn("unit_death", as_map["Undead"].triggers)

    def test_battle_start_effects_apply_and_remove(self):
        team_a = [Unit("Monk"), Unit("Executioner")]
        team_b = [Unit("Witch"), Unit("Royal Ghost")]

        monk_base_dps = team_a[0].dps
        witch_base_max_hp = team_b[0].max_hp

        self.subsystem.apply_battle_start_effects(team_a, team_b)

        self.assertGreater(team_a[0].dps, monk_base_dps)
        self.assertGreater(team_b[0].max_hp, witch_base_max_hp)

        self.subsystem.remove_all_effects(team_a + team_b)

        self.assertEqual(team_a[0].dps, monk_base_dps)
        self.assertEqual(team_b[0].max_hp, witch_base_max_hp)


if __name__ == "__main__":
    unittest.main()
