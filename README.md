# PhishGuard — Regex + Automata Pattern Detector

A student project that screens email addresses, URLs and message text for predefined warning patterns. It demonstrates regular expressions and a small DFA through a pastel pink, green and yellow website.

## Features
- Practical email-format validation
- URL and message pattern checks
- Explainable rule-based warning score
- DFA trace for recognizing whether a string contains a digit
- JFLAP `.jff` model included in `jflap/`
- Responsive frontend

## Requirements
- Python 3.10+
- pip

## Run locally
From the project root:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

If Python reports that `backend` is not importable in your setup, run from the backend folder instead:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Then open http://127.0.0.1:8000.

## JFLAP diagram
Open `jflap/contains_digit_dfa.jff` using JFLAP. The DFA has:
- `q0`: start state, no digit has been seen
- `q1`: accepting state, at least one digit has been seen
- `q0 --0,1--> q1`
- `q0 --a,b--> q0`
- `q1` loops on `a`, `b`, `0`, and `1`

The classroom DFA uses alphabet `{a,b,0,1}`. The website simulator generalizes the non-digit category to any non-digit character.

## Regex101
Use https://regex101.com/ to test individual patterns. The live app runs its actual rules in Python; Regex101 is a companion learning/testing tool, not a backend dependency.

## Limitations and ethics
- This is an educational, rule-based screening tool, not a production anti-phishing product.
- The score is a heuristic, not a probability.
- Email-format validity does not authenticate the sender or prove mailbox existence.
- No live threat-intelligence lookup or domain reputation service is used.
- Avoid pasting real credentials or private messages into demonstrations.
