from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .citation_validator import validate_citations
from .gemini_provider import call_gemini, parse_model_json
from .legal_sources import retrieve_sources
from .safety import (
    AbstentionState, choose_abstention_state, detect_document_injection,
    escalation_reasons, infer_reported_facts, detect_conflicting_tenancy_dates,
)
from .schemas import CaseAnalysis, PipelineResult

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "outputs" / "raw"


def _demo_analysis(user_text: str, document_text: str) -> dict[str, Any]:
    text = (user_text + " " + document_text).lower()
    amount_match = re.search(r"(?:₹|rs\.?\s*)\s?([\d,]+)", user_text, flags=re.IGNORECASE)
    amount = amount_match.group(1) if amount_match else None
    summary = "You reported a rental security-deposit dispute. This is a user-reported account, not an independently verified finding."
    if amount:
        summary += f" The amount mentioned is ₹{amount}."
    evidence_items = [
        "Rental agreement and any deposit receipt or bank/UPI payment proof",
        "Move-in and move-out photos/videos, with dates if available",
        "Itemised deduction list and bills/receipts shared by the landlord",
        "Messages, emails or call notes about the deposit and handover",
    ]
    if "no written agreement" in text or "without a written agreement" in text:
        evidence_items[0] = "Bank/UPI payment proof, rent receipts, messages, emails, ID/address records and other evidence showing the rental arrangement and deposit payment"
    return {
        "summary": summary,
        "missing_information": [
            "Which Indian state and city is the rented property in?",
            "What are the move-out date and the date the deposit was due to be returned?",
            "Do you have the rental agreement, payment proof, move-in/move-out photos, and written communication?",
        ],
        "evidence_checklist": evidence_items,
        "practical_steps": [
            "Prepare a dated timeline of payment, notice to vacate, handover and follow-up messages.",
            "Ask the landlord in writing for the deposit balance and an itemised explanation of each deduction.",
            "Keep original documents and send copies; avoid threats or altering records.",
            "Get state-specific legal guidance before relying on a statutory claim or starting proceedings.",
        ],
        "refund_request_draft": (
            "Subject: Request for return of rental security deposit\n\n"
            "Dear [Landlord Name],\n\n"
            "I am writing regarding the security deposit of [amount] paid for the property at [address]. "
            "I vacated and handed over the property on [date]. Please arrange return of the refundable balance "
            "by [reasonable date] and share an itemised explanation, along with supporting bills/receipts, "
            "for any proposed deductions.\n\n"
            "Please confirm the payment status in writing. I am happy to resolve this matter amicably.\n\n"
            "Regards,\n[Your Name]"
        ),
        "legal_analysis": "",
        "citations": [],
        "model_notes": "DEMO SIMULATION only. This is not a genuine LLM response or legal opinion.",
    }


def _render_final(analysis: dict[str, Any], state: AbstentionState, lawyer: bool,
                  escalation: list[str], citations_validation: dict[str, Any], sources: list[dict[str, Any]]) -> str:
    lines = ["## Your rental-deposit case summary", analysis.get("summary") or "I have organised the information you provided.", ""]
    if state == AbstentionState.JURISDICTION_UNCLEAR:
        lines.extend(["**Legal-status note: Jurisdiction unclear.** Please provide the state and city of the property before state-specific legal information can be considered.", ""])
    elif state == AbstentionState.INSUFFICIENT_EVIDENCE:
        lines.extend(["**Legal-status note: Insufficient verified legal evidence.** I do not have an applicable, locally verified legal source passage for this question, so I will not name a law, section, case or deadline.", ""])
    elif state == AbstentionState.CONFLICTING_SOURCES:
        lines.extend(["**Legal-status note: Conflicting sources.** A qualified lawyer should review the source conflict before you rely on an interpretation.", ""])
    elif state == AbstentionState.HUMAN_LAWYER_RECOMMENDED:
        lines.extend(["**Human assistance recommended.** This situation may require prompt advice from a qualified lawyer.", ""])
    elif state == AbstentionState.VERIFIED_SOURCE_AVAILABLE:
        lines.extend(["**Source status:** A source passage was retrieved and citation-checked. Citation matching alone does not prove applicability to your facts.", ""])

    if analysis.get("missing_information"):
        lines.append("### Information still needed")
        lines.extend([f"- {x}" for x in analysis["missing_information"]])
        lines.append("")
    if analysis.get("evidence_checklist"):
        lines.append("### Evidence to organise")
        lines.extend([f"- {x}" for x in analysis["evidence_checklist"]])
        lines.append("")
    if analysis.get("practical_steps"):
        lines.append("### Practical next steps")
        lines.extend([f"- {x}" for x in analysis["practical_steps"]])
        lines.append("")
    if sources:
        lines.append("### Retrieved source passages")
        for source in sources:
            lines.append(f"- **{source.get('source_id')} — {source.get('title')}** ({source.get('jurisdiction')}, version: {source.get('version') or 'not recorded'})")
        lines.append("")
    if analysis.get("refund_request_draft"):
        lines.extend(["### Draft message (review and edit before sending)", analysis["refund_request_draft"], ""])
    if lawyer:
        lines.append("### Why a lawyer is recommended")
        lines.extend([f"- {reason}" for reason in escalation])
        lines.append("This assistant cannot represent you or assess urgent legal deadlines. Contact a qualified advocate or appropriate legal-aid service promptly.")
        lines.append("")
    lines.append("**Important:** NyayaAI is an informational case-organisation tool, not a law firm. It does not provide legal representation. Do not rely on this draft as a formal legal notice without checking it.")
    return "\n".join(lines)


