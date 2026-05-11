from __future__ import annotations

from src.models.risk_action import RiskAction, RiskActionType, Severity
from src.models.scoring import ScoreSeverity
from src.models.trace import TraceResult


_SEVERITY_ORDER: dict[ScoreSeverity, int] = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4,
}


def severity_for_score(score: int) -> ScoreSeverity:
    if score >= 8:
        return "LOW"
    if score >= 6:
        return "MEDIUM"
    if score >= 3:
        return "HIGH"
    return "CRITICAL"


def max_severity(severities: list[ScoreSeverity]) -> ScoreSeverity:
    return max(severities or ["LOW"], key=lambda severity: _SEVERITY_ORDER[severity])


def risk_action_severity(action: RiskAction) -> ScoreSeverity:
    mapping: dict[Severity, ScoreSeverity] = {
        Severity.NONE: "LOW",
        Severity.LOW: "LOW",
        Severity.MEDIUM: "MEDIUM",
        Severity.HIGH: "HIGH",
        Severity.CRITICAL: "CRITICAL",
    }
    return mapping[action.severity_hint]


def high_risk_action_types() -> set[RiskActionType]:
    return {
        RiskActionType.UPGRADE,
        RiskActionType.PERMISSION_CHANGE,
        RiskActionType.TRANSFER,
        RiskActionType.BRIDGE,
        RiskActionType.ARBITRARY_CALL,
        RiskActionType.PROXY_CHANGE,
        RiskActionType.DELEGATECALL,
        RiskActionType.SELFDESTRUCT,
        RiskActionType.CONTRACT_CREATION,
    }


_BUSINESS_ACTIONS = {
    RiskActionType.APPROVAL,
    RiskActionType.TRANSFER,
    RiskActionType.UPGRADE,
    RiskActionType.PERMISSION_CHANGE,
    RiskActionType.PROXY_CHANGE,
    RiskActionType.BRIDGE,
    RiskActionType.SELFDESTRUCT,
    RiskActionType.ARBITRARY_CALL,
    RiskActionType.UNKNOWN,
    RiskActionType.CONTRACT_CREATION,
}

_WRAPPER_ACTIONS = {
    RiskActionType.DELEGATECALL,
    RiskActionType.MULTICALL,
}

_MATERIAL_ACTIONS = {
    RiskActionType.UPGRADE,
    RiskActionType.PERMISSION_CHANGE,
    RiskActionType.PROXY_CHANGE,
    RiskActionType.BRIDGE,
    RiskActionType.SELFDESTRUCT,
    RiskActionType.ARBITRARY_CALL,
    RiskActionType.CONTRACT_CREATION,
}

_CLAIMED_TO_ACTUAL = {
    "approval": {"approval"},
    "transfer": {"transfer"},
    "treasury_operation": {"transfer", "approval"},
    "upgrade": {"upgrade", "proxy_change"},
    "role_change": {"permission_change", "proxy_change"},
    "bridge": {"bridge"},
    "governance_proposal_creation": set(),
    "contract_creation": {"contract_creation"},
    "parameter_update": {"parameter_update"},
    "maintenance": set(),
    "unknown": set(),
}

_LOW_RISK_CLAIMS = {"approval", "parameter_update", "maintenance", "treasury_operation"}
_CRITICAL_BUSINESS = {"upgrade", "permission_change", "proxy_change", "selfdestruct"}
_HIGH_BUSINESS = {"bridge", "arbitrary_call", "contract_creation"}
_UNKNOWN_BUSINESS = {"unknown"}


def is_wrapper_action(action_type: RiskActionType) -> bool:
    return action_type in _WRAPPER_ACTIONS


def is_business_action(action_type: RiskActionType) -> bool:
    return action_type in _BUSINESS_ACTIONS


def business_action_values(risk_actions: list[RiskAction]) -> set[str]:
    return {
        _business_action_value(action)
        for action in risk_actions
        if is_business_action(action.action_type)
    }


