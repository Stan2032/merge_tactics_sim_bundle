from flask import Flask, jsonify, render_template_string
from data.troops import TROOPS
from engine.draft import DraftEngine
from engine.match import MatchEngine

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Merge Tactics Simulation Engine</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
            padding: 2rem;
        }
        h1 {
            text-align: center;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: #f8fafc;
        }
        .subtitle {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 2rem;
            font-size: 0.95rem;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .run-btn {
            display: block;
            margin: 0 auto 2rem;
            padding: 0.75rem 2rem;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        .run-btn:hover { background: #4f46e5; }
        .run-btn:disabled { background: #475569; cursor: not-allowed; }
        .result-box {
            background: #1e293b;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .result-box h2 {
            font-size: 1.2rem;
            margin-bottom: 1rem;
            color: #a5b4fc;
            border-bottom: 1px solid #334155;
            padding-bottom: 0.5rem;
        }
        .score-grid {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-bottom: 1rem;
        }
        .score-card {
            background: #0f172a;
            border-radius: 8px;
            padding: 1rem 2rem;
            text-align: center;
            min-width: 120px;
        }
        .score-card .label { font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.25rem; }
        .score-card .value { font-size: 2rem; font-weight: bold; }
        .team-a .value { color: #60a5fa; }
        .team-b .value { color: #f87171; }
        .draw .value { color: #a3e635; }
        .round-list { list-style: none; }
        .round-list li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid #334155;
        }
        .round-list li:last-child { border-bottom: none; }
        .winner-badge {
            padding: 0.2rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .winner-A { background: #1e3a5f; color: #60a5fa; }
        .winner-B { background: #5f1e1e; color: #f87171; }
        .winner-Draw { background: #1a2e1a; color: #a3e635; }
        .team-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        .team-panel { background: #0f172a; border-radius: 8px; padding: 1rem; }
        .team-panel h3 { font-size: 1rem; margin-bottom: 0.75rem; }
        .team-a-header { color: #60a5fa; }
        .team-b-header { color: #f87171; }
        .unit-card {
            background: #1e293b;
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
        }
        .unit-name { font-weight: 600; margin-bottom: 0.2rem; }
        .unit-stats { color: #94a3b8; font-size: 0.78rem; }
        .unit-traits {
            display: flex;
            flex-wrap: wrap;
            gap: 0.25rem;
            margin-top: 0.25rem;
        }
        .trait-tag {
            background: #334155;
            color: #cbd5e1;
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
            font-size: 0.7rem;
        }
        #status { text-align: center; color: #94a3b8; margin-bottom: 1rem; font-size: 0.9rem; }
        .hidden { display: none; }
        .winner-announcement {
            text-align: center;
            font-size: 1.4rem;
            font-weight: bold;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .winner-A-bg { background: #1e3a5f; color: #93c5fd; }
        .winner-B-bg { background: #5f1e1e; color: #fca5a5; }
        .winner-Draw-bg { background: #1a2e1a; color: #bef264; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Merge Tactics Simulation Engine</h1>
        <p class="subtitle">Auto-battler combat simulation — pick teams, run the match</p>

        <button class="run-btn" onclick="runSimulation()" id="runBtn">Run Simulation</button>
        <div id="status"></div>
        <div id="results" class="hidden"></div>
    </div>

    <script>
        async function runSimulation() {
            const btn = document.getElementById('runBtn');
            const status = document.getElementById('status');
            const results = document.getElementById('results');

            btn.disabled = true;
            btn.textContent = 'Running...';
            status.textContent = 'Simulating battle...';
            results.classList.add('hidden');

            try {
                const res = await fetch('/api/simulate');
                const data = await res.json();

                if (data.error) {
                    status.textContent = 'Error: ' + data.error;
                    return;
                }

                const score = data.score;
                const winner = score.A > score.B ? 'A' : score.B > score.A ? 'B' : 'Draw';
                const winnerLabel = winner === 'Draw' ? 'It\'s a Draw!' : `Team ${winner} Wins!`;

                let html = `
                    <div class="result-box">
                        <div class="winner-announcement winner-${winner}-bg">${winnerLabel}</div>
                        <h2>Match Score</h2>
                        <div class="score-grid">
                            <div class="score-card team-a">
                                <div class="label">Team A</div>
                                <div class="value">${score.A}</div>
                            </div>
                            <div class="score-card draw">
                                <div class="label">Draw</div>
                                <div class="value">${score.Draw}</div>
                            </div>
                            <div class="score-card team-b">
                                <div class="label">Team B</div>
                                <div class="value">${score.B}</div>
                            </div>
                        </div>
                    </div>

                    <div class="result-box">
                        <h2>Round History</h2>
                        <ul class="round-list">
                            ${data.history.map(r => {
                                const [round, w] = r.split(':');
                                const label = round.replace('_', ' ').replace(/\b\w/g, c => c.toUpperCase());
                                return `<li><span>${label}</span><span class="winner-badge winner-${w}">${w === 'Draw' ? 'Draw' : 'Team ' + w}</span></li>`;
                            }).join('')}
                        </ul>
                    </div>

                    <div class="result-box">
                        <h2>Teams</h2>
                        <div class="team-section">
                            <div class="team-panel">
                                <h3 class="team-a-header">Team A</h3>
                                ${data.team_a.map(u => `
                                    <div class="unit-card">
                                        <div class="unit-name">${u.name}</div>
                                        <div class="unit-stats">HP: ${u.hp} | DPS: ${u.dps} | Range: ${u.range} | Role: ${u.role}</div>
                                        <div class="unit-traits">${u.traits.map(t => `<span class="trait-tag">${t}</span>`).join('')}</div>
                                    </div>
                                `).join('')}
                            </div>
                            <div class="team-panel">
                                <h3 class="team-b-header">Team B</h3>
                                ${data.team_b.map(u => `
                                    <div class="unit-card">
                                        <div class="unit-name">${u.name}</div>
                                        <div class="unit-stats">HP: ${u.hp} | DPS: ${u.dps} | Range: ${u.range} | Role: ${u.role}</div>
                                        <div class="unit-traits">${u.traits.map(t => `<span class="trait-tag">${t}</span>`).join('')}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `;

                results.innerHTML = html;
                results.classList.remove('hidden');
                status.textContent = '';
            } catch (err) {
                status.textContent = 'Failed to run simulation: ' + err.message;
            } finally {
                btn.disabled = false;
                btn.textContent = 'Run Again';
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/simulate")
def simulate():
    try:
        draft_engine = DraftEngine()
        match_engine = MatchEngine()

        pool = list(TROOPS.keys())
        team_a = draft_engine.build_roster(pool)
        team_b = draft_engine.build_roster(reversed(pool))

        result = match_engine.run_match(team_a, team_b)

        def unit_info(u):
            troop = TROOPS[u.name]
            return {
                "name": u.name,
                "hp": troop["hp"],
                "dps": troop["dps"],
                "range": troop["range"],
                "role": troop["role"],
                "traits": troop["traits"],
            }

        return jsonify({
            "score": result.score,
            "history": result.history,
            "team_a": [unit_info(u) for u in team_a],
            "team_b": [unit_info(u) for u in team_b],
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
