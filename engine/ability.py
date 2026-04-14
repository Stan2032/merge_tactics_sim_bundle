class AbilityEngine:
    def __init__(self):
        self.timers = {}

    def update(self, unit, time, events):
        name = unit.name

        if name not in self.timers:
            self.timers[name] = time

        # Witch spawn
        if name == "Witch":
            if time - self.timers[name] >= 6:
                events.append(("spawn", unit))
                self.timers[name] = time

        # Giant Skeleton delayed explosion
        if name == "Giant Skeleton" and unit.hp <= 0:
            events.append(("explode", unit, time + 1.5))