"""Flask web application for the AI Drug Interaction Checker."""

from __future__ import annotations

import html

from flask import Flask, jsonify, render_template_string, request

from drug_interaction_checker import DrugInteractionChecker
from drug_interaction_checker.models import Severity

app = Flask(__name__)
checker = DrugInteractionChecker()

# ---------------------------------------------------------------------------
# Colour palette (maps Severity → CSS class)
# ---------------------------------------------------------------------------
_SEVERITY_CSS = {
    Severity.MINOR: "severity-minor",
    Severity.MODERATE: "severity-moderate",
    Severity.MAJOR: "severity-major",
    Severity.CONTRAINDICATED: "severity-contraindicated",
}

# ---------------------------------------------------------------------------
# Inline HTML template (single file for portability)
# ---------------------------------------------------------------------------
_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>AI Drug Interaction Checker</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem;
    }
    header {
      text-align: center;
      margin-bottom: 2rem;
    }
    header h1 { font-size: 2.2rem; color: #38bdf8; }
    header p  { color: #94a3b8; margin-top: .4rem; }

    .card {
      background: #1e293b;
      border-radius: 12px;
      padding: 2rem;
      width: 100%;
      max-width: 680px;
      box-shadow: 0 4px 24px rgba(0,0,0,.4);
    }
    .form-row {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }
    .form-group {
      flex: 1;
      min-width: 180px;
      display: flex;
      flex-direction: column;
      gap: .4rem;
    }
    label { font-size: .85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .05em; }
    input[type=text] {
      padding: .65rem 1rem;
      border-radius: 8px;
      border: 1px solid #334155;
      background: #0f172a;
      color: #e2e8f0;
      font-size: 1rem;
      outline: none;
      transition: border-color .2s;
    }
    input[type=text]:focus { border-color: #38bdf8; }
    button {
      margin-top: 1.2rem;
      width: 100%;
      padding: .75rem;
      background: #38bdf8;
      color: #0f172a;
      font-size: 1rem;
      font-weight: 700;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background .2s;
    }
    button:hover { background: #7dd3fc; }
    button:disabled { background: #334155; color: #64748b; cursor: not-allowed; }

    /* ── Result panel ──────────────────────────────────────────────── */
    #result { margin-top: 1.8rem; display: none; }

    .result-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: .5rem;
      margin-bottom: 1rem;
    }
    .result-header h2 { font-size: 1.2rem; }

    .badge {
      padding: .3rem .9rem;
      border-radius: 999px;
      font-size: .85rem;
      font-weight: 700;
    }
    .severity-minor          { background:#16a34a; color:#fff; }
    .severity-moderate       { background:#ca8a04; color:#fff; }
    .severity-major          { background:#dc2626; color:#fff; }
    .severity-contraindicated{ background:#991b1b; color:#fff; border: 2px solid #ef4444; }

    .border-minor          { border-left: 4px solid #16a34a; }
    .border-moderate       { border-left: 4px solid #ca8a04; }
    .border-major          { border-left: 4px solid #dc2626; }
    .border-contraindicated{ border-left: 4px solid #991b1b; }
    .border-none           { border-left: 4px solid #475569; }

    .detail-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1rem;
    }
    .detail-item { background: #0f172a; border-radius: 8px; padding: 1rem 1.2rem; }
    .detail-item h3 { font-size: .75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .06em; margin-bottom: .4rem; }
    .detail-item p  { line-height: 1.6; }

    .confidence-bar-wrap { margin-top: .4rem; }
    .confidence-bar-bg { background: #1e293b; border-radius: 4px; height: 6px; overflow: hidden; }
    .confidence-bar    { background: #38bdf8; height: 6px; border-radius: 4px; transition: width .4s; }

    .no-interaction {
      text-align: center;
      color: #94a3b8;
      padding: 1.5rem;
      background: #0f172a;
      border-radius: 8px;
    }
    .error-msg { color: #f87171; text-align: center; padding: 1rem; }
    .spinner { display: inline-block; width: 1em; height: 1em; border: 2px solid #0f172a; border-top-color: transparent; border-radius: 50%; animation: spin .6s linear infinite; vertical-align: middle; margin-right: .4rem; }
    @keyframes spin { to { transform: rotate(360deg); } }

    .disclaimer {
      margin-top: 1.5rem;
      font-size: .78rem;
      color: #64748b;
      text-align: center;
      max-width: 680px;
    }
    footer { margin-top: 3rem; color: #475569; font-size: .8rem; }
  </style>
</head>
<body>
  <header>
    <h1>💊 AI Drug Interaction Checker</h1>
    <p>Enter two drug names to check for known interactions</p>
  </header>

  <div class="card">
    <form id="checkForm">
      <div class="form-row">
        <div class="form-group">
          <label for="drug1">Drug 1</label>
          <input type="text" id="drug1" name="drug1" placeholder="e.g. Warfarin" autocomplete="off" required />
        </div>
        <div class="form-group">
          <label for="drug2">Drug 2</label>
          <input type="text" id="drug2" name="drug2" placeholder="e.g. Aspirin" autocomplete="off" required />
        </div>
      </div>
      <button type="submit" id="checkBtn">Check Interaction</button>
    </form>

    <div id="result"></div>
  </div>

  <p class="disclaimer">
    ⚠️ <strong>Disclaimer:</strong> This tool is for <em>educational purposes only</em> and is not a
    substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified
    healthcare professional before making any clinical decisions.
  </p>

  <footer>AI Drug Interaction Checker &mdash; Open-source, educational use only</footer>

  <script>
    const form    = document.getElementById('checkForm');
    const btn     = document.getElementById('checkBtn');
    const resultDiv = document.getElementById('result');

    const severityEmoji = {
      Minor: '🟢', Moderate: '🟡', Major: '🔴', Contraindicated: '⛔'
    };

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const drug1 = document.getElementById('drug1').value.trim();
      const drug2 = document.getElementById('drug2').value.trim();
      if (!drug1 || !drug2) return;

      btn.disabled = true;
      btn.innerHTML = '<span class="spinner"></span>Checking…';
      resultDiv.style.display = 'block';
      resultDiv.innerHTML = '<p style="text-align:center;color:#94a3b8;">Loading…</p>';

      try {
        const resp = await fetch('/api/check', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({drug1, drug2})
        });
        const data = await resp.json();
        renderResult(data);
      } catch (err) {
        resultDiv.innerHTML = `<p class="error-msg">Network error: ${err.message}</p>`;
      } finally {
        btn.disabled = false;
        btn.textContent = 'Check Interaction';
      }
    });

    function renderResult(data) {
      if (data.error) {
        resultDiv.innerHTML = `<p class="error-msg">⚠️ ${escHtml(data.error)}</p>`;
        return;
      }

      if (!data.found) {
        resultDiv.innerHTML = `
          <div class="no-interaction border-none" style="border-left:4px solid #475569;padding-left:1rem;text-align:left;">
            <p>${escHtml(data.message)}</p>
          </div>`;
        return;
      }

      const {interaction, confidence, message} = data;
      const sev   = interaction.severity;
      const css   = 'severity-' + sev.toLowerCase();
      const border= 'border-'   + sev.toLowerCase();
      const pct   = Math.round(confidence * 100);
      const emoji = severityEmoji[sev] || '';

      resultDiv.innerHTML = `
        <div class="${border}" style="padding-left:1rem;">
          <div class="result-header">
            <h2>⚕ ${escHtml(interaction.drug1)} + ${escHtml(interaction.drug2)}</h2>
            <span class="badge ${css}">${emoji} ${escHtml(sev)}</span>
          </div>
          <div class="detail-grid">
            <div class="detail-item">
              <h3>Description</h3>
              <p>${escHtml(interaction.description)}</p>
            </div>
            <div class="detail-item">
              <h3>Mechanism</h3>
              <p>${escHtml(interaction.mechanism)}</p>
            </div>
            <div class="detail-item">
              <h3>Recommendation</h3>
              <p>${escHtml(interaction.recommendation)}</p>
            </div>
            ${pct < 100 ? `
            <div class="detail-item">
              <h3>Confidence</h3>
              <p>${pct}% (fuzzy name match)</p>
              <div class="confidence-bar-wrap">
                <div class="confidence-bar-bg"><div class="confidence-bar" style="width:${pct}%"></div></div>
              </div>
            </div>` : ''}
          </div>
          ${message.includes('\\n') ? '<p style="margin-top:.8rem;font-size:.85rem;color:#94a3b8;">' + escHtml(message.split('\\n').slice(1).join(' ')) + '</p>' : ''}
        </div>`;
    }

    function escHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
        .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
    }
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index() -> str:
    """Serve the main page."""
    return render_template_string(_HTML_TEMPLATE)


@app.route("/api/check", methods=["POST"])
def api_check():
    """JSON API endpoint for interaction checking.

    Request body (JSON)::

        {"drug1": "Warfarin", "drug2": "Aspirin"}

    Response (JSON)::

        {
            "found": true,
            "drug1_query": "Warfarin",
            "drug2_query": "Aspirin",
            "drug1_matched": "Warfarin",
            "drug2_matched": "Aspirin",
            "confidence": 1.0,
            "message": "Interaction found ...",
            "interaction": {
                "drug1": "Warfarin",
                "drug2": "Aspirin",
                "description": "...",
                "mechanism": "...",
                "severity": "Major",
                "recommendation": "..."
            }
        }
    """
    data = request.get_json(silent=True)
    if not data or "drug1" not in data or "drug2" not in data:
        return jsonify({"error": "Please provide 'drug1' and 'drug2' fields."}), 400

    drug1 = str(data["drug1"]).strip()
    drug2 = str(data["drug2"]).strip()

    if not drug1 or not drug2:
        return jsonify({"error": "Drug names must not be empty."}), 400

    result = checker.check(drug1, drug2)

    response_payload: dict = {
        "found": result.found,
        "drug1_query": result.drug1_query,
        "drug2_query": result.drug2_query,
        "drug1_matched": result.drug1_matched,
        "drug2_matched": result.drug2_matched,
        "confidence": result.confidence,
        "message": result.message,
        "interaction": None,
    }

    if result.interaction is not None:
        ix = result.interaction
        response_payload["interaction"] = {
            "drug1": ix.drug1,
            "drug2": ix.drug2,
            "description": ix.description,
            "mechanism": ix.mechanism,
            "severity": ix.severity.value,
            "recommendation": ix.recommendation,
        }

    return jsonify(response_payload)


@app.route("/api/health")
def health() -> dict:
    """Health check endpoint."""
    return jsonify({"status": "ok"})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
