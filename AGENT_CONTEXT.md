# Agent Continuation Context

Last updated: 2026-04-14 (UTC)
Branch: `work`

## What is stable now
- Full simulation runs (`python main.py`).
- Projectile API is integrated in `engine/full_simulation.py`.
- Season loader supports listing/loading and basic schema checks.
- Initial unit tests exist under `tests/`.
- Trait activation pipeline now exists with initial start-of-battle effects for `Ace` and `Undead`.
- Trait multipliers are now data-driven from `data/trait_effects.py` with explicit placeholder provenance.

## Simplicity assessment
- Current design is mostly not over-engineered for this stage.
- The only risk area is scope creep (shop/draft/multi-round) before core combat fidelity is complete.
- Keep a strict rule: only build abstractions that are used by running simulation code and covered by tests.

## Known gaps
1. `AbilityEngine` is still a placeholder.
2. Trait logic is only partially implemented (currently only `Ace` and `Undead`).
3. Most troop stats still rely on defaults because `data/troops.py` lacks complete numeric fields.
4. Season JSON contains deltas but not complete baseline numeric data.

## Suggested next execution order
1. Implement `engine/traits.py` and integrate at battle start.
2. Fill troop numeric stats and remove implicit defaults over time.
3. Add ability handlers for a small subset of troops, then expand.
4. Add integration tests around complete battle determinism.
5. Defer non-core systems (shop/draft/rounds) until steps 1-4 are stable.

## Validation baseline
- `python -m unittest discover -s tests -v`
- `python main.py`

## Decision log
- See `DECISIONS.md` for current beliefs, counterarguments, and architecture self-review.
