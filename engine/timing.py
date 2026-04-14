def can_act(unit, time):
    return time >= unit.cooldown and time >= unit.locked_until


def apply_attack_timing(unit, time):
    attack_speed = getattr(unit, "attack_speed", 1.0)
    unit.cooldown = time + attack_speed
    unit.locked_until = time + (0.7 * attack_speed)
