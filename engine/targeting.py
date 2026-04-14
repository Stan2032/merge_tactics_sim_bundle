def acquire_target(unit, enemies):
    enemies = [e for e in enemies if e.hp > 0]
    if not enemies:
        return None

    if unit.role == "Assassin":
        return max(enemies, key=lambda e: e.y)

    if unit.role == "DPS":
        return min(enemies, key=lambda e: e.hp)

    return min(enemies, key=lambda e: unit.distance(e))
