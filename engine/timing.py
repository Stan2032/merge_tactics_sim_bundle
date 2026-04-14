def can_act(unit, time):
    return time >= unit.cooldown and time >= unit.locked_until


def apply_attack_timing(unit, time):
    unit.cooldown = time + 1.0
    unit.locked_until = time + 0.7