import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from detector import analyze_input
from automata import trace_contains_digit

def test_email_format():
    assert analyze_input("student@example.com", "email")["email_format_valid"] is True

def test_urgent_message_has_findings():
    result = analyze_input("URGENT! Verify your account now and enter your password", "message")
    assert result["risk_score"] > 0
    assert len(result["findings"]) >= 1

def test_dfa_accepts_digit():
    assert trace_contains_digit("abc2")["accepted"] is True

def test_dfa_rejects_no_digit():
    assert trace_contains_digit("hello")["accepted"] is False
