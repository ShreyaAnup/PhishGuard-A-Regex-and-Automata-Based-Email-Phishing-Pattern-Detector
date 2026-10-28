from urllib.parse import urlparse
from regex_patterns import (
    URL_RE, IPV4_LIKE_RE, URL_SHORTENER_RE, URGENT_RE,
    CREDENTIAL_RE, LINK_ACTION_RE, HTML_LINK_RE, email_is_valid
)

def analyze_input(text: str, mode: str = "message") -> dict:
    text = text.strip()
    findings = []
    score = 0
    email_valid = None
    urls = URL_RE.findall(text)

    if mode == "email":
        email_valid = email_is_valid(text)
        if not email_valid:
            findings.append({
                "severity": "info",
                "title": "Email format may be invalid",
                "detail": "The address does not match this project's practical email-format rule."
            })
        else:
            findings.append({
                "severity": "info",
                "title": "Email format looks plausible",
                "detail": "Format validation cannot confirm that the mailbox exists or that the sender is genuine."
            })

    if mode in ("url", "message"):
        candidates = urls[:]
        if mode == "url" and not candidates:
            candidates = [text] if "://" in text else []
        for url in candidates:
            parsed = urlparse(url)
            host = (parsed.hostname or "").lower()
            if parsed.scheme.lower() not in ("http", "https"):
                findings.append({"severity": "medium", "title": "Unexpected URL scheme",
                                 "detail": f"URL scheme is {parsed.scheme or 'missing'}. Inspect it carefully."})
                score += 15
            if host and (host.replace(".", "").isdigit() or IPV4_LIKE_RE.search(host)):
                findings.append({"severity": "high", "title": "IP-address-like host",
                                 "detail": "The URL host resembles an IP address rather than a conventional domain."})
                score += 30
            if URL_SHORTENER_RE.search(url):
                findings.append({"severity": "medium", "title": "URL shortener detected",
                                 "detail": "Shortened links hide the final destination. Expand and inspect before opening."})
                score += 20
            if "@" in url:
                findings.append({"severity": "medium", "title": "At-sign in URL",
                                 "detail": "An at-sign can make URL text confusing. Check the actual hostname carefully."})
                score += 15
            if len(url) > 120:
                findings.append({"severity": "low", "title": "Very long URL",
                                 "detail": "Long URLs are not automatically malicious, but deserve closer inspection."})
                score += 10

    if mode in ("message", "email"):
        rules = [
            (URGENT_RE, 20, "Urgency or threat language",
             "The text uses urgency or account-threat wording that can pressure a recipient."),
            (CREDENTIAL_RE, 20, "Credential-related wording",
             "The text mentions passwords, one-time codes, or sensitive account details."),
            (LINK_ACTION_RE, 15, "Call to click or sign in",
             "The text encourages clicking a link or signing in. Verify the destination independently."),
        ]
        for pattern, points, title, detail in rules:
            if pattern.search(text):
                findings.append({"severity": "medium", "title": title, "detail": detail})
                score += points

        if HTML_LINK_RE.search(text):
            findings.append({"severity": "low", "title": "HTML link found",
                             "detail": "Inspect the visible link text and actual href destination separately."})
            score += 10

    score = min(score, 100)
    if score >= 50:
        level = "High concern"
    elif score >= 25:
        level = "Medium concern"
    else:
        level = "Low concern"

    if not findings:
        findings.append({
            "severity": "info",
            "title": "No configured warning patterns matched",
            "detail": "This does not prove the content is safe. Review the sender and destination independently."
        })

    return {
        "mode": mode,
        "email_format_valid": email_valid,
        "urls_found": urls,
        "risk_score": score,
        "risk_level": level,
        "findings": findings,
        "disclaimer": "Educational, rule-based screening only. A score is not a probability of phishing."
    }