def observed_business_action_values(risk_actions: list[RiskAction], trace: TraceResult | None = None) -> set[str]:
    """Return deterministic business actions observed from risk actions and decoded trace functions.

    Proxy/controller traces often contain an undecoded outer CALL and a decoded
    inner DELEGATECALL with the same selector. Treat the decoded trace function
    as the stronger local fact so normal execution wrappers do not become
    false unknown-sensitive findings.
    """

    selector_to_action = _selector_to_decoded_action(trace)
    values: set[str] = set()
    for action in risk_actions:
        if action.action_type == RiskActionType.UNKNOWN:
            inferred = selector_to_action.get((action.function_selector or "").lower())
            if inferred:
                values.add(inferred)
            elif str(getattr(action.evidence_source, "value", action.evidence_source)) != "reverted_trace":
                values.add("unknown")
            continue
        if is_business_action(action.action_type):
            values.add(_business_action_value(action))

    values.update(selector_to_action.values())
    return values


def wrapper_action_values(risk_actions: list[RiskAction]) -> set[str]:
    return {
        action.action_type.value
        for action in risk_actions
        if is_wrapper_action(action.action_type)
    }


def business_actions(risk_actions: list[RiskAction]) -> list[RiskAction]:
    return [action for action in risk_actions if is_business_action(action.action_type)]


def wrapper_actions(risk_actions: list[RiskAction]) -> list[RiskAction]:
    return [action for action in risk_actions if is_wrapper_action(action.action_type)]


def claimed_action_values(claimed_actions: list[str]) -> set[str]:
    return {action for action in claimed_actions if action and action != "unknown"}


def covered_business_actions(claimed_actions: list[str], actual_business_actions: set[str]) -> set[str]:
    covered: set[str] = set()
    for claimed in claimed_actions:
        covered.update(actual for actual in actual_business_actions if actual in _CLAIMED_TO_ACTUAL.get(claimed, set()))
    return covered


def uncovered_business_actions(claimed_actions: list[str], actual_business_actions: set[str]) -> set[str]:
    return set(actual_business_actions) - covered_business_actions(claimed_actions, actual_business_actions)


def has_material_business_gap(claimed_actions: list[str], actual_business_actions: set[str]) -> bool:
    uncovered = uncovered_business_actions(claimed_actions, actual_business_actions)
    if uncovered & _MATERIAL_ACTION_VALUES:
        return True
    return _low_risk_claim_with_sensitive_actual(claimed_actions, actual_business_actions)


def semantic_score_for_actions(claimed_actions: list[str], actual_business_actions: set[str]) -> tuple[int, str, set[str], set[str]]:
    covered = covered_business_actions(claimed_actions, actual_business_actions)
    uncovered = set(actual_business_actions) - covered
    claims = claimed_action_values(claimed_actions)

    if not actual_business_actions:
        return 10, "No deterministic business action was extracted from the trace.", covered, uncovered
    if _low_risk_claim_with_sensitive_actual(claimed_actions, actual_business_actions):
        return 2, "Text claims a low-risk action while the trace includes a sensitive business action.", covered, uncovered
    if uncovered & _CRITICAL_BUSINESS:
        return 2, "Trace includes an unclaimed critical business action.", covered, uncovered
    if uncovered & _HIGH_BUSINESS:
        return 3, "Trace includes an unclaimed high-risk business action.", covered, uncovered
    if uncovered & _UNKNOWN_BUSINESS and covered:
        return 7, "Claimed business actions match known extracted actions; additional unknown selectors need review.", covered, uncovered
    if uncovered & _UNKNOWN_BUSINESS:
        return 6, "Trace includes unknown selectors that need review, but no deterministic critical business action was confirmed.", covered, uncovered
    if actual_business_actions.issubset(covered) and covered:
        return 10, "Claimed business actions match extracted business actions.", covered, uncovered
    if covered and uncovered <= {"approval", "transfer"}:
        return 7, "Claimed business actions partially match; extra non-critical business actions need review.", covered, uncovered
    if claims:
        return 4, "Claimed business action categories differ from extracted business actions.", covered, uncovered
    return 6, "Proposal text does not disclose canonical business actions; extracted actions need review.", covered, uncovered


