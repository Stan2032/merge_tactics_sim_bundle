from engine.targeting import acquire_target
from engine.movement import move_towards
from engine.projectile import Projectile, resolve_projectile
from engine.timing import can_act, apply_attack_timing
from engine.ability import AbilityEngine


def simulate_battle_full(teamA, teamB):
    time = 0
    dt = 0.1

    projectiles = []
    ability_engine = AbilityEngine()

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
                    projectiles.append(
                        Projectile(
                            source=unit,
                            target=target,
                            speed=unit.projectile_speed,
                            damage=unit.dps,
                        )
                    )
                    apply_attack_timing(unit, time)
                else:
                    move_towards(unit, target, occupied)

        for proj in projectiles[:]:
            if proj.update(dt) == "hit":
                target_team = teamB if proj.source in teamA else teamA
                resolve_projectile(proj, target_team)
                projectiles.remove(proj)

        teamA = [u for u in teamA if u.hp > 0]
        teamB = [u for u in teamB if u.hp > 0]

    return "A" if teamA else "B" if teamB else "Draw"
