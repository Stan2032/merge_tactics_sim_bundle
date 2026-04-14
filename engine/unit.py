from data.troops import TROOPS


class Unit:
    def __init__(self, name, x=0, y=0):
        data = TROOPS[name]

        self.name = name
        self.traits = data["traits"]
        self.role = data["role"]

        self.max_hp = 100
        self.hp = self.max_hp
        self.dps = 10
        self.range = 1

        self.x = x
        self.y = y

        self.cooldown = 0
        self.locked_until = 0

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
