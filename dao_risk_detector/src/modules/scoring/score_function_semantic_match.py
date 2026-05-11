from __future__ import annotations

from src.models.risk_action import RiskAction, RiskActionType
from src.models.scoring import FunctionSemanticMatchScore, RiskFinding
from src.models.semantics import ProposalSemantics
from src.models.trace import TraceResult
from src.modules.scoring.scoring_utils import (
    compact_risk_action,
    observed_business_action_values,
    semantic_score_for_actions,
    severity_for_score,
    wrapper_action_values,
)


def score_function_semantic_match(
    semantics: ProposalSemantics,
    trace: TraceResult,
    risk_actions: list[RiskAction],
) -> FunctionSemanticMatchScore:
    """Score mismatch between stated actions and deterministic payload actions."""

    claimed_actions = [action.canonical_action for action in semantics.claimed_actions]
    actual_business_actions = observed_business_action_values(risk_actions, trace)
    wrapper_actions = wrapper_action_values(risk_actions)
    decoded_functions = set(trace.parsed_trace.decoded_functions if trace.parsed_trace else [])
    unknown_selectors = sorted(
        {
            action.function_selector or "unknown"
            for action in risk_actions
            if action.action_type == RiskActionType.UNKNOWN
        }
    )

    score, summary, matched, unmatched_actual = semantic_score_for_actions(claimed_actions, actual_business_actions)
    if score == 10 and wrapper_actions:
        score = 9
        summary = "Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch."

    findings = []
    if score < 8:
        findings.append(
            RiskFinding(
                id="semantic.function_mismatch",
                title="Claimed actions do not fully match trace actions",
                severity=severity_for_score(score),
                description=summary,
                evidence_type="rule_engine",
                evidence=[
                    {
                        "claimed_actions": claimed_actions,
                        "actual_business_actions": sorted(actual_business_actions),
                        "wrapper_actions": sorted(wrapper_actions),
                        "decoded_functions": sorted(decoded_functions),
                        "unknown_selectors": unknown_selectors,
                    }
                ],
                recommendation="Compare proposal action wording with decoded functions and risk actions before relying on the text.",
                confidence=0.9,
            )
        )

    return FunctionSemanticMatchScore(
        score=score,
        severity=severity_for_score(score),
        matched_functions=sorted(decoded_functions),
        unmatched_functions=sorted(unmatched_actual),
        unknown_selectors=unknown_selectors,
        claimed_actions=claimed_actions,
        actual_actions=sorted(actual_business_actions),
        summary=summary,
        findings=findings,
        evidence=[
            {
                "claimed_actions": [action.model_dump() for action in semantics.claimed_actions],
                "actual_risk_actions": [compact_risk_action(action) for action in risk_actions],
                "actual_business_actions": sorted(actual_business_actions),
                "wrapper_actions": sorted(wrapper_actions),
                "decoded_functions": sorted(decoded_functions),
            }
        ],
    )
