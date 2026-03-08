# 💊 AI Drug Interaction Checker

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-green)](tests/)

> **⚠️ Disclaimer:** This project is for **educational purposes only**. It is not a
> substitute for professional medical advice, diagnosis, or treatment. Always consult a
> qualified healthcare professional before making clinical decisions.

---

An AI-powered Drug Interaction Checker that accepts two drug names and returns detailed
information about their interaction — including the description, pharmacological
mechanism, severity level, and clinical recommendation.

---

## ✨ Features

- 🔬 **50+ drug interaction entries** covering major drug categories
- 💡 **Fuzzy name matching** — handles brand names, generic names, and misspellings
- 🎨 **Rich CLI** with colour-coded severity indicators
- 🌐 **Flask web interface** with a modern dark-themed UI
- 📊 **Confidence scores** when fuzzy matching is used
- 🔌 **JSON API** at `/api/check` for programmatic access
- ✅ **Full test suite** using pytest

### Drug Categories Covered
- Anticoagulants (Warfarin, Heparin, DOACs)
- NSAIDs (Ibuprofen, Naproxen, Aspirin)
- Antibiotics (Ciprofloxacin, Clarithromycin, Metronidazole)
- Antidepressants / SSRIs / MAOIs
- Antihypertensives (ACE inhibitors, beta-blockers, CCBs)
- Statins (Simvastatin, Atorvastatin, Rosuvastatin)
- Opioids (Morphine, Fentanyl, Tramadol)
- Benzodiazepines, Antidiabetics, Immunosuppressants, and more

---

## 📋 Requirements

- Python 3.9+
- Flask >= 2.3
- Rich >= 13.0

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/karanvirrsingh/pharmacy2.git
cd pharmacy2

# 2. (Optional) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) install the package itself
pip install -e .
```

---

## 🖥️ Usage

### CLI — Interactive Mode

```bash
python main.py
```

### CLI — Single Lookup

```bash
python main.py Warfarin Aspirin
python main.py Coumadin Advil      # brand names work too
python main.py "St. John's Wort" Warfarin
```

### Web Interface

```bash
python app.py
# Open http://localhost:5000 in your browser
```

### JSON API

```bash
curl -X POST http://localhost:5000/api/check \
     -H "Content-Type: application/json" \
     -d '{"drug1": "Warfarin", "drug2": "Aspirin"}'
```

---

## 📊 Sample Output

### Severity Levels

| Level | Emoji | Meaning |
|-------|-------|---------|
| Minor | 🟢 | Clinically insignificant; monitor if necessary |
| Moderate | 🟡 | May require dose adjustment or monitoring |
| Major | 🔴 | Potentially life-threatening; avoid or use with caution |
| Contraindicated | ⛔ | Do not use together |

### API Response (JSON)

```json
{
  "found": true,
  "drug1_query": "Warfarin",
  "drug2_query": "Aspirin",
  "drug1_matched": "Warfarin",
  "drug2_matched": "Aspirin",
  "confidence": 1.0,
  "message": "Interaction found between Warfarin and Aspirin.",
  "interaction": {
    "drug1": "Warfarin",
    "drug2": "Aspirin",
    "description": "Concurrent use significantly increases the risk of bleeding ...",
    "mechanism": "Aspirin irreversibly acetylates COX-1 ...",
    "severity": "Major",
    "recommendation": "Avoid combination unless clearly indicated ..."
  }
}
```

---

## 🗂️ Project Structure

```
pharmacy2/
├── README.md
├── requirements.txt
├── setup.py
├── app.py                       # Flask web application
├── main.py                      # CLI entry point
├── drug_interaction_checker/
│   ├── __init__.py
│   ├── checker.py               # Core interaction checking logic
│   ├── database.py              # 50+ drug interaction knowledge base
│   ├── models.py                # Data models (Drug, Interaction, Severity)
│   └── utils.py                 # Fuzzy name matching, confidence helpers
└── tests/
    ├── __init__.py
    ├── test_checker.py
    ├── test_database.py
    └── test_utils.py
```

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add interactions to `drug_interaction_checker/database.py`
4. Write / update tests in `tests/`
5. Open a Pull Request

---

## ⚠️ Medical Disclaimer

**This software is for educational purposes only.**

- It does not constitute medical advice
- It may not cover all possible interactions
- Always consult a qualified healthcare professional

---

## 📄 License

MIT
