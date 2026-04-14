import math


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

        dist = math.hypot(dx, dy)
        if dist == 0:
            return "hit"
        travel = self.speed * dt
        if dist <= travel:
            self.x = self.target.x
            self.y = self.target.y
            return "hit"

        ratio = travel / dist
        self.x += dx * ratio
        self.y += dy * ratio

        return None


def resolve_projectile(proj, enemies):
    if proj.target.hp <= 0:
        return

    if proj.aoe > 0:
        for e in enemies:
            if abs(e.x - proj.target.x) + abs(e.y - proj.target.y) <= proj.aoe:
                e.hp -= proj.damage
    else:
        proj.target.hp -= proj.damage
