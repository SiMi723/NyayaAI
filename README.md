# NyayaAI — AI Legal Action Copilot

A narrow Streamlit MVP for helping Indian tenants organise rental security-deposit disputes. It supports English/Hindi/Hinglish intake, PDF/TXT text extraction, structured case notes, evidence checklists, a neutral refund-request draft, provenance labels, abstention states, escalation flags and citation checks.

> **Important:** NyayaAI is an informational case-organisation tool, not a law firm. It does not provide legal representation or guarantee legal outcomes. For court matters, imminent eviction/lockout, urgent deadlines, threats or complex agreements, consult a qualified advocate.

## 1. Run locally (Windows PowerShell)

```powershell
cd NyayaAI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your own Gemini API key to `.env`:

```text
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never commit `.env` or share your API key. Launch:

```powershell
python -m streamlit run app.py
```

Open `http://localhost:8501`.

Without a key, the app works in clearly labelled **DEMO MODE** with deterministic simulated outputs. Demo is useful for checking the interface, not for claiming genuine AI performance.

## 2. Run tests

```powershell
python -m pytest -q
```

The current audit run passes 17 automated unit tests. This is code-level testing, not proof of legal accuracy or live-model quality.

## 3. Run the eight synthetic cases

Live Gemini execution (requires `GEMINI_API_KEY` in `.env` or environment):

```powershell
python scripts/run_evaluations.py --live
```

Deterministic simulation only:

```powershell
python scripts/run_evaluations.py --demo
```

Both modes save raw records in `outputs/raw/` and create `outputs/evaluation.csv`. Demo records are explicitly marked as simulations. The evaluation file leaves manual quality fields unreviewed; inspect each output before marking it pass/fail.

## 4. Architecture

- `app.py`: Streamlit interface
- `nyayaai/pipeline.py`: orchestration, abstention and output capture
- `nyayaai/legal_sources.py`: local lexical retrieval
- `nyayaai/citation_validator.py`: source/provision/exact-quote validator
- `nyayaai/safety.py`: document injection detection, provenance and escalation
- `nyayaai/gemini_provider.py`: swappable Gemini provider adapter
- `data/legal_sources.json`: source registry (starter portal entries only)
- `data/synthetic_cases.json`: eight synthetic tests
- `docs/safety_and_evaluation.md`: safeguards, test protocol and limitations

## 5. Important source limitation

The starter source registry contains official portal links but no verified statutory text. These portal-only entries are inactive and are not treated as legal evidence. Consequently, the app abstains from definitive legal citations until reviewed exact source passages are added with jurisdiction, version and effective-date metadata. A matching citation does not prove applicability.

## 6. M1 research reference

The companion `SPIKIE-24/LLM` repository is kept as a read-only research reference. Its README describes M1 as a 12-layer MHA Transformer (hidden size 768, 12 heads, RoPE, pre-RMSNorm, GELU) and Phase 2 NER as character-boundary prediction. The public repository contains notebooks and a README, but no model checkpoints or separate deployable Python package. M1 is **not integrated** in this MVP. Rental-specific entity labels and annotated tenancy documents would be needed before adapting its judgment-trained NER approach.

The large local checkpoint and its matching tokenizer/model files are intentionally not bundled. NyayaAI runs independently of those assets and uses the configurable Gemini adapter when a key is supplied.

## 7. Rebuild the two-page solution document

```powershell
python scripts/build_solution_pdf.py
```

The script writes `NyayaAI_Solution_Document.pdf` in the project root. It uses ReportLab, included in `requirements.txt`.
