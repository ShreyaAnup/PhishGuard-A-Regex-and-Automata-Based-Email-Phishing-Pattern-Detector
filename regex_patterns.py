"""Regex rules used by PhishGuard. These are heuristic indicators, not proof of phishing."""
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")
URL_RE = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
IPV4_LIKE_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
URL_SHORTENER_RE = re.compile(
    r"\b(?:bit\.ly|tinyurl\.com|t\.co|goo\.gl|is\.gd|cutt\.ly|ow\.ly)/\S+",
    re.IGNORECASE
)
AT_SYMBOL_RE = re.compile(r"@")
URGENT_RE = re.compile(
    r"\b(?:urgent|immediately|act now|final warning|account suspended|verify your account)\b",
    re.IGNORECASE
)
CREDENTIAL_RE = re.compile(
    r"\b(?:password|passcode|one[- ]time code|OTP|login details|bank details)\b",
    re.IGNORECASE
)
LINK_ACTION_RE = re.compile(
    r"\b(?:click here|click the link|open the link|sign in now|verify now)\b",
    re.IGNORECASE
)
HTML_LINK_RE = re.compile(r"<a\b[^>]*href\s*=\s*['\"]?([^'\"\s>]+)", re.IGNORECASE)

def email_is_valid(value: str) -> bool:
    """Practical format check only; it does not prove mailbox existence."""
    return bool(EMAIL_RE.fullmatch(value.strip()))
