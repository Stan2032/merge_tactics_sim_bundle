This project is a Merge Tactics simulation engine.

Current state:
- Data model is correct (traits + troops)
- Core combat engine implemented
- Targeting, movement, timing, projectile systems exist
- Ability system is placeholder

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

Goal:
A fully realistic auto-battler simulation engine capable of learning optimal strategies.
