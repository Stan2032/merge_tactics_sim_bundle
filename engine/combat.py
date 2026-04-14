from engine.tick import simulate_tick


def simulate_battle(teamA, teamB, max_ticks=50):
    for _ in range(max_ticks):
        if not teamA:
            return "B"
        if not teamB:
            return "A"

        teamA, teamB = simulate_tick(teamA, teamB)

    return "Draw"
