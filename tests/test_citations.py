from nyayaai.citation_validator import validate_citations


def test_citation_rejects_unknown_source_id():
    result = validate_citations([{"source_id":"FAKE-123", "provision":"Section 999", "quote":"fake text"}], [])
    assert result["all_valid"] is False
    assert result["checks"][0]["valid"] is False


def test_citation_requires_exact_quote():
    sources = [{"source_id":"S1", "source_text":"The tenant shall provide written notice.", "provision":"Clause 4", "jurisdiction":"Delhi", "version":"2024"}]
    good = validate_citations([{"source_id":"S1", "provision":"Clause 4", "quote":"The tenant shall provide written notice."}], sources)
    bad = validate_citations([{"source_id":"S1", "provision":"Clause 4", "quote":"The landlord must pay double."}], sources)
    assert good["all_valid"] is True
    assert bad["all_valid"] is False
    assert good["checks"][0]["applicability"] == "NOT_ASSESSED_BY_CITATION_VALIDATOR"
