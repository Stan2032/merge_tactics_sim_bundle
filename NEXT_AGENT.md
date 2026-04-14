This project is a Merge Tactics simulation engine.

Current state:
- Data model is correct (traits + troops)
- Core combat engine implemented
- Targeting, movement, timing, projectile systems exist
- Ability system is placeholder
- Trait pipeline exists with initial Ace/Undead start-of-battle effects
- Trait effect placeholders are data-driven in `data/trait_effects.py`

Next priorities:
1. Implement full trait system (Ace, Undead, etc.)
2. Expand ability engine per troop
3. Add positioning AI
4. Add drafting + shop system
5. Add multi-round simulation

Important constraints:
- Do NOT break modular structure
- Keep systems separated
- Avoid hardcoding behaviour into combat loop
- Prefer smallest working implementation over adding new architecture early

Goal:
A fully realistic auto-battler simulation engine capable of learning optimal strategies.

Handoff files:
- TODO.md (active perpetual queue)
- AGENT_CONTEXT.md (continuation context)
- DECISIONS.md (beliefs, critiques, and decision log)
