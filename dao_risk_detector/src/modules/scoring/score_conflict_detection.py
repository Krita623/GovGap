from __future__ import annotations

from src.config.known_addresses import SYSTEM_ADDRESS_WHITELIST
from src.models.risk_action import RiskAction, RiskActionType
from src.models.scoring import ConflictDetectionScore, RiskFinding
from src.models.semantics import ProposalSemantics
from src.models.trace import TraceResult
from src.modules.scoring.scoring_utils import (
    action_is_material,
    compact_risk_action,
    covered_business_actions,
    inferred_action_for_risk_action,
    observed_business_action_values,
    severity_for_score,
    uncovered_business_actions,
)


_CRITICAL_UNCOVERED_ACTIONS = {
    RiskActionType.SELFDESTRUCT,
    RiskActionType.UPGRADE,
    RiskActionType.PERMISSION_CHANGE,
    RiskActionType.PROXY_CHANGE,
}

_HIGH_UNCOVERED_ACTIONS = {
    RiskActionType.BRIDGE,
    RiskActionType.ARBITRARY_CALL,
    RiskActionType.CONTRACT_CREATION,
}

_NON_CRITICAL_BUSINESS_ACTIONS = {
    RiskActionType.APPROVAL,
    RiskActionType.TRANSFER,
}


def score_conflict_detection(
    semantics: ProposalSemantics,
    trace: TraceResult,
    risk_actions: list[RiskAction],
) -> ConflictDetectionScore:
    """Score undisclosed objects and hidden execution paths."""

    disclosed = _disclosed_addresses(semantics)
    unique_addresses = set(trace.parsed_trace.unique_addresses if trace.parsed_trace else [])
    system_addresses = sorted(address for address in unique_addresses if _is_system_address(address))
    unaccounted = sorted(address for address in unique_addresses if address not in disclosed and address not in system_addresses)
    claimed_actions = [action.canonical_action for action in semantics.claimed_actions]
    actual_business = observed_business_action_values(risk_actions, trace)
    covered_business = covered_business_actions(claimed_actions, actual_business)
    uncovered_business = uncovered_business_actions(claimed_actions, actual_business)

    unaccounted_actions = [
        action for action in risk_actions if action.to_address in unaccounted or action.from_address in unaccounted
    ]
    uncovered_unaccounted_actions = [
        action
        for action in unaccounted_actions
        if _action_value_for_conflict(action, trace) in uncovered_business
    ]
    has_uncovered_critical = any(action.action_type in _CRITICAL_UNCOVERED_ACTIONS for action in uncovered_unaccounted_actions)
    has_uncovered_high = any(action.action_type in _HIGH_UNCOVERED_ACTIONS for action in uncovered_unaccounted_actions)
    has_uncovered_noncritical_business = any(
        action.action_type in _NON_CRITICAL_BUSINESS_ACTIONS for action in uncovered_unaccounted_actions
    )
    has_uncovered_unknown_only = bool(uncovered_unaccounted_actions) and all(
        action.action_type == RiskActionType.UNKNOWN for action in uncovered_unaccounted_actions
    )
    has_delegatecall_unknown_sensitive = any(
        action.action_type == RiskActionType.DELEGATECALL for action in unaccounted_actions
    ) and bool(uncovered_business & {"upgrade", "permission_change", "proxy_change", "bridge", "arbitrary_call"})
    has_only_wrapper_or_covered_business = bool(unaccounted) and not uncovered_unaccounted_actions

    if not unaccounted:
        score = 10
        summary = "All trace addresses are disclosed or system-whitelisted."
    elif has_uncovered_critical or has_delegatecall_unknown_sensitive:
        score = 2
        summary = "An undisclosed address participates in an uncovered critical business action."
    elif has_uncovered_high:
        score = 4
        summary = "An undisclosed address participates in an uncovered high-risk business action."
    elif has_uncovered_noncritical_business:
        score = 5
        summary = "An undisclosed address participates in an uncovered approval or transfer action."
    elif has_uncovered_unknown_only:
        score = 6
        summary = "Undisclosed addresses include unknown selectors that require review, but no deterministic high-risk business action was confirmed."
    elif has_only_wrapper_or_covered_business and covered_business:
        score = 8
        summary = "Execution includes undisclosed path components, but core business actions match proposal text."
    elif unaccounted and not unaccounted_actions and not actual_business:
        score = 8
        summary = "Trace includes undisclosed execution path components without extracted risk actions."
    else:
        score = 7
        summary = "Trace includes undisclosed addresses without evidence of an uncovered sensitive business action."

    findings = []
    if unaccounted:
        findings.append(
            RiskFinding(
                id="conflict.unaccounted_addresses",
                title="Unaccounted trace addresses",
                severity=severity_for_score(score),
                description="One or more addresses appeared in the trace without direct proposal text disclosure.",
                evidence_type="trace",
                evidence=[
                    {
                        "unaccounted_addresses": unaccounted,
                        "related_actions": [compact_risk_action(action) for action in unaccounted_actions],
                        "covered_business_actions": sorted(covered_business),
                        "uncovered_business_actions": sorted(uncovered_business),
                        "material_related_actions": [
                            compact_risk_action(action) for action in unaccounted_actions if action_is_material(action)
                        ],
                    }
                ],
                recommendation=_recommendation_for_score(score),
                confidence=0.9,
            )
        )

    evidence = [
        {
            "disclosed_addresses": sorted(disclosed),
            "trace_unique_addresses": sorted(unique_addresses),
            "system_addresses": system_addresses,
            "unaccounted_addresses": unaccounted,
            "covered_business_actions": sorted(covered_business),
            "uncovered_business_actions": sorted(uncovered_business),
        }
    ]

    return ConflictDetectionScore(
        score=score,
        severity=severity_for_score(score),
        summary=summary,
        disclosed_addresses=sorted(disclosed),
        system_addresses=system_addresses,
        unaccounted_addresses=unaccounted,
        findings=findings,
        evidence=evidence,
    )


def _disclosed_addresses(semantics: ProposalSemantics) -> set[str]:
    addresses = {item.address.lower() for item in semantics.disclosed_addresses}
    addresses.update(entity.address.lower() for entity in semantics.disclosed_entities if entity.address)
    return addresses


def _is_system_address(address: str) -> bool:
    return address.lower() in SYSTEM_ADDRESS_WHITELIST


def _recommendation_for_score(score: int) -> str:
    if score <= 2:
        return "Pause or escalate manual review because an uncovered critical business action is linked to an undisclosed address."
    if score <= 5:
        return "Review whether the proposal text sufficiently discloses the business action and its counterparty."
    return "Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text."


def _action_value_for_conflict(action: RiskAction, trace: TraceResult) -> str | None:
    inferred = inferred_action_for_risk_action(action, trace)
    if inferred:
        return inferred
    evidence_source = getattr(action.evidence_source, "value", action.evidence_source)
    if action.action_type == RiskActionType.UNKNOWN and str(evidence_source) != "reverted_trace":
        return "unknown"
    return None
