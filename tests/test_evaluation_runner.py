from __future__ import annotations

import json
from pathlib import Path

import scripts.run_evaluations as runner
from nyayaai.schemas import CaseAnalysis, PipelineResult


def _fake_result(test_id: str, mode: str = "LIVE_GEMINI") -> PipelineResult:
    return PipelineResult(
        test_id=test_id,
        model_id="gemini-test",
        mode=mode,
        timestamp="2026-11-20T00:00:00+00:00",
        abstention_state="INSUFFICIENT_EVIDENCE",
        human_lawyer_recommended=False,
        escalation_reasons=[],
        jurisdiction="Delhi",
        retrieved_sources=[],
        citation_validation={"all_valid": None, "citation_count": 0},
        document_safety={},
        parsed_analysis=CaseAnalysis(summary="Test"),
        raw_model_response='{"summary":"Test"}',
        final_response="Test",
    )


def test_live_runner_passes_api_key_and_model(monkeypatch, tmp_path):
    cases = [{"test_id": "TC01", "input": "Example", "expected": "Expected"}]
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps(cases), encoding="utf-8")
    evaluation_path = tmp_path / "evaluation.csv"
    raw_path = tmp_path / "raw"
    monkeypatch.setattr(runner, "CASES", cases_path)
    monkeypatch.setattr(runner, "EVALUATION", evaluation_path)
    monkeypatch.setenv("GEMINI_API_KEY", "test-secret")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")

    received = {}

    def fake_run_case(**kwargs):
        received.update(kwargs)
        return _fake_result(kwargs["test_id"])

    def fake_capture(result, original_input):
        raw_path.mkdir(exist_ok=True)
        path = raw_path / f"{result.test_id}.json"
        path.write_text("{}", encoding="utf-8")
        return path

    monkeypatch.setattr(runner, "run_case", fake_run_case)
    monkeypatch.setattr(runner, "capture_raw_output", fake_capture)
    monkeypatch.setattr("sys.argv", ["run_evaluations.py", "--live"])

    runner.main()

    assert received["api_key"] == "test-secret"
    assert received["model"] == "gemini-test-model"
    assert received["force_demo"] is False
    assert "TC01" in evaluation_path.read_text(encoding="utf-8-sig")


def test_live_runner_rejects_demo_response(monkeypatch, tmp_path):
    cases = [{"test_id": "TC01", "input": "Example", "expected": "Expected"}]
    cases_path = tmp_path / "cases.json"
    cases_path.write_text(json.dumps(cases), encoding="utf-8")
    monkeypatch.setattr(runner, "CASES", cases_path)
    monkeypatch.setattr(runner, "EVALUATION", tmp_path / "evaluation.csv")
    monkeypatch.setenv("GEMINI_API_KEY", "test-secret")
    monkeypatch.setattr(runner, "run_case", lambda **kwargs: _fake_result("TC01", "DEMO"))
    monkeypatch.setattr("sys.argv", ["run_evaluations.py", "--live"])

    try:
        runner.main()
    except RuntimeError as exc:
        assert "refusing to label a simulated response as a live model run" in str(exc)
    else:
        raise AssertionError("A DEMO response must not be accepted in --live mode")
