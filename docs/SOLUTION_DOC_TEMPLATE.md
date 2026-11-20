# NyayaAI — AI Legal Action Copilot (KukuFM Problem 2)

## Problem and scope
NyayaAI focuses on Indian rental security-deposit disputes. It helps a tenant organise a narrative into a structured case, identify supporting evidence, understand what information is missing, and draft a neutral refund request. It is not designed to cover every area of Indian law.

## How it works
The Streamlit interface accepts English, Hindi or Hinglish text and PDF/TXT supporting documents. A provider adapter calls Gemini when a user supplies an API key; otherwise the interface clearly labels deterministic demo mode. The application separates user-reported facts from document-supported excerpts, flags urgent situations for human assistance, and uses a local source registry plus exact-quote citation validator. The starter registry currently has official portal links but no curated statute passages, so the app abstains from definitive legal citations.

## Human and code boundaries
The language model organises the narrative and drafts plain-language communication. Deterministic code handles document-safety flags, basic escalation patterns, provenance labels, retrieval filters, citation checks and append-only run capture. A qualified lawyer remains necessary for legal interpretation, court proceedings, urgent eviction/lockout, threats, deadlines and complex contracts.

## Quality evidence
Automated unit tests: 14 passed (see `outputs/unit_test_results.txt`). Eight synthetic cases are in `data/synthetic_cases.json`. Add actual live model run outcomes here only after running `python scripts/run_evaluations.py --live`, inspecting each raw JSON file and completing `outputs/evaluation.csv`.

## Failures and limitations
The starter registry contains no verified statutory text; legal answers are therefore withheld. Rule-based escalation can miss edge cases. Citation matching does not prove applicability. PDF text extraction may fail on scans. Hindi/Hinglish output and all live model outputs need manual review. The tool is not hallucination-free, legally certified or a substitute for an advocate.

## Tools used
ChatGPT for project planning/code review; Antigravity/Gemini may be used for local iteration; Python, Streamlit, Pydantic, pypdf and Google GenAI SDK. Update this section to accurately describe your actual use and any observed tool mistake before submission.
