def move_towards(unit, target, occupied):
    options = [
        (unit.x+1, unit.y),
        (unit.x-1, unit.y),
        (unit.x, unit.y+1),
        (unit.x, unit.y-1),
    ]

    options = [p for p in options if p not in occupied]

    if not options:
        return

    best = min(options, key=lambda p: abs(p[0]-target.x)+abs(p[1]-target.y))
    unit.x, unit.y = best