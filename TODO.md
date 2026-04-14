# TODO (Perpetual Work Queue)

This file is intended to be continuously updated by future agents.

## In Progress
- [ ] Keep the simulator MVP-simple: only implement mechanics required for single-battle correctness (no shop/draft/round systems until trait+ability core is stable).
- [ ] Expand trait activation pipeline (`engine/traits.py`) beyond initial Ace/Undead start-of-battle effects.

## Next Up
- [ ] Add troop combat stats in `data/troops.py` (`hp`, `dps`, `range`, `projectile_speed`) for all troops with source/confidence notes.
- [ ] Replace placeholder values in `data/trait_effects.py` with sourced trait numbers and timestamps.
- [ ] Wire seasonal overrides: allow season JSON to patch troop pools/thresholds cleanly during sim setup.
- [ ] Expand `AbilityEngine` from placeholder to per-troop ability handlers and cooldown rules.
- [ ] Add deterministic simulation tests for projectile hit timing, movement blocking, and round timeout outcomes.

## Backlog (defer until MVP stable)
- [ ] Positioning AI module (`engine/positioning_ai.py`).
- [ ] Shop/draft system (`engine/shop.py`, `engine/draft.py`).
- [ ] Multi-round orchestration (`engine/match.py` or `engine/rounds.py`).
- [ ] Data provenance framework (`official`, `wiki`, `measured`, `inferred`) for every numeric stat.
- [ ] Maintain `DECISIONS.md` with explicit belief-vs-counterargument updates each handoff.

## Operational Notes
- Keep combat-loop modules separated; avoid hardcoding season-specific behavior in `engine/combat.py` or `engine/full_simulation.py`.
- Update this file on every meaningful handoff.
- If a task cannot be validated by an executable test, do not add abstraction for it yet.
