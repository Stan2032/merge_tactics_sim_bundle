# Merge Tactics Simulation Engine

## Overview
A Python-based auto-battler simulation engine (similar to Teamfight Tactics). Resolves battles between teams of units with a grid-based tick system, accounting for unit stats, movement, projectiles, abilities, and trait effects.

## Architecture
- **Language:** Python 3.12
- **Web Server:** Flask (app.py) — serves the simulation UI on port 5000
- **No external database** — all game data is defined in Python/JSON files

## Key Files
- `app.py` — Flask web server entry point; exposes `/` (UI) and `/api/simulate` (JSON API)
- `main.py` — CLI entry point (runs a match and prints results)
- `engine/` — Core simulation modules
  - `full_simulation.py` — Main battle loop (tick-based)
  - `match.py` — Multi-round match orchestration
  - `unit.py` — Unit class with stats and behaviors
  - `draft.py` — Draft/team-building logic
  - `positioning_ai.py` — Starting position assignment
  - `traits.py`, `ability.py` — Trait and ability systems
  - `movement.py`, `targeting.py`, `projectile.py` — Combat mechanics
- `data/` — Static game data
  - `troops.py` — All unit definitions (HP, DPS, range, traits, etc.)
  - `traits.py` — Trait thresholds
  - `trait_effects.py` — Trait buff/debuff multipliers
  - `seasons/` — Season-specific JSON balance data
- `tests/` — unittest test suite

## Running
- **Web UI:** `python app.py` (port 5000)
- **CLI:** `python main.py`
- **Tests:** `python -m unittest discover tests`

## Bug Fixes Applied
- Removed undefined `trait_subsystem.remove_all_effects()` call in `engine/full_simulation.py` (line 69 of original)

## Deployment
- Target: autoscale
- Run: `python app.py`
