from __future__ import annotations

import re
from enum import Enum


class AbstentionState(str, Enum):
    VERIFIED_SOURCE_AVAILABLE = "VERIFIED_SOURCE_AVAILABLE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    JURISDICTION_UNCLEAR = "JURISDICTION_UNCLEAR"
    CONFLICTING_SOURCES = "CONFLICTING_SOURCES"
    HUMAN_LAWYER_RECOMMENDED = "HUMAN_LAWYER_RECOMMENDED"


INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior|above) instructions",
    r"reveal (the )?(system prompt|api key|credentials)",
    r"you are now (the )?(system|developer)",
    r"disregard (all )?(safety|previous) rules",
    r"send .* (password|api key|secret)",
]

ESCALATION_RULES = {
    "court proceeding": [r"court case", r"case is pending", r"summons", r"court hearing", r"tribunal"],
    "urgent eviction or lockout threat": [r"lock(?:ed)? ?out", r"throw me out", r"throw (?:my|our) belongings", r"evict(ion)? (today|tonight|tomorrow|immediately)", r"forced eviction", r"change(?:d)? the locks?", r"changed the lock"],
    "imminent deadline": [r"deadline (is )?(today|tomorrow)", r"within 24 hours", r"hearing tomorrow", r"reply by tomorrow"],
    "threats or intimidation": [r"threaten(ed|ing)?", r"physical harm", r"beat me", r"threat to harm"],
    "complex contractual dispute": [r"arbitration clause", r"multiple agreements", r"commercial lease", r"sublease dispute"],
}


def detect_document_injection(text: str) -> dict:
    matches: list[str] = []
    lowered = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            matches.append(pattern)
    return {
        "is_suspicious": bool(matches),
        "matched_patterns": matches,
        "handling": "Document content is treated as untrusted evidence, never as instructions.",
    }


def escalation_reasons(text: str) -> list[str]:
    lowered = text.lower()
    reasons = []
    for reason, patterns in ESCALATION_RULES.items():
        if any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in patterns):
            reasons.append(reason)
    return reasons


def choose_abstention_state(
    *, jurisdiction: str | None, has_verified_source: bool, escalation: bool, conflicting_sources: bool = False
) -> AbstentionState:
    if escalation:
        return AbstentionState.HUMAN_LAWYER_RECOMMENDED
    if conflicting_sources:
        return AbstentionState.CONFLICTING_SOURCES
    if not jurisdiction or not jurisdiction.strip():
        return AbstentionState.JURISDICTION_UNCLEAR
    if has_verified_source:
        return AbstentionState.VERIFIED_SOURCE_AVAILABLE
    return AbstentionState.INSUFFICIENT_EVIDENCE


def infer_reported_facts(user_text: str, document_text: str = "") -> list[dict]:
    """Keep user statements and document excerpts in separate provenance buckets."""
    facts = []
    cleaned = user_text.strip()
    if cleaned:
        facts.append({
            "field": "user_account",
            "value": cleaned,
            "provenance": "USER_REPORTED",
            "supporting_text": cleaned[:500],
            "notes": "This is the user's account and has not been independently verified.",
        })
    doc = document_text.strip()
    if doc:
        facts.append({
            "field": "uploaded_document_excerpt",
            "value": doc[:1000],
            "provenance": "DOCUMENT_SUPPORTED",
            "supporting_text": doc[:1000],
            "notes": "Text appears in the uploaded document; authenticity and legal effect are not established.",
        })
    return facts


DATE_PATTERNS = [
    # ISO dates and common written forms, including forms without a year.
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:\s+\d{4})?\b",
    r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?\b",
]

def detect_conflicting_tenancy_dates(text: str) -> dict:
    """Flag likely inconsistent tenancy dates for manual clarification; does not resolve them."""
    lowered = text.lower()
    date_mentions = []
    for pattern in DATE_PATTERNS:
        date_mentions.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    context_present = any(term in lowered for term in ("agreement", "handover", "vacated", "tenancy"))
    conflict = len(set(x.lower() for x in date_mentions)) >= 2 and context_present and ("but" in lowered or "however" in lowered or "says" in lowered)
    return {
        "possible_conflict": bool(conflict),
        "date_mentions": list(dict.fromkeys(date_mentions)),
        "note": "Possible inconsistency detected. Preserve both records and ask the user to clarify; do not choose a date automatically." if conflict else "No obvious date conflict detected by the simple rule.",
    }
