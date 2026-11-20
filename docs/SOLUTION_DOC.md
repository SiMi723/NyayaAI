# NyayaAI - AI Legal Action Copilot for Indian Rental Deposit Disputes

## Problem choice and scope

I selected Problem 2 and narrowed it to one recurring everyday problem: a tenant vacates a rented home, but the landlord withholds the security deposit or disputes deductions for repairs or painting. A narrow scope makes it possible to build and test a useful workflow without claiming to cover all Indian law. The prototype accepts free-text in English, Hindi or Hinglish and optional PDF/TXT documents. Voice input, scanned-PDF OCR, formal legal notices and legal representation are outside the current scope.

## How the prototype works

A user describes the dispute and reports the property city/state. NyayaAI extracts selectable PDF text or reads TXT, then organises the narrative into a case summary, missing-information questions, an evidence checklist, practical next steps and a neutral refund-request draft. Gemini is called when an API key is configured; otherwise the app clearly identifies its deterministic DEMO simulation. Basic deterministic checks flag selected urgent situations, instruction-like text in uploaded documents and possible conflicting tenancy dates. User narratives are labelled USER_REPORTED; extracted document excerpts are labelled DOCUMENT_SUPPORTED. These labels do not prove authenticity.

## AI, code and human roles

Gemini handles language understanding, summarisation and drafting. Python handles file parsing, retrieval over the local legal-source registry, provenance labels, selected escalation and date checks, citation validation and append-only raw-output capture. A human must review every draft and disputed fact. A qualified advocate is necessary for court proceedings, urgent lockout or eviction risks, imminent deadlines, threats and complex contractual interpretation.

## M1 research reference

I reviewed the public `SPIKIE-24/LLM` repository as a technical reference. Its README describes M1 as a 12-layer, 768-hidden-size, 12-head multi-head-attention Transformer using RoPE, pre-RMSNorm and GELU. Its Phase 2 legal NER task uses character-boundary prediction. The public repository contains README and model notebooks, but not deployable checkpoints or a standalone model package. M1 was not integrated. Its judgment-oriented labels are not rental-agreement labels; adaptation would require matching model/tokenizer assets, a rental-specific annotation schema, representative labelled tenancy documents and separate evaluation. The large local checkpoint and matching tokenizer/model assets are not part of this submission.

## Legal reliability

The source registry currently contains official discovery-portal links only, with no curated, versioned statutory passages. Portal URLs are not treated as legal evidence. As a result, NyayaAI abstains from definitive legal citations. If a passage is later added, the validator checks the retrieved source ID, provision and exact quote. This does not determine whether a rule applies to a particular tenancy or remains legally operative. Unknown jurisdiction, missing evidence and selected high-risk situations produce abstention or lawyer-escalation messages.

## Quality checks, failures and limitations

The code audit passes 17 automated unit tests. Eight synthetic cases (TC01-TC08) were run and their raw outputs captured in DEMO mode. They are deterministic simulations, not genuine AI results, and remain NOT_YET_REVIEWED in the evaluation tracker. The tests cover deposit not returned, no written agreement, disputed deductions, missing jurisdiction, fabricated-law request, suspicious uploaded notice, imminent lockout and conflicting dates. The date-conflict heuristic is intentionally basic and English-oriented. The prototype does not yet provide full field-level extraction or a chronological evidence timeline. Hindi/Hinglish model quality requires live testing. The browser launch was not verified in the audit environment because Streamlit was not installed and package installation was unavailable.

A concrete implementation mistake found during review was that the initial evaluation runner checked for an API key but did not pass it into the pipeline. A requested `--live` run could therefore fall back to DEMO. I fixed the argument passing, added a guard that rejects non-live results in live mode, corrected the documented script import path, and added regression tests.

## Scale and tools

A production version would need a reviewed, jurisdiction- and date-aware corpus of official tenancy laws, source versioning, stronger multilingual extraction, rental-specific annotated data, a chronological evidence ledger and advocate review for legal interpretations. Model providers can be swapped through the provider adapter. Tools used: Antigravity/Gemini for the initial scaffold (as supplied in the project workspace), ChatGPT for code review and implementation fixes, and Python, Streamlit, Pydantic, pypdf, Google GenAI and pytest in the project.