def action_is_uncovered(action: RiskAction, claimed_actions: list[str], actual_business_actions: set[str]) -> bool:
    if not is_business_action(action.action_type):
        return False
    return _business_action_value(action) in uncovered_business_actions(claimed_actions, actual_business_actions)


def action_is_material(action: RiskAction) -> bool:
    return action.action_type in _MATERIAL_ACTIONS


def _low_risk_claim_with_sensitive_actual(claimed_actions: list[str], actual_business_actions: set[str]) -> bool:
    uncovered = uncovered_business_actions(claimed_actions, actual_business_actions)
    return bool(set(claimed_actions) & _LOW_RISK_CLAIMS and uncovered & (_CRITICAL_BUSINESS | _HIGH_BUSINESS))


def _business_action_value(action: RiskAction) -> str:
    if action.action_type == RiskActionType.UNKNOWN:
        return "unknown"
    return action.action_type.value


def inferred_action_for_risk_action(action: RiskAction, trace: TraceResult | None = None) -> str | None:
    if action.action_type != RiskActionType.UNKNOWN:
        return _business_action_value(action) if is_business_action(action.action_type) else None
    return _selector_to_decoded_action(trace).get((action.function_selector or "").lower())


def _selector_to_decoded_action(trace: TraceResult | None) -> dict[str, str]:
    if not trace or not trace.parsed_trace:
        return {}
    mapping: dict[str, str] = {}
    for call in trace.parsed_trace.calls:
        if call.call_type == "STATICCALL":
            continue
        selector = (call.function_selector or "").lower()
        decoded = call.decoded_function or ""
        action = _action_from_function_name(decoded)
        if selector and action:
            mapping[selector] = action
    return mapping


def _action_from_function_name(decoded_function: str | None) -> str | None:
    if not decoded_function:
        return None
    name = decoded_function.split("(", 1)[0].strip().lower()
    if not name:
        return None

    if any(token in name for token in ("upgrade", "implementation")):
        return "upgrade"
    if any(token in name for token in ("transferownership", "acceptownership", "renounceownership")):
        return "permission_change"
    if any(name.startswith(prefix) for prefix in ("setowner", "setadmin", "changeadmin", "grantrole", "revokerole", "setoperator", "setvetoer")):
        return "permission_change"
    if name in {"transfer", "transferfrom"} or any(token in name for token in ("withdraw", "sweep")):
        return "transfer"
    if name in {"approve", "increaseallowance"} or "allowance" in name:
        return "approval"
    if any(token in name for token in ("bridge", "sendmessage", "relaymessage", "crosschain")):
        return "bridge"
    if any(
        token in name
        for token in (
            "parameter",
            "threshold",
            "quorum",
            "votingdelay",
            "votingperiod",
            "reservefactor",
            "riskparam",
            "config",
            "ltv",
            "collateral",
            "borrow",
            "factor",
            "pauseguardian",
            "priceoracle",
            "collateralfactor",
            "dynamicquorum",
        )
    ):
        return "parameter_update"
    if name.startswith("set") or name.startswith("_set"):
        return "parameter_update"
    return None


_MATERIAL_ACTION_VALUES = {action.value for action in _MATERIAL_ACTIONS}


def compact_risk_action(action: RiskAction) -> dict[str, object]:
    return {
        "id": action.id,
        "action_type": _enum_value(action.action_type),
        "severity_hint": _enum_value(action.severity_hint),
        "from_address": action.from_address,
        "to_address": action.to_address,
        "depth": action.depth,
        "function_selector": action.function_selector,
        "decoded_function": action.decoded_function,
        "value": action.value,
        "evidence_source": _enum_value(action.evidence_source),
        "confidence": action.confidence,
    }


def _enum_value(value: object) -> object:
    return getattr(value, "value", value)
