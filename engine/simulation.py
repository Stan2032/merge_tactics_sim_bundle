from engine.unit import Unit
from engine.combat import simulate_battle


def simulate_game():
    # placeholder teams
    teamA = [Unit("Monk"), Unit("Executioner"), Unit("Bandit")]
    teamB = [Unit("Witch"), Unit("Royal Ghost"), Unit("Skeleton King")]

    winner = simulate_battle(teamA, teamB)
    print("Winner:", winner)