# NyayaAI — AI Legal Action Copilot

**Making everyday legal problems easier to understand and act upon.**

[Live Prototype](https://nyayaai-simi.streamlit.app/) · [GitHub Repository](https://github.com/SiMi723/NyayaAI)

---

## 1. Overview

NyayaAI is an AI-powered legal action copilot designed to help ordinary people in India navigate everyday rental security-deposit disputes.

Many tenants face difficulties when landlords withhold security deposits, impose disputed painting or repair deductions, or fail to communicate clearly after a tenancy ends. Understanding the situation, organising evidence and preparing a formal response can be intimidating, particularly without access to affordable legal assistance.

NyayaAI addresses this problem through a focused, conversational interface that helps tenants organise their accounts, identify missing information, understand practical next steps and prepare a neutral security-deposit refund request.

**The current prototype focuses specifically on rental security-deposit disputes rather than attempting to cover every area of Indian law.**

> **Legal Disclaimer:** NyayaAI is an informational case-organisation tool, not a law firm. It does not provide legal representation, guarantee legal outcomes or replace a qualified advocate. Legal information and generated drafts require independent verification and human review.

## 2. Live Application

**Access the deployed application:**  
https://nyayaai-simi.streamlit.app/

The prototype is built using Streamlit and supports two operating modes:

- **LIVE mode:** Uses the Google Gemini API for language understanding, case organisation and draft generation.
- **DEMO mode:** Uses deterministic simulated responses when an API key is unavailable. Demo outputs are intended for interface and workflow testing, not as evidence of genuine AI performance.

A model-provider abstraction keeps the language-model integration replaceable, allowing other providers to be introduced with minimal changes to the application workflow.

## 3. Key Features

### Multilingual Case Intake
- Accepts free-text descriptions in English, Hindi and Hinglish.
- Collects the property location, deposit amount, tenancy dates and landlord's stated reasons for deductions.
- Converts an unstructured narrative into an organised case representation.

### Document Analysis
- Supports PDF and TXT uploads.
- Extracts selectable text from rental agreements, notices and supporting documents.
- Displays extracted text for user inspection.
- Treats uploaded content as untrusted evidence rather than executable instructions.
- Reports when a PDF contains no extractable text.

### Evidence Organisation
- Separates user-reported facts from document-supported information.
- Identifies missing information and supporting evidence.
- Helps users organise payment records, messages, agreements and handover-related evidence.

### Practical Action Support
- Generates a structured case summary.
- Identifies unanswered questions and information gaps.
- Suggests practical evidence-collection steps.
- Prepares a neutral, personalised security-deposit refund request.

### Legal Reliability and Safety
- Uses an explicit legal-source registry.
- Excludes inactive portal-only records from legal evidence retrieval.
- Validates retrieved source IDs, provision identifiers and exact quotations.
- Supports abstention when legal evidence or jurisdiction is insufficient.
- Flags selected high-risk situations for qualified legal assistance.
- Provides transparency about uncertainty and the limitations of automated checks.

## 4. How It Works

The application follows a modular processing pipeline:

1. **User Input:** The tenant describes the dispute and provides the property jurisdiction.
2. **Document Processing:** Uploaded PDF/TXT files are parsed and their extracted content is treated as untrusted evidence.
3. **Source Retrieval:** The local registry is searched for eligible legal passages.
4. **AI Processing:** Gemini organises the narrative, identifies missing information and generates practical communication drafts.
5. **Safety Validation:** Deterministic Python checks apply provenance labels, selected escalation rules, citation validation and document-safety checks.
6. **Response Generation:** The application presents the case summary, evidence checklist, next steps and refund-request draft.
7. **Raw Output Capture:** Execution records can be saved with timestamps and model-mode metadata.

### AI vs. Deterministic Code vs. Human Review

| Component | Responsibility |
|---|---|
| Gemini | Language understanding, summarisation and drafting |
| Python | Document parsing, retrieval filtering, provenance, citation checks, escalation heuristics and raw-output capture |
| Human reviewer | Verification of facts, evidence and generated drafts |
| Qualified advocate | Legal interpretation, formal proceedings and complex or urgent matters |

## 5. Preventing Legal Hallucinations

Legal reliability is a central design consideration.

NyayaAI does not treat an official website link as sufficient evidence for a statutory claim. Its starter legal-source registry contains official discovery portals but currently has no curated, verified statutory passages.

Consequently, the application abstains from definitive statutory citations when supporting legal text is unavailable.

The safeguards include:

- Restricting legal citations to retrieved source records.
- Checking source IDs, provision identifiers and exact quoted text.
- Distinguishing source verification from legal applicability.
- Requesting jurisdiction rather than assuming which state law governs.
- Flagging selected situations that require professional legal assistance.
- Treating uploaded documents as untrusted input.

A successfully validated quotation does not establish that a provision applies to a particular tenancy or remains legally operative. Human legal review remains necessary.

## 6. Evaluation and Testing

Since Problem 2 does not provide an input pack, eight synthetic test cases were created to evaluate the prototype's intended behaviour.

| Test ID | Scenario |
|---|---|
| TC01 | Security deposit not returned |
| TC02 | Rental arrangement without a written agreement |
| TC03 | Disputed repair and painting deductions |
| TC04 | Missing property jurisdiction |
| TC05 | User requests fabricated legal provisions |
| TC06 | Suspicious legal claims and embedded instructions in an uploaded notice |
| TC07 | Imminent forced lockout |
| TC08 | Conflicting tenancy dates |

**Automated testing:** 17 unit tests passed in the development audit.

**End-to-end outputs:** Eight recorded runs are included under `outputs/raw/`. These are deterministic DEMO simulations, not genuine Gemini responses. They have not been manually quality-scored and should not be interpreted as live-model accuracy results.

The evaluation tracker is maintained at `outputs/evaluation.csv`.

### Known Failure Cases and Limitations

- The current legal registry does not contain verified statutory passages.
- The date-conflict and escalation detectors use basic heuristics and may miss unusual wording.
- Hindi/Hinglish response quality requires further live-model evaluation.
- Scanned or image-only PDFs are not supported because OCR is not implemented.
- Voice input is not currently implemented.
- Complete field-level extraction and a chronological evidence timeline remain future improvements.
- Citation validation does not establish legal applicability.
- Gemini may still generate unsupported factual statements; outputs require human inspection.

## 7. Technology Stack

| Area | Technologies |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| Language Model | Google Gemini API |
| Data Validation | Pydantic |
| Document Processing | pypdf |
| Configuration | python-dotenv |
| Automated Testing | pytest |
| Version Control | Git and GitHub |

## 8. Installation and Local Setup

### Prerequisites
- Python 3.10 or newer
- Git
- A Google Gemini API key for LIVE mode

### Windows PowerShell

Clone the repository:

```powershell
git clone https://github.com/SiMi723/NyayaAI.git
cd NyayaAI
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Configure environment variables:

```powershell
Copy-Item .env.example .env
```

Add your own API key to `.env`:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

**Security:** Never commit `.env`, API keys or credentials to GitHub.

Launch the application:

```powershell
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

Without an API key, the application starts in clearly labelled DEMO mode.

## 9. Running Tests and Evaluations

Run automated unit tests:

```powershell
python -m pytest -q
```

Run the eight synthetic cases in DEMO mode:

```powershell
python scripts/run_evaluations.py --demo
```

Run the cases using Gemini LIVE mode:

```powershell
python scripts/run_evaluations.py --live
```

LIVE execution requires a valid API key and an available model endpoint.

Execution records are saved in `outputs/raw/`, while evaluation tracking is maintained in `outputs/evaluation.csv`.

Raw outputs are append-only. Human-review fields should only be marked complete after inspecting the corresponding records.

## 10. Project Structure

```text
NyayaAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── nyayaai/
│   ├── gemini_provider.py
│   ├── pipeline.py
│   ├── legal_sources.py
│   ├── citation_validator.py
│   ├── safety.py
│   └── schemas.py
│
├── data/
│   ├── legal_sources.json
│   └── synthetic_cases.json
│
├── tests/
│   ├── test_citations.py
│   ├── test_evaluation_runner.py
│   ├── test_pipeline.py
│   └── test_safety.py
│
├── scripts/
│   ├── run_evaluations.py
│   └── build_solution_pdf.py
│
├── outputs/
│   ├── raw/
│   ├── evaluation.csv
│   └── unit_test_results.txt
│
└── docs/
    ├── architecture.md
    ├── safety_and_evaluation.md
    ├── SOLUTION_DOC.md
    └── SOLUTION_DOC_TEMPLATE.md
```

## 11. Future Development

Potential improvements include:

- Curating a reviewed, jurisdiction-specific corpus of current Indian tenancy laws.
- Improving structured extraction of deposit amounts, dates, parties and deductions.
- Introducing chronological evidence timelines.
- Adding OCR for scanned rental agreements and notices.
- Supporting voice-based intake and improved multilingual interactions.
- Expanding evaluation with manually reviewed real-world scenarios.
- Strengthening post-generation validation across every user-visible output.
- Introducing advocate review workflows and additional model providers.

## 12. Development Tools and Acknowledgements

This prototype was developed with assistance from:

- **Antigravity and Gemini:** Initial application scaffolding and development assistance.
- **ChatGPT:** Technical planning, code review, debugging and implementation support.
- **Python and Streamlit:** Application implementation.
- **Google Gemini API:** Configurable language-model integration.

One implementation issue identified during development was an API-key hand-off bug in the initial evaluation runner, which could cause a requested LIVE evaluation to fall back to DEMO mode. The issue was corrected, regression tests were added and the updated automated test suite passed.

The project was developed through iterative implementation and testing, with explicit attention to honest capability claims and legal-safety limitations.

---

**NyayaAI — Helping people organise their legal problems, understand their options and take informed next steps.**

*Built as part of the Kuku AI Generalist Assignment — Problem 2: Build an AI Lawyer.*
