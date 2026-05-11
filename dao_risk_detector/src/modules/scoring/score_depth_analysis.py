from __future__ import annotations

from src.models.risk_action import RiskAction, RiskActionType
from src.models.scoring import DepthAnalysisScore, RiskFinding
from src.models.semantics import ProposalSemantics
from src.models.trace import TraceResult
from src.modules.scoring.scoring_utils import (
    action_is_material,
    compact_risk_action,
    observed_business_action_values,
    semantic_score_for_actions,
    severity_for_score,
    uncovered_business_actions,
)


_COMPLEXITY_EXPECTED_DEPTH = {
    "simple": 2,
    "moderate": 5,
    "complex": 8,
}

_SENSITIVE_DEPTH_ACTIONS = {
    "upgrade",
    "permission_change",
    "proxy_change",
    "selfdestruct",
    "bridge",
    "arbitrary_call",
    "contract_creation",
    "unknown",
}


def score_depth_analysis(
    semantics: ProposalSemantics,
    trace: TraceResult,
    risk_actions: list[RiskAction],
) -> DepthAnalysisScore:
    """Score hidden complexity from trace depth and indirect execution patterns."""

    parsed = trace.parsed_trace
    max_depth = parsed.max_depth if parsed else 0
    delegatecall_count = parsed.delegatecall_count if parsed else 0
    claimed = semantics.claimed_complexity.level
    claimed_actions = [action.canonical_action for action in semantics.claimed_actions]
    actual_business = observed_business_action_values(risk_actions, trace)
    semantic_score, _, _, _ = semantic_score_for_actions(claimed_actions, actual_business)
    uncovered_business = uncovered_business_actions(claimed_actions, actual_business)
    has_sensitive_business = bool(actual_business & _SENSITIVE_DEPTH_ACTIONS)
    has_uncovered_sensitive_business = bool(uncovered_business & _SENSITIVE_DEPTH_ACTIONS)
    has_material_actions = any(action_is_material(action) for action in risk_actions)
    delegatecall_sensitive = delegatecall_count > 0 and has_uncovered_sensitive_business
    severe_mismatch = max_depth > 12 and (has_uncovered_sensitive_business or has_material_actions) and claimed in {"simple", "moderate", "unknown"}
    business_matches = semantic_score >= 8

    if severe_mismatch:
        score = 2
        summary = "Trace depth is extreme and includes an uncovered sensitive business action."
    elif business_matches and max_depth <= 4:
        score = 9 if claimed in {"moderate", "complex", "unknown"} else 8
        summary = "Core business actions match proposal text; observed wrapper depth is within a normal review range."
    elif claimed == "unknown":
        if max_depth <= 5:
            score = 9
            summary = "Text complexity is unknown; observed trace depth is low to moderate."
        elif max_depth <= 8:
            score = 6 if has_sensitive_business else 8
            summary = "Text complexity is unknown; observed trace depth is moderately deep."
        elif max_depth <= 12:
            score = 5
            summary = "Text complexity is unknown; observed trace depth is high."
        else:
            score = 4 if has_sensitive_business else 5
            summary = "Text complexity is unknown; observed trace depth is very high."
    else:
        expected = _COMPLEXITY_EXPECTED_DEPTH[claimed]
        delta = max_depth - expected
        if delta <= 0:
            score = 10
            summary = "Observed trace depth is consistent with the claimed complexity."
        elif claimed == "simple" and max_depth > 8:
            score = 3 if has_uncovered_sensitive_business else 5
            summary = "Text claims simple complexity but trace depth is high."
        elif claimed == "moderate" and max_depth > 12:
            score = 4 if has_uncovered_sensitive_business else 5
            summary = "Text claims moderate complexity but trace depth is very high."
        elif claimed == "complex" and max_depth > 12:
            score = 6 if has_uncovered_sensitive_business else 7
            summary = "Text claims complex execution but trace depth is still deeper than expected."
        elif business_matches and max_depth <= 8:
            score = 7 if has_sensitive_business else 8
            summary = "Core business actions match proposal text; additional wrapper depth is a review complexity signal."
        elif 2 <= delta <= 3:
            score = 7
            summary = "Observed trace depth is moderately deeper than claimed."
        else:
            score = 6 if delta == 1 else 5
            summary = "Observed trace depth exceeds claimed complexity."

    depth_mismatch = claimed != "unknown" and max_depth > _COMPLEXITY_EXPECTED_DEPTH[claimed]
    findings = []
    if score < 8:
        findings.append(
            RiskFinding(
                id="depth.complexity_mismatch",
                title="Trace complexity exceeds textual complexity disclosure",
                severity=severity_for_score(score),
                description=summary,
                evidence_type="trace",
                evidence=[
                    {
                        "claimed_complexity": claimed,
                        "actual_max_depth": max_depth,
                        "delegatecall_count": delegatecall_count,
                        "business_actions_match": business_matches,
                        "uncovered_business_actions": sorted(uncovered_business),
                        "delegatecall_sensitive": delegatecall_sensitive,
                        "high_risk_actions": [
                            compact_risk_action(action) for action in risk_actions if action_is_material(action)
                        ],
                    }
                ],
                recommendation="Review whether the proposal text should describe the actual call depth or indirect execution paths.",
                confidence=0.9,
            )
        )

    return DepthAnalysisScore(
        score=score,
        severity=severity_for_score(score),
        claimed_complexity=claimed,
        actual_max_depth=max_depth,
        depth_mismatch=depth_mismatch,
        summary=summary,
        findings=findings,
        evidence=[
            {
                "claimed_complexity": semantics.claimed_complexity.model_dump(),
                "actual_max_depth": max_depth,
                "delegatecall_count": delegatecall_count,
                "business_actions_match": business_matches,
                "actual_business_actions": sorted(actual_business),
                "uncovered_business_actions": sorted(uncovered_business),
            }
        ],
    )
