from __future__ import annotations

from src.models.scoring import (
    ConflictDetectionScore,
    DepthAnalysisScore,
    FunctionSemanticMatchScore,
    OverallScore,
    RiskFinding,
)
from src.modules.scoring.scoring_utils import max_severity


_SEVERITY_CAP = {
    "CRITICAL": 2,
    "HIGH": 4,
    "MEDIUM": 6,
    "LOW": 9,
}

_MATERIAL_ACTIONS = {
    "upgrade",
    "permission_change",
    "proxy_change",
    "selfdestruct",
    "bridge",
    "arbitrary_call",
    "contract_creation",
}


def calculate_overall_score(
    conflict_detection: ConflictDetectionScore,
    depth_analysis: DepthAnalysisScore,
    function_semantic_match: FunctionSemanticMatchScore,
    risk_findings: list[RiskFinding],
) -> OverallScore:
    """Calculate overall score by worst-case risk gating."""

    dimension_scores = [
        conflict_detection.score,
        depth_analysis.score,
        function_semantic_match.score,
    ]
    dimension_severities = [
        conflict_detection.severity,
        depth_analysis.severity,
        function_semantic_match.severity,
    ]
    finding_severities = [
        finding.severity
        for finding in risk_findings
        if finding.severity in {"LOW", "MEDIUM"} or _is_material_finding(finding)
    ]

    if all(score == 10 for score in dimension_scores) and not risk_findings:
        return OverallScore(
            score=10,
            risk_level="LOW",
            score_method="min_dimension_score_with_severity_cap",
            summary="All dimensions scored 10 and no rule-engine findings were generated.",
        )

    base_score = min(dimension_scores)
    highest = max_severity(dimension_severities + finding_severities)
    overall_score = min(base_score, _SEVERITY_CAP[highest])
    return OverallScore(
        score=overall_score,
        risk_level=highest,
        score_method="min_dimension_score_with_severity_cap",
        summary=f"Overall score uses minimum dimension score {base_score} capped by highest severity {highest}.",
    )


def _is_material_finding(finding: RiskFinding) -> bool:
    if finding.severity not in {"HIGH", "CRITICAL"}:
        return False
    for evidence in finding.evidence:
        uncovered = {str(action) for action in evidence.get("uncovered_business_actions", [])}
        actual = {str(action) for action in evidence.get("actual_business_actions", [])}
        unknown_selectors = evidence.get("unknown_selectors", [])
        material_related = evidence.get("material_related_actions", [])
        if uncovered & _MATERIAL_ACTIONS:
            return True
        if actual & _MATERIAL_ACTIONS and "claimed_actions" in evidence:
            return True
        if unknown_selectors and (uncovered & _MATERIAL_ACTIONS or actual & _MATERIAL_ACTIONS):
            return True
        if material_related:
            return True
    return False
