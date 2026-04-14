from engine.targeting import acquire_target
from engine.movement import move_towards
from engine.projectile import Projectile, resolve_projectile
from engine.timing import can_act, apply_attack_timing
from engine.ability import AbilityEngine
from engine.traits import apply_start_of_battle_traits


def simulate_battle_full(teamA, teamB):
    time = 0
    dt = 0.1

    projectiles = []
    ability_engine = AbilityEngine()
    apply_start_of_battle_traits(teamA)
    apply_start_of_battle_traits(teamB)

    while teamA and teamB and time < 30:
        time += dt

        occupied = {(u.x, u.y) for u in teamA + teamB}

        for u in teamA + teamB:
            ability_engine.update(u, time, [])

        for team, enemies in [(teamA, teamB), (teamB, teamA)]:
            for unit in team:
                if not can_act(unit, time):
                    continue

                target = acquire_target(unit, enemies)
                if not target:
                    continue

                if unit.distance(target) <= unit.range:
                    projectile_speed = getattr(unit, "projectile_speed", 8)
                    projectile = Projectile(
                        source=unit,
                        target=target,
                        speed=projectile_speed,
                        damage=unit.dps,
                    )
                    projectiles.append((projectile, enemies))
                    apply_attack_timing(unit, time)
                else:
                    old_pos = (unit.x, unit.y)
                    move_towards(unit, target, occupied)
                    new_pos = (unit.x, unit.y)
                    if new_pos != old_pos:
                        occupied.discard(old_pos)
                        occupied.add(new_pos)

        remaining_projectiles = []
        for proj, enemies in projectiles:
            result = proj.update(dt)
            if result == "hit":
                resolve_projectile(proj, enemies)
            else:
                remaining_projectiles.append((proj, enemies))
        projectiles = remaining_projectiles

        teamA = [u for u in teamA if u.hp > 0]
        teamB = [u for u in teamB if u.hp > 0]

    return "A" if teamA else "B" if teamB else "Draw"
