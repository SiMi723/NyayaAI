# NyayaAI Architecture

## Scope

NyayaAI is a text-first prototype for Indian rental security-deposit disputes. It is an informational case-organisation tool, not legal representation, and it does not predict legal outcomes. The interface accepts an English, Hindi or Hinglish narrative and an optional PDF/TXT document. Voice input, OCR for scanned PDFs and a curated live legal corpus are not included in this version.

## Request flow

1. **Streamlit intake** collects the user's narrative and reported property jurisdiction.
2. **Document parser** extracts selectable PDF text with `pypdf` or decodes TXT. Extracted content is capped and treated as untrusted evidence. Image-only PDFs are disclosed as unsupported when no text is extracted.
3. **Local retrieval** searches only active registry records containing exact legal text. Portal URLs without source text are excluded.
4. **Provider adapter** calls Gemini when an API key is supplied; otherwise the app produces a deterministic DEMO simulation.
5. **Safety layer** flags selected instruction-like document text, urgent situations and possible contradictory dates. These are heuristics and can miss uncommon wording.
6. **Provenance layer** labels the user narrative as `USER_REPORTED` and extracted document excerpts as `DOCUMENT_SUPPORTED`. These labels indicate source, not authenticity.
7. **Citation validator** checks retrieved source ID, provision label and exact quoted text. It does not decide legal applicability.
8. **Response renderer** returns case organisation, missing information, evidence checklist, practical next steps and a neutral refund-request draft. Legal analysis is withheld unless a retrieved passage and its quote validate.
9. **Raw capture** stores timestamped, append-only execution records. Synthetic DEMO runs remain clearly marked as simulations.

## Model boundary vs deterministic code

| Component | Responsibility |
|---|---|
| Gemini | Understand the narrative, organise information, produce a readable summary and draft |
| Deterministic Python | Parse files, filter sources, validate citations, add provenance labels, detect selected escalation patterns, capture raw records |
| Human reviewer / advocate | Verify disputed facts, interpret applicable law, review drafts and handle urgent/formal proceedings |

## Current source status

The starter registry contains official discovery-portal entries only. It contains no curated, versioned statutory passage. Therefore, current runs should abstain from definitive statutory citations. An official portal URL is not itself evidence for a legal rule.

## Operational limitations

- The model provider can be replaced through the provider adapter, but each provider/model needs configuration and testing.
- Model availability and quality are not guaranteed; API errors must remain visible and must not be converted into invented answers.
- The source registry needs human curation, jurisdiction and effective-date metadata before legal passages are enabled.
- Date checks and escalation detection are simple heuristics, not comprehensive legal triage.
- Scanned PDFs and handwriting are unsupported because OCR is not included.
