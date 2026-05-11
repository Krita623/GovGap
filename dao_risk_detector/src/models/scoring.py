from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


ScoreSeverity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
EvidenceType = Literal[
    "trace",
    "reverted_trace",
    "static_decode",
    "llm_text_extraction",
    "system_whitelist",
    "rule_engine",
]


class StrictScoringModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RiskFinding(StrictScoringModel):
    id: str
    title: str
    severity: ScoreSeverity
    description: str
    evidence_type: EvidenceType
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    recommendation: str
    confidence: float = Field(ge=0.0, le=1.0)


class ConflictDetectionScore(StrictScoringModel):
    score: int = Field(ge=0, le=10)
    severity: ScoreSeverity
    summary: str
    disclosed_addresses: list[str] = Field(default_factory=list)
    system_addresses: list[str] = Field(default_factory=list)
    unaccounted_addresses: list[str] = Field(default_factory=list)
    findings: list[RiskFinding] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)


class DepthAnalysisScore(StrictScoringModel):
    score: int = Field(ge=0, le=10)
    severity: ScoreSeverity
    claimed_complexity: Literal["simple", "moderate", "complex", "unknown"]
    actual_max_depth: int = Field(ge=0)
    depth_mismatch: bool
    summary: str
    findings: list[RiskFinding] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)


class FunctionSemanticMatchScore(StrictScoringModel):
    score: int = Field(ge=0, le=10)
    severity: ScoreSeverity
    matched_functions: list[str] = Field(default_factory=list)
    unmatched_functions: list[str] = Field(default_factory=list)
    unknown_selectors: list[str] = Field(default_factory=list)
    claimed_actions: list[str] = Field(default_factory=list)
    actual_actions: list[str] = Field(default_factory=list)
    summary: str
    findings: list[RiskFinding] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)


class OverallScore(StrictScoringModel):
    score: int = Field(ge=0, le=10)
    score_scale: Literal[10] = 10
    risk_level: ScoreSeverity
    score_method: Literal["min_dimension_score_with_severity_cap"]
    summary: str


class FinalMetadata(StrictScoringModel):
    proposal_id: str
    generated_at: str
    chain_id: int | None = None
    simulation_status: Literal["success", "reverted_with_trace", "partial", "failed"]
    trace_source: Literal["simulated_trace", "rpc_debug_trace", "static_decode"]


class HallucinationControls(StrictScoringModel):
    llm_used_for_scoring: Literal[False] = False
    llm_used_for_trace_analysis: Literal[False] = False
    unsupported_claims_allowed: Literal[False] = False
    unknown_fields_preserved_as_unknown: Literal[True] = True


class FinalAuditJSON(StrictScoringModel):
    metadata: FinalMetadata
    overall: OverallScore
    proposal_semantics: dict[str, Any]
    trace_summary: dict[str, Any]
    risk_actions: list[dict[str, Any]]
    dimensions: dict[str, dict[str, Any]]
    risk_findings: list[RiskFinding]
    hallucination_controls: HallucinationControls = Field(default_factory=HallucinationControls)
