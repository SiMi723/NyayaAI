from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from nyayaai.pipeline import capture_raw_output, run_case

load_dotenv()
ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="NyayaAI | Rental Deposit Copilot", page_icon="⚖️", layout="wide")

st.title("⚖️ NyayaAI — AI Legal Action Copilot")
st.caption("A cautious assistant for organising Indian rental security-deposit disputes.")
st.warning(
    "NyayaAI is an informational case-organisation tool, not a law firm. It does not provide formal legal advice or representation. "
    "For court proceedings, urgent eviction/lockout threats, imminent deadlines or threats, contact a qualified advocate promptly."
)

with st.sidebar:
    st.header("Configuration & model status")
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input("Google Gemini API key", value=env_key, type="password", help="Key stays in this local session unless you add it to your own .env file. Never share it or commit it.")
    model = st.text_input("Gemini model", value=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    live = bool(api_key.strip())
    if live:
        st.success(f"LIVE AI MODE — {model}")
    else:
        st.warning("DEMO MODE — deterministic simulated outputs; not genuine AI results.")
    st.caption("For persistent local configuration, copy .env.example to .env and add GEMINI_API_KEY.")
    st.divider()
    st.markdown("**Legal-source policy**")
    st.caption("The starter registry contains official portal links only, not verified statute passages. NyayaAI therefore abstains from definitive legal citations until exact source text is curated and checked.")

if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "document_name" not in st.session_state:
    st.session_state.document_name = None

intake_tab, docs_tab, result_tab, safety_tab = st.tabs([
    "1. Intake chat", "2. Document analysis", "3. Case & action plan", "4. Reliability checks"
])

with intake_tab:
    st.subheader("Describe your rental deposit dispute")
    st.write("You can write in English, Hindi or Hinglish. Include the city/state, deposit amount, dates and what the landlord said.")
    problem = st.text_area("Your situation", height=180, placeholder="Example: Landlord in Pune is not returning my ₹30,000 deposit after I vacated...")
    jurisdiction = st.text_input("Property city and state", placeholder="e.g. Pune, Maharashtra")
    if st.button("Build my case", type="primary", disabled=not problem.strip()):
        with st.spinner("Organising your case and checking available sources..."):
            try:
                result = run_case(user_text=problem, document_text=st.session_state.document_text,
                                  jurisdiction=jurisdiction or None, api_key=api_key or None,
                                  model=model, force_demo=not live)
                st.session_state.last_result = result
                st.success("Case organised. Review the result in tab 3.")
            except Exception as exc:
                st.error(f"The model call failed: {exc}. No legal conclusion has been created. You can retry or use DEMO mode.")

with docs_tab:
    st.subheader("Upload an agreement, notice or supporting document")
    uploaded = st.file_uploader("Choose PDF or TXT", type=["pdf", "txt"])
    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".pdf"):
                from pypdf import PdfReader
                import io
                reader = PdfReader(io.BytesIO(uploaded.getvalue()))
                extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
            else:
                extracted = uploaded.getvalue().decode("utf-8", errors="replace")
            st.session_state.document_text = extracted[:18000]
            st.session_state.document_name = uploaded.name
            if extracted.strip():
                st.success(f"Loaded {uploaded.name}. Extracted {len(extracted)} characters.")
                st.text_area("Extracted text preview (read-only copy)", value=extracted[:5000], height=180, disabled=True)
            else:
                st.warning(
                    "The file was opened, but no extractable text was found. "
                    "It may be a scanned/image-only or protected PDF. OCR is not included, "
                    "so do not treat this as a successful document analysis."
                )
            st.caption("Uploaded content is treated as untrusted evidence. Embedded instructions are not followed.")
        except Exception as exc:
            st.error(f"Could not read this file: {exc}")
    if st.session_state.document_name:
        st.info(f"Current document: {st.session_state.document_name}")
    if st.button("Clear uploaded document"):
        st.session_state.document_text = ""
        st.session_state.document_name = None
        st.rerun()

with result_tab:
    st.subheader("Structured case and next steps")
    if st.session_state.last_result is None:
        st.info("Submit your situation in the Intake chat tab to build the case.")
    else:
        result = st.session_state.last_result
        st.markdown(result.final_response)
        st.divider()
        st.markdown("**Fact provenance**")
        for fact in result.parsed_analysis.facts:
            st.markdown(f"- `{fact.provenance.value}` — {fact.field}: {fact.value[:240]}")
        st.markdown("**Case status**")
        st.code(result.abstention_state)
        if result.human_lawyer_recommended:
            st.error("Human lawyer escalation recommended: " + "; ".join(result.escalation_reasons))
        if st.button("Save raw run record", type="primary"):
            saved = capture_raw_output(result, {
                "user_problem": "Stored in the current Streamlit session; add test input in your local run log if needed.",
                "document_name": st.session_state.document_name,
                "jurisdiction": result.jurisdiction,
            })
            st.success(f"Append-only run record saved: {saved.relative_to(ROOT)}")
            if result.mode == "DEMO":
                st.warning("This raw record is a DEMO simulation, not a genuine AI response.")

with safety_tab:
    st.subheader("How NyayaAI handles legal reliability")
    st.markdown("""
    - **No invented laws:** the model may cite only source IDs and exact passages retrieved from the local registry.
    - **Citation validation:** source ID, provision and exact quoted text are checked. Applicability is not established by matching text alone.
    - **Abstention:** if jurisdiction or source evidence is missing, the app says so instead of guessing.
    - **Provenance:** user statements and uploaded-document excerpts are kept separate from verified sources.
    - **Human escalation:** court matters, imminent lockouts/deadlines, threats and complex contract disputes are flagged.
    - **Document safety:** uploaded text is treated as untrusted evidence, not as instructions.
    """)
    st.info("Starter limitation: official legal portals are listed, but no statute or judgment text is preloaded. Definitive legal citations remain disabled until a reviewer adds exact, current source passages with jurisdiction and version metadata.")
    st.caption("Synthetic test cases are in data/synthetic_cases.json. See docs/safety_and_evaluation.md for test instructions.")
