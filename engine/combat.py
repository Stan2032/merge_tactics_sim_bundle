def simulate_battle(teamA, teamB):
    while teamA and teamB:
        teamB[0].hp -= teamA[0].dps
        if teamB[0].hp <= 0:
            teamB.pop(0)

        if not teamB:
            return "A"

        teamA[0].hp -= teamB[0].dps
        if teamA[0].hp <= 0:
            teamA.pop(0)

    return "B"