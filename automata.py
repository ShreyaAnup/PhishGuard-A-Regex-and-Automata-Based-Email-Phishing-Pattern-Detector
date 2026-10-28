"""A tiny DFA simulator used to demonstrate finite-state processing.

DFA: Does the input contain at least one digit?
Alphabet for the classroom diagram: {a, b, 0, 1}. In the simulator, all
non-digit characters behave like the non-digit category.
Regex equivalent: [0-9]
"""
import re

def trace_contains_digit(text: str) -> dict:
    state = "q0"
    trace = [{"index": 0, "character": "START", "state": state,
              "meaning": "No digit has been seen yet."}]
    for index, char in enumerate(text, start=1):
        if char.isdigit():
            state = "q1"
        # q0 remains q0 for non-digits; q1 remains accepting forever.
        trace.append({
            "index": index,
            "character": char,
            "state": state,
            "meaning": "Digit found — accepting state." if state == "q1"
                       else "No digit seen yet."
        })
    return {
        "pattern": "[0-9]",
        "accepted": state == "q1",
        "final_state": state,
        "trace": trace,
        "note": "This teaching DFA checks whether at least one digit appears. "
                "It is a simplified automata demonstration, not the phishing score itself."
    }
