from data.troops import TROOPS
from engine.draft import DraftEngine
from engine.match import MatchEngine


def main():
    draft_engine = DraftEngine()
    match_engine = MatchEngine()

    pool = list(TROOPS.keys())
    team_a = draft_engine.build_roster(pool)
    team_b = draft_engine.build_roster(reversed(pool))

    result = match_engine.run_match(team_a, team_b)

    print("Match score:", result.score)
    print("Round history:", result.history)


if __name__ == "__main__":
    main()
