# NyayaAI - Solution document drafting checklist

Use this file only as a drafting aid. The submitted two-page document is `NyayaAI_Solution_Document.pdf`; keep its claims consistent with the code, test records and actual deployment status.

## Problem choice and framing
- Name the user and one narrowly scoped everyday legal problem.
- State assumptions and what is out of scope.

## Prototype and approach
- Explain the user journey from intake to a practical output.
- Separate what the language model does, what deterministic code does and when a human/lawyer is required.
- Explain how a compatible model provider can be changed and identify likely cost/scale constraints.

## Legal reliability
- Describe the source registry, retrieval conditions, citation checks, abstention and escalation.
- Do not describe portal links as verified legal passages.

## Quality evidence
- Recorded automated code audit: 17 unit tests passed.
- Eight synthetic cases are provided in `data/synthetic_cases.json`.
- The included eight raw JSON records are deterministic DEMO simulations, not genuine Gemini outputs.
- Do not claim an end-to-end pass rate until genuine live runs are inspected and human-reviewed.

## Failures, limitations and learning
- Include a real implementation mistake or model/tool failure, what evidence exposed it, what was changed and what remains unresolved.
- Distinguish a working UI, a successful API call and a reliable legal answer.

## Tools used
- List only tools actually used.
- State one concrete error or limitation from AI-assisted development and how it was checked/corrected.
