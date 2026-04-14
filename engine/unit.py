from data.troops import TROOPS

class Unit:
    def __init__(self, name, x=0, y=0):
        data = TROOPS[name]

        self.name = name
        self.traits = data["traits"]
        self.role = data["role"]

        self.hp = 100
        self.dps = 10
        self.range = 1

        self.x = x
        self.y = y

        self.cooldown = 0
        self.locked_until = 0

    def __repr__(self):
        return f"{self.name}(HP={self.hp})"
