import json
import tempfile
import unittest
from pathlib import Path

from data import season_data


class SeasonDataTests(unittest.TestCase):
    def test_load_known_season(self):
        season = season_data.load_season("season_8")
        self.assertEqual(season["season_id"], "season_8")

    def test_mismatched_season_id_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            seasons_dir = Path(tmp)
            (seasons_dir / "season_tmp.json").write_text(
                json.dumps(
                    {
                        "season_id": "wrong_id",
                        "name": "Tmp",
                        "effective_date_utc": "2026-01-01",
                        "source": {"type": "test"},
                    }
                ),
                encoding="utf-8",
            )

            original_dir = season_data.SEASONS_DIR
            season_data.SEASONS_DIR = seasons_dir
            try:
                with self.assertRaises(ValueError):
                    season_data.load_season("season_tmp")
            finally:
                season_data.SEASONS_DIR = original_dir


if __name__ == "__main__":
    unittest.main()
