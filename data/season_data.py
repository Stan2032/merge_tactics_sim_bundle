import json
from pathlib import Path


SEASONS_DIR = Path(__file__).parent / "seasons"
REQUIRED_TOP_LEVEL_KEYS = ("season_id", "name", "effective_date_utc", "source")


def list_seasons():
    return sorted(path.stem for path in SEASONS_DIR.glob("*.json"))


def load_season(season_id):
    season_path = SEASONS_DIR / f"{season_id}.json"
    if not season_path.exists():
        known = ", ".join(list_seasons()) or "(none)"
        raise FileNotFoundError(f"Unknown season '{season_id}'. Available seasons: {known}")

    with season_path.open("r", encoding="utf-8") as fp:
        season = json.load(fp)

    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in season]
    if missing:
        missing_fields = ", ".join(missing)
        raise ValueError(f"Season '{season_id}' is missing required keys: {missing_fields}")

    if season["season_id"] != season_id:
        raise ValueError(
            f"Season id mismatch: requested '{season_id}', file contains '{season['season_id']}'"
        )

    return season
