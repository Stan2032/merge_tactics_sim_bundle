import unittest

from engine.projectile import Projectile, resolve_projectile


class Dummy:
    def __init__(self, x=0, y=0, hp=100):
        self.x = x
        self.y = y
        self.hp = hp


class ProjectileTests(unittest.TestCase):
    def test_linear_projectile_uses_speed_and_dt(self):
        source = Dummy(x=0, y=0)
        target = Dummy(x=4, y=0)
        proj = Projectile(source=source, target=target, speed=8, damage=10)

        self.assertIsNone(proj.update(0.1))
        self.assertAlmostEqual(proj.x, 0.8, places=6)

    def test_linear_projectile_diagonal_hit_uses_euclidean_distance(self):
        source = Dummy(x=0, y=0)
        target = Dummy(x=1, y=1)
        proj = Projectile(source=source, target=target, speed=20, damage=10)

        result = proj.update(0.1)
        self.assertEqual(result, "hit")
        self.assertEqual((proj.x, proj.y), (1, 1))

    def test_resolve_projectile_skips_dead_target(self):
        source = Dummy(x=0, y=0)
        target = Dummy(x=1, y=0, hp=0)
        proj = Projectile(source=source, target=target, speed=8, damage=10)

        resolve_projectile(proj, [target])
        self.assertEqual(target.hp, 0)


if __name__ == "__main__":
    unittest.main()
