from engine.targeting import acquire_target
from engine.movement import move_towards
from engine.projectile import Projectile, resolve_projectile
from engine.timing import can_act, apply_attack_timing
from engine.ability import AbilityEngine
from engine.traits import TraitSubsystem


def simulate_battle_full(teamA, teamB):
    time = 0
    dt = 0.1

    projectiles = []
    ability_engine = AbilityEngine()
    trait_subsystem = TraitSubsystem()
    trait_subsystem.apply_battle_start_effects(teamA, teamB)

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
                    projectiles.append(Projectile(unit, target, speed=1, damage=unit.dps))
                    apply_attack_timing(unit, time)
                else:
                    move_towards(unit, target, occupied)

        for proj in projectiles[:]:
            hit_state = proj.update(dt)
            if hit_state == "hit":
                enemy_team = teamA if proj.source in teamB else teamB
                resolve_projectile(proj, enemy_team)
                projectiles.remove(proj)

        dead_a = [u for u in teamA if u.hp <= 0]
        dead_b = [u for u in teamB if u.hp <= 0]

        for dead_unit in dead_a + dead_b:
            trait_subsystem.handle_event(
                "unit_death",
                teamA,
                teamB,
                payload={"unit": dead_unit, "time": time},
            )

        teamA = [u for u in teamA if u.hp > 0]
        teamB = [u for u in teamB if u.hp > 0]

    trait_subsystem.remove_all_effects(teamA + teamB)

    return "A" if teamA else "B" if teamB else "Draw"
