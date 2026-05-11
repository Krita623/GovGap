from __future__ import annotations

from typing import Any

from src.config.known_addresses import (
    KNOWN_PROTOCOL_ADDRESSES,
    KNOWN_SAFE_OR_PROXY_OR_GOVERNANCE_ADDRESSES,
    SYSTEM_ADDRESS_WHITELIST,
)
from src.config.known_selectors import SELECTOR_ACTIONS, SELECTOR_SIGNATURES
from src.models.risk_action import RiskAction, RiskActionType, Severity
from src.models.trace import TraceResult


_VIEW_STATIC_HELPERS = {
    "balanceof",
    "allowance",
    "owner",
    "getvotes",
    "getpastvotes",
    "quorum",
    "state",
    "proposalsnapshot",
    "proposaldeadline",
    "supportsinterface",
    "name",
    "symbol",
    "decimals",
}

_GOVERNANCE_BOOKKEEPING = {
    "proposalcount",
    "proposalthreshold",
    "votingdelay",
    "votingperiod",
    "latestproposalids",
    "hashproposal",
    "descriptionhash",
}

_WRAPPER_FUNCTIONS = {
    "execute",
    "queue",
    "propose",
    "exectransaction",
    "executetransaction",
}

_SENSITIVE_INNER_ACTIONS = {
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

_DELEGATECALL_BLOCKERS = {
    RiskActionType.UPGRADE,
    RiskActionType.PERMISSION_CHANGE,
    RiskActionType.PROXY_CHANGE,
    RiskActionType.ARBITRARY_CALL,
    RiskActionType.SELFDESTRUCT,
    RiskActionType.BRIDGE,
}

_ZERO_AMOUNT_ACTIONS = {
    RiskActionType.APPROVAL,
    RiskActionType.TRANSFER,
}

_SEVERITY_RANK = {
    Severity.NONE: 0,
    Severity.LOW: 1,
    Severity.MEDIUM: 2,
    Severity.HIGH: 3,
    Severity.CRITICAL: 4,
}


def extract_risk_actions(trace: TraceResult) -> list[RiskAction]:
    """Extract filtered deterministic risk actions from trace facts."""

    return extract_risk_actions_with_summary(trace)["risk_actions"]


def extract_risk_actions_with_summary(trace: TraceResult) -> dict[str, Any]:
    """Extract risk actions and include a compact deterministic filtering summary."""

    raw_actions = _extract_raw_risk_actions(trace)
    filtered_actions = _filter_low_value_actions(raw_actions)
    deduplicated_actions, deduplicated_count = _deduplicate_actions(filtered_actions)
    return {
        "risk_actions": deduplicated_actions,
        "filtering_summary": {
            "raw_detected_count": len(raw_actions),
            "filtered_count": len(raw_actions) - len(filtered_actions),
            "deduplicated_count": deduplicated_count,
            "final_risk_action_count": len(deduplicated_actions),
        },
    }


def _extract_raw_risk_actions(trace: TraceResult) -> list[RiskAction]:
    if trace.parsed_trace is None:
        return []

    evidence_source = "static_decode" if trace.trace_source == "static_decode" else "trace"
    if trace.simulation_status.value == "reverted_with_trace":
        evidence_source = "reverted_trace"

    actions: list[RiskAction] = []
    for index, call in enumerate(trace.parsed_trace.calls):
        action_type = _action_type_for_call(
            call.call_type,
            call.function_selector,
            call.decoded_function,
            call.to_address,
            call.value,
        )
        if action_type is None:
            continue

        severity = _severity_for_action(action_type, call.value)
        actions.append(
            RiskAction(
                id=f"{trace.proposal_id}:{index}:{action_type.value}",
                action_type=action_type,
                severity_hint=severity,
                from_address=call.from_address,
                to_address=call.to_address,
                depth=call.depth,
                function_selector=call.function_selector,
                decoded_function=call.decoded_function or _decoded_name(call.function_selector),
                value=call.value,
                evidence_source=evidence_source,
                raw_evidence=call.model_dump(),
                confidence=_confidence_for_source(evidence_source),
            )
        )

    return actions


def _filter_low_value_actions(actions: list[RiskAction]) -> list[RiskAction]:
    filtered: list[RiskAction] = []
    for action in actions:
        if _filter_reason(action, actions) is None:
            filtered.append(action)
    return filtered


def _filter_reason(action: RiskAction, all_actions: list[RiskAction]) -> str | None:
    if is_system_whitelisted(action.to_address):
        return "system_precompile"

    function_name = _function_name(action.decoded_function)
    call_type = str(action.raw_evidence.get("call_type", "")).upper()
    if call_type == "STATICCALL" and function_name in _VIEW_STATIC_HELPERS:
        return "view_or_static_helper"

    if function_name in _GOVERNANCE_BOOKKEEPING:
        return "governance_bookkeeping"

    if function_name in _WRAPPER_FUNCTIONS and _has_inner_sensitive_action(action, all_actions):
        if not _is_arbitrary_execute(action):
            return "wrapper_with_inner_sensitive_action"

    if _is_filterable_delegatecall(action, all_actions):
        return "known_proxy_or_governance_delegatecall"

    if _is_zero_amount_known_counterparty(action):
        return "zero_amount_known_counterparty"

    return None


def _is_filterable_delegatecall(action: RiskAction, all_actions: list[RiskAction]) -> bool:
    if action.action_type != RiskActionType.DELEGATECALL:
        return False
    if not _known_proxy_or_governance_address(action.to_address):
        return False
    if not action.function_selector or action.function_selector.lower() not in SELECTOR_SIGNATURES:
        return False
    return not any(item.action_type in _DELEGATECALL_BLOCKERS for item in all_actions)


def _is_zero_amount_known_counterparty(action: RiskAction) -> bool:
    if action.action_type not in _ZERO_AMOUNT_ACTIONS:
        return False
    if not action.function_selector or action.function_selector.lower() not in SELECTOR_SIGNATURES:
        return False
    amount = _decoded_amount(action)
    if amount is None or amount != 0:
        return False
    counterparty = _decoded_counterparty(action)
    return bool(counterparty and _known_protocol_address(counterparty))


def _has_inner_sensitive_action(action: RiskAction, all_actions: list[RiskAction]) -> bool:
    return any(
        item.id != action.id
        and item.depth > action.depth
        and item.action_type in _SENSITIVE_INNER_ACTIONS
        for item in all_actions
    )


def _is_arbitrary_execute(action: RiskAction) -> bool:
    signature = (action.decoded_function or "").replace(" ", "").lower()
    return signature == "execute(address,uint256,bytes)"


def _deduplicate_actions(actions: list[RiskAction]) -> tuple[list[RiskAction], int]:
    by_key: dict[tuple[object, ...], RiskAction] = {}
    merged_counts: dict[tuple[object, ...], int] = {}
    for action in actions:
        key = (
            action.action_type.value,
            _normalize_address(action.from_address),
            _normalize_address(action.to_address),
            (action.function_selector or "").lower(),
            action.decoded_function or "",
        )
        existing = by_key.get(key)
        merged_counts[key] = merged_counts.get(key, 0) + 1
        if existing is None or _prefer_action(action, existing):
            by_key[key] = action

    deduplicated = sorted(by_key.values(), key=lambda item: (item.depth, item.id))
    for action in deduplicated:
        key = (
            action.action_type.value,
            _normalize_address(action.from_address),
            _normalize_address(action.to_address),
            (action.function_selector or "").lower(),
            action.decoded_function or "",
        )
        merged_count = merged_counts.get(key, 1)
        if merged_count > 1:
            action.raw_evidence = {**action.raw_evidence, "merged_count": merged_count}

    return deduplicated, len(actions) - len(deduplicated)


def _prefer_action(candidate: RiskAction, existing: RiskAction) -> bool:
    candidate_rank = _SEVERITY_RANK[candidate.severity_hint]
    existing_rank = _SEVERITY_RANK[existing.severity_hint]
    if candidate_rank != existing_rank:
        return candidate_rank > existing_rank
    return candidate.depth < existing.depth


def _action_type_for_call(
    call_type: str,
    selector: str | None,
    decoded_function: str | None,
    to_address: str | None,
    value: str,
) -> RiskActionType | None:
    normalized_call_type = call_type.upper()
    if normalized_call_type == "DELEGATECALL":
        return RiskActionType.DELEGATECALL
    if normalized_call_type in {"CREATE", "CREATE2"}:
        return RiskActionType.CONTRACT_CREATION
    if normalized_call_type == "SELFDESTRUCT":
        return RiskActionType.SELFDESTRUCT
    if _int_value(value) > 0:
        return RiskActionType.TRANSFER

    if selector:
        mapped = SELECTOR_ACTIONS.get(selector.lower())
        if mapped:
            return RiskActionType(mapped)
        mapped_by_name = _action_type_from_function_name(decoded_function)
        if mapped_by_name:
            return mapped_by_name
        if _is_unknown_non_whitelisted(selector, decoded_function, to_address):
            return RiskActionType.UNKNOWN

    return None


def _action_type_from_function_name(decoded_function: str | None) -> RiskActionType | None:
    name = _function_name(decoded_function)
    if not name:
        return None
    if name in {"upgradeto", "upgradetoandcall", "setimplementation"}:
        return RiskActionType.UPGRADE
    if name in {"transferownership", "setowner", "grantrole", "revokerole", "setoperator"}:
        return RiskActionType.PERMISSION_CHANGE
    if name == "changeadmin":
        return RiskActionType.PROXY_CHANGE
    if name in {"transfer", "transferfrom", "withdraw", "sweep"}:
        return RiskActionType.TRANSFER
    if name in {"approve", "increaseallowance"}:
        return RiskActionType.APPROVAL
    if name == "multicall":
        return RiskActionType.MULTICALL
    if name == "execute":
        return RiskActionType.ARBITRARY_CALL
    if name in {"sendmessage", "relaymessage"} or "sendmessage" in name or "bridge" in name:
        return RiskActionType.BRIDGE
    return None


def _is_unknown_non_whitelisted(
    selector: str,
    decoded_function: str | None,
    to_address: str | None,
) -> bool:
    return (
        selector.lower() not in SELECTOR_SIGNATURES
        and decoded_function is None
        and not is_system_whitelisted(to_address)
    )


def _severity_for_action(action_type: RiskActionType, value: str) -> Severity:
    if action_type in {RiskActionType.SELFDESTRUCT, RiskActionType.UPGRADE, RiskActionType.PROXY_CHANGE}:
        return Severity.CRITICAL
    if action_type in {
        RiskActionType.DELEGATECALL,
        RiskActionType.ARBITRARY_CALL,
        RiskActionType.PERMISSION_CHANGE,
        RiskActionType.BRIDGE,
        RiskActionType.UNKNOWN,
        RiskActionType.CONTRACT_CREATION,
    }:
        return Severity.HIGH
    if action_type in {RiskActionType.TRANSFER, RiskActionType.APPROVAL, RiskActionType.MULTICALL}:
        return Severity.MEDIUM
    if _int_value(value) > 0:
        return Severity.MEDIUM
    return Severity.LOW


def _decoded_amount(action: RiskAction) -> int | None:
    args = action.raw_evidence.get("decoded_args")
    if not isinstance(args, list) or not args:
        return None
    name = _function_name(action.decoded_function)
    if name in {"approve", "increaseallowance", "transfer", "transferfrom"}:
        value = args[-1]
        return value if isinstance(value, int) else _safe_int(value)
    return None


def _decoded_counterparty(action: RiskAction) -> str | None:
    args = action.raw_evidence.get("decoded_args")
    if not isinstance(args, list) or not args:
        return None
    name = _function_name(action.decoded_function)
    if name in {"approve", "increaseallowance", "transfer"} and isinstance(args[0], str):
        return args[0]
    if name == "transferfrom" and len(args) > 1 and isinstance(args[1], str):
        return args[1]
    return action.to_address


def _function_name(decoded_function: str | None) -> str:
    if not decoded_function:
        return ""
    return decoded_function.split("(", 1)[0].replace("_", "").lower()


def _decoded_name(selector: str | None) -> str | None:
    return SELECTOR_SIGNATURES.get((selector or "").lower())


def _confidence_for_source(evidence_source: str) -> float:
    if evidence_source == "trace":
        return 0.9
    if evidence_source == "reverted_trace":
        return 0.75
    return 0.45


def _int_value(value: str) -> int:
    try:
        return int(value, 16) if value.startswith("0x") else int(value)
    except ValueError:
        return 0


def _safe_int(value: object) -> int | None:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _normalize_address(address: str | None) -> str | None:
    return address.lower() if isinstance(address, str) else None


def _known_protocol_address(address: str | None) -> bool:
    return bool(address and address.lower() in KNOWN_PROTOCOL_ADDRESSES)


def _known_proxy_or_governance_address(address: str | None) -> bool:
    return bool(address and address.lower() in KNOWN_SAFE_OR_PROXY_OR_GOVERNANCE_ADDRESSES)


def is_system_whitelisted(address: str | None) -> bool:
    """Return whether an address is a deterministic system whitelist entry."""

    return bool(address and address.lower() in SYSTEM_ADDRESS_WHITELIST)
