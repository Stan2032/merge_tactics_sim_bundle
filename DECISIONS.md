# Decisions, Beliefs, and Self-Review Log

Last updated: 2026-04-14 (UTC)

## What I believe right now
1. The project should optimize for *validated correctness per battle tick*, not feature breadth.
2. The highest-value next work is implementing trait effects and ability effects with tests.
3. Season files are useful as deltas, but they should not be treated as full truth without baseline stats.
4. Documentation/handoff is useful only if it reduces rework and is actively maintained.

## Argument against each belief (self-challenge)
### 1) "Correctness over feature breadth"
- Counterargument: building shop/draft/multi-round earlier could expose architecture constraints sooner.
- Rebuttal: true, but current missing core combat mechanics make those constraints noisy and low-signal.

### 2) "Traits/abilities first"
- Counterargument: complete troop numeric stats might be a stricter prerequisite than trait code.
- Rebuttal: both are needed; practical sequence is small trait+ability slice while progressively filling stats.

### 3) "Season files are deltas"
- Counterargument: maybe season notes are complete enough for a simplified simulator.
- Rebuttal: they still omit many numeric baselines; provenance must remain explicit.

### 4) "Docs are only useful if maintained"
- Counterargument: extra docs can become stale and create confusion.
- Rebuttal: agreed; therefore keep docs short, opinionated, and updated in every handoff.

## Current architecture choices questioned
- Projectile model uses continuous interpolation in a mostly grid-oriented engine.
  - Risk: metric mismatch with grid movement and Manhattan-based AOE checks.
  - Decision for now: keep as-is until trait/ability pass, then either fully grid-ize or consistently use Euclidean metrics.
- Unit stats defaulting in code (`hp`, `dps`, etc.)
  - Risk: defaults can hide missing data.
  - Decision for now: keep defaults for runtime stability, but add TODO to phase toward explicit per-unit stats.
- Initial Ace/Undead trait effect multipliers are currently assumed placeholders.
  - Risk: simulated balance can diverge from live game values.
  - Decision for now: keep placeholders to validate architecture, and replace with sourced numbers once verified.
- Moving trait multipliers into data files (`data/trait_effects.py`) increases transparency.
  - Counterargument: adds one more file and indirection for a tiny codebase.
  - Decision for now: keep it data-driven because provenance tagging is worth the small complexity.

## Rules for future agents
- If a new abstraction is introduced, add at least one executable test proving its value.
- If a mechanic is inferred (not from official source), label it as inferred in data or notes.
- Prefer deleting stale docs over keeping contradictory docs.
