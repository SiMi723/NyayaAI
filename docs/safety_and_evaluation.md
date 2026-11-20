# NyayaAI — Legal Reliability, Safety and Evaluation

## Scope

NyayaAI is a narrow MVP for organising rental security-deposit disputes. It helps users structure their account, identify documents to collect, prepare a neutral refund request and recognise when professional legal help is needed. It is not a law firm, does not represent users and does not promise outcomes.

## How hallucinations are reduced

1. The app retrieves only active local source records with exact `source_text`.
2. Portal-only records are discovery links, not legal evidence, and are excluded from retrieval.
3. The model is instructed to use only retrieved source IDs and exact quotes; it must leave legal analysis empty when evidence is missing.
4. Citation validation checks source ID, provision text and exact quote. Unsupported citations are rejected.
5. The pipeline removes generated legal analysis unless at least one citation matches a retrieved passage. This is a guardrail, not a proof that every remaining statement is correct.
6. Jurisdiction is requested explicitly; the app does not infer a state tenancy law from general context.

## Legal source registry

`data/legal_sources.json` contains official discovery portals (India Code, NALSA, Legislative Department and Supreme Court of India). These entries have `active: false` and empty `source_text`. They are not citable legal authority. Before a legal passage is enabled, a reviewer should record its exact official text, title, source URL, jurisdiction, provision, document version and effective date. State-specific tenancy material must be checked for the property location and relevant date.

## Citation validation and applicability

`nyayaai/citation_validator.py` verifies that the source ID was retrieved and that the provision and quoted text match the stored passage. The validator explicitly reports `NOT_ASSESSED_BY_CITATION_VALIDATOR` for applicability. A valid quote does not prove that the provision governs the user's facts, remains in force, or has been interpreted correctly. Human legal review remains necessary for those questions.

## Abstention and escalation

The pipeline supports `VERIFIED_SOURCE_AVAILABLE`, `INSUFFICIENT_EVIDENCE`, `JURISDICTION_UNCLEAR`, `CONFLICTING_SOURCES` and `HUMAN_LAWYER_RECOMMENDED`. It flags court proceedings, urgent eviction/lockout threats, imminent deadlines, threats and complex contractual disputes for qualified assistance. The current detector is keyword/rule based and can miss unusual phrasing or over-flag benign text.

## Fact provenance

User-entered facts are labelled `USER_REPORTED`. Text extracted from an uploaded file is labelled `DOCUMENT_SUPPORTED`; this means the text appears in that file, not that the document is authentic or legally conclusive. The starter app does not label ordinary user statements as `SOURCE_VERIFIED`.

## Document safety

Uploaded files are parsed as text and passed as untrusted evidence. Instruction-like strings are flagged. They are not executed and are not allowed to override application instructions. File extraction can be incomplete for scanned PDFs; OCR is not included in this MVP.

## Synthetic test cases

Eight cases are provided in `data/synthetic_cases.json`:

- TC01: Security deposit not returned
- TC02: No written rental agreement
- TC03: Disputed repair deductions
- TC04: Jurisdiction missing
- TC05: User requests fabricated legal provisions
- TC06: Suspicious legal claims in uploaded notice
- TC07: Imminent forced lockout
- TC08: Conflicting tenancy dates

Run genuine Gemini tests (requires your own API key configured locally):

```bash
python scripts/run_evaluations.py --live
```

Run deterministic simulation only (not genuine AI results):

```bash
python scripts/run_evaluations.py --demo
```

Every run creates append-only raw JSON records under `outputs/raw/` and writes a reviewer tracker to `outputs/evaluation.csv`. Demo files are labelled as simulations. The live runner explicitly passes the configured API key to the pipeline and rejects any result that does not report `LIVE_GEMINI`. The tracker intentionally leaves quality fields as `REVIEW_REQUIRED` / `NOT_YET_REVIEWED`; do not mark cases as passed without inspecting raw output and recording a human review.

## Current limitations and failure modes

- No tenancy statute or judgment passage is preloaded; therefore the starter version abstains from definitive statutory advice.
- The keyword retrieval and escalation checks are simple baselines, not a comprehensive legal retrieval or triage system.
- Citation checks establish source identity/text matching only, not applicability.
- Gemini may still make unsupported factual statements. Inspect outputs, compare them to uploaded evidence and reject uncertain responses.
- Hindi/Hinglish quality depends on the selected model and needs manual testing.
- Scanned PDFs and handwriting are not handled because OCR is not included.
- Legal aid availability and state-specific law should be independently verified before giving user-specific recommendations.
- Synthetic tests are not a representative sample of real legal disputes.

## Honest status

The code includes safety controls and automated unit tests. The eight end-to-end model cases are not considered passed until they have been run with a live model and manually reviewed. No claim is made that the system is hallucination-free, legally certified or a substitute for an advocate.

## Audit notes (20 November 2026)

- 17 automated unit tests pass in the audit runtime.
- Eight synthetic cases were executed in deterministic DEMO mode and captured as raw JSON; they are not live Gemini runs and have not been manually quality-scored.
- The runtime used for the audit did not have Streamlit installed, and package installation was blocked by unavailable network access. The browser UI launch was therefore not verified in this environment.
- The date-conflict heuristic was extended to detect written day-month dates without a year, as used in TC08. This remains a simple English-language heuristic.
