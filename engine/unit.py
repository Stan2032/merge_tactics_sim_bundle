from data.troops import TROOPS


class Unit:
    def __init__(self, name, x=0, y=0):
        if name not in TROOPS:
            raise KeyError(f"Unknown troop '{name}'")

        data = TROOPS[name]

        self.name = name
        self.traits = self._validate_traits(name, data.get("traits"))
        self.role = self._validate_role(name, data.get("role"))

        self.hp = self._read_stat(name, data, "hp", default=100)
        self.dps = self._read_stat(name, data, "dps", default=10)
        self.range = self._read_stat(name, data, "range", default=1)
        self.attack_speed = self._read_stat(name, data, "attack_speed", default=1.0)
        self.projectile_speed = self._read_stat(name, data, "projectile_speed", default=1.0)

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
