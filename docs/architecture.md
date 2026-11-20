# NyayaAI Architecture

## Scope

NyayaAI is a narrow, text-first prototype for rental security-deposit disputes in India. It is not legal representation and does not predict legal outcomes. The interface accepts a narrative and optional PDF/TXT document. Voice input, OCR for scanned PDFs, and a live verified legal corpus are not included in this version.

## Request flow

1. **Streamlit intake** collects a user narrative and a reported property jurisdiction.
2. **Document parser** extracts selectable PDF text with `pypdf` or decodes TXT. Extracted text is capped and treated as untrusted evidence. Image-only PDFs are disclosed as unsupported when no text is extracted.
3. **Local retrieval** searches only active registry records containing exact legal text. Portal URLs without text are excluded.
4. **Provider adapter** calls Gemini when an API key is explicitly supplied; otherwise it generates a deterministic DEMO simulation. Provider identity and mode are retained.
5. **Safety layer** flags instruction-like document text, known urgent situations, and possible contradictory dates. These are heuristic checks and may miss uncommon language.
6. **Provenance layer** labels the complete user narrative as `USER_REPORTED` and extracted text as `DOCUMENT_SUPPORTED`; this MVP does not independently authenticate either source.
7. **Citation validator** checks retrieved source ID, provision label and exact quoted text. It does not decide legal applicability.
8. **Response renderer** returns case organisation, missing information, evidence checklist, practical next steps and a neutral refund-request draft. Legal analysis is removed unless a retrieved passage and its quote validate.
9. **Raw capture** stores timestamped, append-only execution records. Synthetic demo runs remain clearly marked as simulations.

## Model boundary vs deterministic code

| Component | Responsibility |
|---|---|
| Gemini | Understand a narrative, organise information, produce a readable summary and draft |
| Deterministic Python | Parse files, apply source filters, validate citation quotes, add provenance labels, detect selected escalation patterns, capture raw records |
| Human reviewer / lawyer | Verify disputed facts, interpret law, assess applicability, review drafts and handle urgent or formal proceedings |

## M1 research reference

The companion `SPIKIE-24/LLM` repository contains four notebooks and a README. Its README describes M1 as a 12-layer, 768-hidden-size, 12-head multi-head-attention decoder with RoPE, pre-RMSNorm and GELU feed-forward blocks. Its Phase 2 legal NER experiment uses character-boundary prediction. The public repository tree contains notebooks and a README, but no checkpoint or separate deployable model package. M1 was not integrated into NyayaAI. The large local checkpoint and its matching tokenizer/model assets were not included in this delivery. The judgment-oriented entity labels also need adaptation and rental-specific evaluation before use on tenancy documents.

## Current source status

The starter registry has official discovery-portal entries only. It contains no curated, versioned legal passage. Therefore, current runs should abstain from definitive statutory citations. A portal URL is not itself evidence for a legal rule.