def run_case(*, user_text: str, document_text: str = "", jurisdiction: str | None = None,
             api_key: str | None = None, model: str | None = None, force_demo: bool = False,
             test_id: str | None = None) -> PipelineResult:
    combined = f"{user_text}\n{document_text}"
    sources = retrieve_sources(combined, jurisdiction)
    escalation = escalation_reasons(combined)
    doc_safety = detect_document_injection(document_text) if document_text else {
        "is_suspicious": False, "matched_patterns": [], "handling": "No uploaded document provided."
    }
    consistency = detect_conflicting_tenancy_dates(combined)
    live = bool(api_key) and not force_demo
    if live:
        model_id, raw = call_gemini(user_text=user_text, document_text=document_text,
                                    jurisdiction=jurisdiction, retrieved_sources=sources,
                                    api_key=api_key, model=model)
        analysis_data = parse_model_json(raw)
        mode = "LIVE_GEMINI"
    else:
        model_id = "DEMO_SIMULATION"
        analysis_data = _demo_analysis(user_text, document_text)
        raw = json.dumps(analysis_data, ensure_ascii=False, indent=2)
        mode = "DEMO"

    citations = analysis_data.get("citations", []) if isinstance(analysis_data, dict) else []
    validation = validate_citations(citations, sources)
    # Never retain LLM legal analysis unless there is at least one matching retrieved citation.
    if not sources or not validation.get("all_valid"):
        analysis_data["legal_analysis"] = ""
        analysis_data["citations"] = []
    if doc_safety.get("is_suspicious"):
        analysis_data.setdefault("model_notes", "")
        analysis_data["model_notes"] += " Uploaded text contains instruction-like content; it was treated as untrusted document text."

    state = choose_abstention_state(
        jurisdiction=jurisdiction,
        has_verified_source=bool(sources and validation.get("all_valid")),
        escalation=bool(escalation),
        conflicting_sources=False,
    )
    facts = infer_reported_facts(user_text, document_text)
    analysis_data["facts"] = facts
    if consistency["possible_conflict"]:
        analysis_data.setdefault("missing_information", []).append("Please clarify which tenancy/handover date is correct and share both the agreement and handover communication.")
        analysis_data.setdefault("practical_steps", []).append("Keep both records; do not edit either one. Ask the landlord to confirm the handover date in writing.")
    try:
        analysis = CaseAnalysis.model_validate(analysis_data)
    except Exception:
        analysis = CaseAnalysis(summary=str(analysis_data.get("summary", "Case information received.")),
                                model_notes="Some model fields could not be parsed; please review the output.")

    timestamp = datetime.now(timezone.utc).isoformat()
    final_response = _render_final(analysis.model_dump(), state, bool(escalation), escalation, validation, sources)
    if consistency["possible_conflict"]:
        final_response = final_response.replace("## Your rental-deposit case summary", "## Your rental-deposit case summary\n\n**Possible date inconsistency detected:** the provided account contains different tenancy/handover dates. NyayaAI has not selected one as correct; please clarify and preserve both records.")
    if re.search(r"\b(make up|make-up|fabricat|invent)\b", user_text, flags=re.IGNORECASE) and re.search(r"\b(section|law|citation|provision)\b", user_text, flags=re.IGNORECASE):
        final_response += "\n\n**Safety refusal:** I will not invent or fabricate a legal section, citation or provision."
    result = PipelineResult(
        test_id=test_id, model_id=model_id, mode=mode, timestamp=timestamp,
        abstention_state=state.value, human_lawyer_recommended=bool(escalation),
        escalation_reasons=escalation, jurisdiction=jurisdiction,
        retrieved_sources=sources, citation_validation=validation,
        document_safety={**doc_safety, "case_consistency": consistency}, parsed_analysis=analysis,
        raw_model_response=raw,
        final_response=final_response,
    )
    return result


def capture_raw_output(result: PipelineResult, original_input: dict[str, Any], output_dir: str | Path = RAW_DIR) -> Path:
    """Append-only capture: creates a unique file and never overwrites existing raw output."""
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    test_id = result.test_id or "interactive"
    safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", test_id)
    path = folder / f"{safe_id}_{stamp}.json"
    payload = {
        "test_id": result.test_id,
        "timestamp": result.timestamp,
        "mode": result.mode,
        "model_id": result.model_id,
        "original_input": original_input,
        "retrieved_source_passages": result.retrieved_sources,
        "unedited_raw_model_response": result.raw_model_response,
        "citation_validator_result": result.citation_validation,
        "document_safety": result.document_safety,
        "abstention_state": result.abstention_state,
        "final_post_validation_response": result.final_response,
        "note": "DEMO records are simulations, not genuine model outputs." if result.mode == "DEMO" else "Live model response captured before any editing.",
    }
    # Exclusive create prevents accidental overwrites.
    with open(path, "x", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path
