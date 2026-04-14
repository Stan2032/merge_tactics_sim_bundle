# Merge Tactics Simulation Engine

Full auto-battler simulation system with:
- Trait system
- Combat engine
- Projectile + ability timing
- AI drafting + positioning

Current trait implementation includes an initial start-of-battle pipeline (`engine/traits.py`)
with baseline `Ace` and `Undead` effects for architecture validation.
Trait multipliers are currently kept in `data/trait_effects.py` with explicit placeholder provenance.

Seasonal data is stored under `data/seasons/` and can be loaded with `data/season_data.py`
(`list_seasons()` and `load_season(season_id)`).
`load_season` validates required top-level keys and season id/file-name consistency.

Run with:

```bash
python main.py
```

Run checks with:

```bash
python -m unittest discover -s tests -v
```
