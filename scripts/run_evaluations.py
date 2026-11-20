from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Make the documented `python scripts/run_evaluations.py ...` command work
# when launched from the repository root on Windows and other platforms.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
from nyayaai.pipeline import capture_raw_output, run_case

load_dotenv(ROOT / ".env")
CASES = ROOT / "data" / "synthetic_cases.json"
EVALUATION = ROOT / "outputs" / "evaluation.csv"

FIELDS = [
    "test_id", "expected_behaviour", "actual_behaviour", "fact_extraction_correctness",
    "citation_validity", "abstention_correctness", "escalation_correctness",
    "unsupported_claims", "pass_fail", "reviewer_notes"
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NyayaAI synthetic evaluation cases.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--live", action="store_true", help="Call Gemini with GEMINI_API_KEY; requires a valid key.")
    mode.add_argument("--demo", action="store_true", help="Run clearly labelled deterministic simulation, not genuine AI.")
    args = parser.parse_args()
    if args.live and not os.getenv("GEMINI_API_KEY"):
        raise SystemExit("GEMINI_API_KEY is missing. Set it in your environment or .env before --live.")

    cases = json.loads(CASES.read_text(encoding="utf-8"))
    rows = []
    for case in cases:
        result = run_case(
            user_text=case["input"], document_text=case.get("document_text", ""),
            jurisdiction=case.get("jurisdiction"),
            api_key=os.getenv("GEMINI_API_KEY") if args.live else None,
            model=os.getenv("GEMINI_MODEL"),
            force_demo=args.demo,
            test_id=case["test_id"],
        )
        if args.live and result.mode != "LIVE_GEMINI":
            raise RuntimeError(
                f"{case['test_id']} was requested in --live mode but ran as {result.mode}; "
                "refusing to label a simulated response as a live model run."
            )
        saved = capture_raw_output(result, {
            "test_id": case["test_id"], "input": case["input"],
            "document_text": case.get("document_text", ""), "jurisdiction": case.get("jurisdiction")
        })
        consistency = result.document_safety.get("case_consistency", {})
        actual = (
            f"state={result.abstention_state}; lawyer={result.human_lawyer_recommended}; "
            f"document_injection={result.document_safety.get('is_suspicious', False)}; "
            f"date_conflict={consistency.get('possible_conflict', False)}; "
            f"mode={result.mode}"
        )
        rows.append({
            "test_id": case["test_id"],
            "expected_behaviour": case["expected"],
            "actual_behaviour": actual,
            "fact_extraction_correctness": "REVIEW_REQUIRED",
            "citation_validity": "NO_CITATIONS_EMITTED" if result.citation_validation.get("citation_count", 0) == 0 else ("PASS" if result.citation_validation.get("all_valid") is True else "FAIL_REVIEW"),
            "abstention_correctness": "REVIEW_REQUIRED",
            "escalation_correctness": "REVIEW_REQUIRED",
            "unsupported_claims": "REVIEW_RAW_OUTPUT",
            "pass_fail": "NOT_YET_REVIEWED",
            "reviewer_notes": f"Output mode={result.mode}; raw file={saved.name}. DEMO output is simulation only." if args.demo else f"Live output captured; manual legal/quality review still required. Raw file={saved.name}"
        })
        print(f"{case['test_id']}: {result.abstention_state} | {result.mode} | saved {saved.name}")

    EVALUATION.parent.mkdir(parents=True, exist_ok=True)
    with open(EVALUATION, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Evaluation tracker written to: {EVALUATION}")
    print("Reminder: NOT_YET_REVIEWED rows must be manually reviewed; do not call them passed.")


if __name__ == "__main__":
    main()
