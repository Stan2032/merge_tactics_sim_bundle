from engine.full_simulation import simulate_battle_full
from engine.unit import Unit


def main():
    teamA = [
        Unit("Monk", 0, 0),
        Unit("Executioner", 1, 0),
        Unit("Bandit", 2, 0),
    ]

    teamB = [
        Unit("Witch", 0, 2),
        Unit("Royal Ghost", 1, 2),
        Unit("Skeleton King", 2, 2),
    ]

    result = simulate_battle_full(teamA, teamB)
    print("Winner:", result)


if __name__ == "__main__":
    main()
