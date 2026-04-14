class Projectile:
    def __init__(self, source, target, speed, damage, kind="linear", aoe=0, flight_time=0):
        self.source = source
        self.target = target
        self.speed = speed
        self.damage = damage
        self.kind = kind
        self.aoe = aoe
        self.flight_time = flight_time

        self.x = source.x
        self.y = source.y
        self.t = 0

    def update(self, dt):
        self.t += dt

        if self.kind == "instant":
            return "hit"

        if self.kind == "arc":
            if self.t >= self.flight_time:
                return "hit"
            return None

        # linear
        dx = self.target.x - self.x
        dy = self.target.y - self.y

        if abs(dx) + abs(dy) <= self.speed:
            return "hit"

        if abs(dx) > abs(dy):
            self.x += 1 if dx > 0 else -1
        else:
            self.y += 1 if dy > 0 else -1

        return None


def resolve_projectile(proj, enemies):
    if proj.aoe > 0:
        for e in enemies:
            if abs(e.x - proj.target.x) + abs(e.y - proj.target.y) <= proj.aoe:
                e.hp -= proj.damage
    else:
        proj.target.hp -= proj.damage