from engine.targeting import acquire_target
from engine.movement import move_towards
from engine.projectile import Projectile, resolve_projectile
from engine.timing import can_act, apply_attack_timing
from engine.ability import AbilityEngine


def simulate_battle_full(teamA, teamB):
    time = 0
    dt = 0.1

    projectiles = []
    events = []
    ability_engine = AbilityEngine()

    while teamA and teamB and time < 30:
        time += dt

        occupied = {(u.x, u.y) for u in teamA + teamB}

        # abilities
        for u in teamA + teamB:
            ability_engine.update(u, time, events)

        # actions
        for unit in teamA:
            if not can_act(unit, time):
                continue

            target = acquire_target(unit, teamB)
            if not target:
                continue

            dist = abs(unit.x - target.x) + abs(unit.y - target.y)

            if dist <= unit.range:
                proj = Projectile(unit, target, speed=1, damage=unit.dps)
                projectiles.append(proj)
                apply_attack_timing(unit, time)
            else:
                move_towards(unit, target, occupied)

        for unit in teamB:
            if not can_act(unit, time):
                continue

            target = acquire_target(unit, teamA)
            if not target:
                continue

            dist = abs(unit.x - target.x) + abs(unit.y - target.y)

            if dist <= unit.range:
                proj = Projectile(unit, target, speed=1, damage=unit.dps)
                projectiles.append(proj)
                apply_attack_timing(unit, time)
            else:
                move_towards(unit, target, occupied)

        # update projectiles
        for proj in projectiles[:]:
            result = proj.update(dt)
            if result == "hit":
                resolve_projectile(proj, teamA if proj.source in teamB else teamB)
                projectiles.remove(proj)

        # cleanup
        teamA = [u for u in teamA if u.hp > 0]
        teamB = [u for u in teamB if u.hp > 0]

    if teamA:
        return "A"
    elif teamB:
        return "B"
    return "Draw"