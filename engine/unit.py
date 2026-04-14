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
        self.traits = self._validate_traits(name, data.get("traits"))
        self.role = self._validate_role(name, data.get("role"))

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

    @staticmethod
    def _validate_traits(name, traits):
        if not isinstance(traits, list) or not all(isinstance(t, str) for t in traits):
            raise ValueError(f"Troop '{name}' must define 'traits' as a list[str]")
        return traits

    @staticmethod
    def _validate_role(name, role):
        if not isinstance(role, str) or not role:
            raise ValueError(f"Troop '{name}' must define non-empty 'role'")
        return role

    @staticmethod
    def _read_stat(name, data, key, default):
        value = data.get(key, default)
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(f"Troop '{name}' has invalid '{key}'={value}; expected positive number")
        return value
