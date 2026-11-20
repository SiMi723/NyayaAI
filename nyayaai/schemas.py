from __future__ import annotations

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class Provenance(str, Enum):
    USER_REPORTED = "USER_REPORTED"
    DOCUMENT_SUPPORTED = "DOCUMENT_SUPPORTED"
    SOURCE_VERIFIED = "SOURCE_VERIFIED"
    UNVERIFIED_ALLEGATION = "UNVERIFIED_ALLEGATION"
    UNKNOWN = "UNKNOWN"


class FactRecord(BaseModel):
    field: str
    value: str
    provenance: Provenance
    supporting_text: str | None = None
    notes: str | None = None


class Citation(BaseModel):
    source_id: str
    provision: str = ""
    quote: str = ""


class CaseAnalysis(BaseModel):
    summary: str = ""
    missing_information: list[str] = Field(default_factory=list)
    evidence_checklist: list[str] = Field(default_factory=list)
    practical_steps: list[str] = Field(default_factory=list)
    refund_request_draft: str = ""
    legal_analysis: str = ""
    citations: list[Citation] = Field(default_factory=list)
    facts: list[FactRecord] = Field(default_factory=list)
    model_notes: str = ""


class PipelineResult(BaseModel):
    test_id: str | None = None
    model_id: str
    mode: str
    timestamp: str
    abstention_state: str
    human_lawyer_recommended: bool
    escalation_reasons: list[str] = Field(default_factory=list)
    jurisdiction: str | None = None
    retrieved_sources: list[dict[str, Any]] = Field(default_factory=list)
    citation_validation: dict[str, Any] = Field(default_factory=dict)
    document_safety: dict[str, Any] = Field(default_factory=dict)
    parsed_analysis: CaseAnalysis = Field(default_factory=CaseAnalysis)
    raw_model_response: str
    final_response: str
