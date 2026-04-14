from engine.targeting import acquire_target
from engine.movement import move_towards


def simulate_tick(teamA, teamB):
    occupied = {(u.x, u.y) for u in teamA + teamB}

    for unit in teamA:
        target = acquire_target(unit, teamB)
        if not target:
            continue

        dist = abs(unit.x - target.x) + abs(unit.y - target.y)

        if dist <= unit.range:
            target.hp -= unit.dps
        else:
            move_towards(unit, target, occupied)

    for unit in teamB:
        target = acquire_target(unit, teamA)
        if not target:
            continue

        dist = abs(unit.x - target.x) + abs(unit.y - target.y)

        if dist <= unit.range:
            target.hp -= unit.dps
        else:
            move_towards(unit, target, occupied)

    teamA[:] = [u for u in teamA if u.hp > 0]
    teamB[:] = [u for u in teamB if u.hp > 0]

    return teamA, teamB