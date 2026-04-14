from data.troops import TROOPS


class Unit:
    def __init__(self, name, x=0, y=0):
        if name not in TROOPS:
            raise KeyError(f"Unknown troop '{name}'")
        data = TROOPS[name]

        for required_key in ("traits", "role"):
            if required_key not in data:
                raise ValueError(f"Troop '{name}' missing required field '{required_key}'")

        self.name = name
        self.traits = data["traits"]
        self.role = data["role"]

        self.hp = max(1, data.get("hp", 100))
        self.dps = max(0, data.get("dps", 10))
        self.range = max(1, data.get("range", 1))
        self.projectile_speed = max(1, data.get("projectile_speed", 8))

        self.x = x
        self.y = y

        self.cooldown = 0
        self.locked_until = 0

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
