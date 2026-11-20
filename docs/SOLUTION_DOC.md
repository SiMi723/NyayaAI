# NyayaAI - AI Legal Action Copilot

*Kuku AI Generalist Assignment | Problem 2 | Focus: Indian rental security-deposit disputes*

## Problem choice, user and scope

I chose Problem 2 because everyday rental disputes can leave people unsure what happened, what evidence matters and how to ask for a resolution. I narrowed the product to one recurring situation: a tenant has vacated a rented home, but the landlord has not returned the security deposit or disputes deductions for painting or repairs. A narrow scope makes the prototype testable without claiming to cover all Indian law.

The intended user is a tenant who can describe the problem in English, Hindi or Hinglish. The current prototype accepts text and optional selectable-text PDF/TXT documents. Voice input, OCR for scanned PDFs, formal legal notices, court filings and legal representation are outside this version. I assume the user supplies the property city/state and that uploaded files are evidence to organise, not proof of authenticity.

## How it works

1. The user describes the dispute and provides the property's city/state.
2. The user may upload a rental agreement, notice or supporting PDF/TXT. The app extracts selectable text and warns when no text can be extracted.
3. Gemini organises the narrative into a case summary, missing-information questions, evidence checklist, practical next steps and a neutral refund-request draft. Without an API key, the app clearly identifies its deterministic DEMO mode.
4. Python applies basic checks for selected urgent situations, suspicious instruction-like text in documents, provenance labels and possible date conflicts. It also retrieves only active legal-source records containing exact text and validates returned source IDs, provision labels and quotations.
5. The user reviews the output. A qualified advocate remains responsible for legal interpretation and formal proceedings.

The intended output is an organised case file the tenant can review and act on, not a prediction of who will win. A useful result separates what the user reported from what appears in an uploaded file, makes unknowns visible and helps prepare a clear, neutral request without inventing legal authority.

## AI, code and human roles

Gemini handles language understanding, summarisation and drafting. Deterministic Python handles file parsing, source filtering, selected escalation/date checks, provenance labels, citation checks and append-only raw-output capture. A human reviews disputed facts and every draft; a qualified advocate is needed for court matters, urgent lockout/eviction risks, imminent deadlines, threats and complex contractual interpretation. The model provider is isolated behind an adapter so another compatible provider can be connected later.

## Legal reliability and abstention

The starter registry lists official discovery portals but contains no curated, versioned statutory passages. A portal URL is not legal evidence. NyayaAI therefore abstains from definitive statutory citations at present. If exact text is added later, the validator checks whether the source was retrieved and whether its provision and quotation match. That check does not establish that the law applies to the user's facts or remains in force. The app is not hallucination-free and must not replace a lawyer.

## Quality checks, honest failures and what I learned

I created eight synthetic cases: deposit not returned; no written agreement; disputed repair deductions; missing jurisdiction; a request to invent a legal provision; a suspicious uploaded notice; an imminent lockout; and conflicting tenancy dates. The recorded deterministic runs are preserved as raw JSON and clearly labelled DEMO. The code audit passed 17 automated unit tests. These results test code paths; they are not genuine Gemini accuracy scores and the end-to-end cases remain unreviewed until run live and checked by a person.

The first local version opened, but displayed DEMO MODE because I had not configured a live API key. I initially spent time waiting for an automated coding agent that was not showing visible progress. I changed approach: I inspected the project structure, kept the scope small, checked the provider and pipeline separately, and used VS Code and Git to make the application reproducible. During code review I found a real bug: the evaluation runner checked for an API key but did not pass it into the pipeline, so a requested live run could fall back to DEMO. I fixed the key hand-off, added a guard against non-live results in live mode, corrected the documented launch path and added regression tests.

After deployment, the first Gemini live request returned HTTP 503 (temporary model unavailability). The Streamlit application was still running; the failure was at the model service. I kept the error visible, changed the model selection and retried rather than presenting a failed call as a successful AI result. Model availability and live quality still need repeat testing. This was a useful reminder that a working interface, a reachable API and a reliable answer are three different things.

## Limitations, scale and tools

Current limitations include no verified statute passages, no voice input, no OCR for scanned PDFs, incomplete field-level extraction and no full chronological evidence ledger. The date and escalation checks are simple heuristics and can miss edge cases. Hindi/Hinglish quality and all live outputs need manual review. Eight DEMO records do not establish legal accuracy.

To scale, I would add a reviewed, jurisdiction- and date-aware corpus of official tenancy material; rental-specific annotated examples; stronger multilingual extraction; a structured event/evidence ledger; monitoring for model failures; and advocate review for high-risk cases. The provider adapter makes model replacement possible without redesigning the user workflow.

Tools used: Antigravity and Gemini during initial prototyping; ChatGPT for code generation, review and debugging; VS Code for local development; Python, Streamlit, Pydantic, pypdf, Google GenAI SDK and pytest for implementation; GitHub for version control; and Streamlit Community Cloud for deployment. ChatGPT-assisted code was reviewed and tested rather than treated as automatically correct. One concrete tool/code failure and its correction are described above.

**Submission status:** Public runnable prototype and repository are available; 17 automated unit tests passed in the recorded audit; eight synthetic DEMO raw outputs are included. Genuine live end-to-end runs, manual output scoring and further browser-level testing remain necessary. No legal certification or guaranteed outcome is claimed.
