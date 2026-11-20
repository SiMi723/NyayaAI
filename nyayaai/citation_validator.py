from __future__ import annotations

from typing import Any


def validate_citations(citations: list[dict[str, Any]], retrieved_sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Validate citation identity and exact quoted text, not legal applicability."""
    source_by_id = {str(s.get("source_id")): s for s in retrieved_sources}
    checks = []
    for citation in citations:
        source_id = str(citation.get("source_id", ""))
        provision = str(citation.get("provision", "")).strip()
        quote = str(citation.get("quote", "")).strip()
        source = source_by_id.get(source_id)
        if source is None:
            checks.append({"source_id": source_id, "valid": False, "reason": "Source ID was not retrieved."})
            continue
        source_text = str(source.get("source_text", ""))
        provision_expected = str(source.get("provision", "")).strip()
        provision_ok = not provision or provision == provision_expected or provision in source_text
        quote_ok = bool(quote) and quote in source_text
        checks.append({
            "source_id": source_id,
            "valid": bool(provision_ok and quote_ok),
            "provision_exact_match": provision_ok,
            "quoted_text_exact_match": quote_ok,
            "jurisdiction": source.get("jurisdiction"),
            "version": source.get("version"),
            "effective_date": source.get("effective_date"),
            "applicability": "NOT_ASSESSED_BY_CITATION_VALIDATOR",
            "reason": "Citation identity/text checks passed; applicability still needs legal interpretation." if provision_ok and quote_ok else "Provision or exact quoted text did not match the retrieved source.",
        })
    invalid = [c for c in checks if not c["valid"]]
    return {
        "all_valid": (not invalid) if checks else None,
        "citation_count": len(checks),
        "valid_count": sum(1 for c in checks if c["valid"]),
        "invalid_count": len(invalid),
        "checks": checks,
        "important_limit": "A matching citation does not establish legal applicability or correctness of interpretation.",
    }
