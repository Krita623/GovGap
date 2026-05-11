from __future__ import annotations

import json
from pathlib import Path

from src.config.known_selectors import SELECTOR_SIGNATURES
from src.models.trace import ParsedTrace, TraceCall, TraceResult, TraceStatus
from src.utils.abi import decode_function_args_from_abi, get_function_signature_from_abi


CALL_TYPES = {"CALL", "DELEGATECALL", "STATICCALL", "CALLCODE", "CREATE", "CREATE2", "SELFDESTRUCT"}
CREATION_CALL_TYPES = {"CREATE", "CREATE2"}


def parse_trace(proposal_id: str, trace_path: Path) -> TraceResult:
    """Parse raw Anvil/cast trace output into normalized call frames."""

    try:
        raw_trace = json.loads(trace_path.read_text(encoding="utf-8"))
        parsed = parse_raw_trace(raw_trace)
        return TraceResult(
            proposal_id=proposal_id,
            simulation_status=TraceStatus.PARTIAL,
            trace_source="anvil",
            raw_trace=raw_trace,
            parsed_trace=parsed,
            confidence=0.6,
        )
    except Exception as exc:
        return TraceResult(
            proposal_id=proposal_id,
            simulation_status=TraceStatus.FAILED,
            trace_source="anvil",
            error=str(exc),
            confidence=0.0,
        )


def parse_raw_trace(raw_trace: dict[str, object] | list[object], chain_id: int | None = None) -> ParsedTrace:
    """Normalize common debug trace formats into a flat call list."""

    calls: list[TraceCall] = []
    if isinstance(raw_trace, list):
        for item in raw_trace:
            if isinstance(item, dict):
                if _looks_like_parity_trace(item):
                    _append_parity_trace(item, calls, chain_id)
                else:
                    _walk_call_trace(item, 0, calls, chain_id)
    elif _looks_like_call_frame(raw_trace):
        _walk_call_trace(raw_trace, 0, calls, chain_id)
    elif raw_trace.get("trace_format") == "trace_transaction" and isinstance(raw_trace.get("result"), list):
        for item in raw_trace["result"]:
            if isinstance(item, dict):
                _append_parity_trace(item, calls, chain_id)
    elif isinstance(raw_trace.get("result"), dict):
        result = raw_trace["result"]
        if isinstance(result, dict):
            _walk_call_trace(result, 0, calls, chain_id)

    return _summarize_calls(calls)


def _looks_like_call_frame(value: object) -> bool:
    return isinstance(value, dict) and any(key in value for key in ("type", "from", "to", "input", "calls"))


def _looks_like_parity_trace(value: object) -> bool:
    return isinstance(value, dict) and isinstance(value.get("action"), dict)


def _append_parity_trace(frame: dict[str, object], calls: list[TraceCall], chain_id: int | None) -> None:
    action = frame.get("action")
    result = frame.get("result")
    if not isinstance(action, dict):
        return
    if not isinstance(result, dict):
        result = {}

    call_type = str(action.get("callType") or frame.get("type") or "UNKNOWN").upper()
    if call_type not in CALL_TYPES:
        call_type = "UNKNOWN"
    input_data = _as_hex(action.get("input"))
    selector = None if call_type in CREATION_CALL_TYPES else _selector(input_data)
    to_address = _lower_or_none(action.get("to"))
    decoded_function = (
        get_function_signature_from_abi(chain_id, to_address, selector)
        or (SELECTOR_SIGNATURES.get(selector) if selector else None)
    )
    decoded_args = decode_function_args_from_abi(chain_id, to_address, selector, input_data)
    trace_address = frame.get("traceAddress")
    depth = len(trace_address) if isinstance(trace_address, list) else 0

    calls.append(
        TraceCall(
            call_type=call_type,
            from_address=_lower_or_none(action.get("from")),
            to_address=to_address,
            value=str(action.get("value") or "0"),
            input=input_data,
            output=_as_hex(result.get("output")),
            depth=depth,
            function_selector=selector,
            decoded_function=decoded_function,
            decoded_args=decoded_args,
            error=_string_or_none(frame.get("error")),
        )
    )


def _walk_call_trace(
    frame: dict[str, object],
    depth: int,
    calls: list[TraceCall],
    chain_id: int | None,
) -> None:
    call_type = str(frame.get("type") or frame.get("callType") or "UNKNOWN").upper()
    if call_type not in CALL_TYPES:
        call_type = "UNKNOWN"

    input_data = _as_hex(frame.get("input") or frame.get("data"))
    selector = None if call_type in CREATION_CALL_TYPES else _selector(input_data)
    to_address = _lower_or_none(frame.get("to"))
    decoded_function = (
        get_function_signature_from_abi(chain_id, to_address, selector)
        or (SELECTOR_SIGNATURES.get(selector) if selector else None)
    )
    decoded_args = decode_function_args_from_abi(chain_id, to_address, selector, input_data)
    if decoded_function is None and selector:
        delegate_target = _matching_delegatecall_target(frame, input_data, selector)
        if delegate_target:
            decoded_function = (
                get_function_signature_from_abi(chain_id, delegate_target, selector)
                or SELECTOR_SIGNATURES.get(selector)
            )
            decoded_args = decode_function_args_from_abi(
                chain_id,
                delegate_target,
                selector,
                input_data,
            )

    calls.append(
        TraceCall(
            call_type=call_type,
            from_address=_lower_or_none(frame.get("from")),
            to_address=to_address,
            value=str(frame.get("value") or "0"),
            input=input_data,
            output=_as_hex(frame.get("output")),
            depth=depth,
            function_selector=selector,
            decoded_function=decoded_function,
            decoded_args=decoded_args,
            error=_string_or_none(frame.get("error") or frame.get("revertReason")),
        )
    )

    nested = frame.get("calls")
    if isinstance(nested, list):
        for child in nested:
            if isinstance(child, dict):
                _walk_call_trace(child, depth + 1, calls, chain_id)


def _matching_delegatecall_target(
    frame: dict[str, object],
    input_data: str | None,
    selector: str,
) -> str | None:
    nested = frame.get("calls")
    if not isinstance(nested, list):
        return None
    for child in nested:
        if not isinstance(child, dict):
            continue
        call_type = str(child.get("type") or child.get("callType") or "").upper()
        if call_type != "DELEGATECALL":
            continue
        child_input = _as_hex(child.get("input") or child.get("data"))
        if child_input != input_data or _selector(child_input) != selector:
            continue
        child_to = _lower_or_none(child.get("to"))
        if child_to:
            return child_to
    return None


def _summarize_calls(calls: list[TraceCall]) -> ParsedTrace:
    addresses: set[str] = set()
    decoded: list[str] = []
    for call in calls:
        if call.from_address:
            addresses.add(call.from_address)
        if call.to_address:
            addresses.add(call.to_address)
        if call.decoded_function:
            decoded.append(call.decoded_function)

    return ParsedTrace(
        calls=calls,
        max_depth=max((call.depth for call in calls), default=0),
        unique_addresses=sorted(addresses),
        delegatecall_count=sum(1 for call in calls if call.call_type == "DELEGATECALL"),
        staticcall_count=sum(1 for call in calls if call.call_type == "STATICCALL"),
        external_call_count=sum(1 for call in calls if call.call_type in {"CALL", "CALLCODE"}),
        value_transfer_count=sum(1 for call in calls if _int_value(call.value) > 0),
        decoded_functions=sorted(set(decoded)),
    )


def _selector(input_data: str | None) -> str | None:
    if input_data and input_data.startswith("0x") and len(input_data) >= 10:
        return input_data[:10].lower()
    return None


def _as_hex(value: object) -> str | None:
    if isinstance(value, str):
        return value.lower() if value.startswith("0x") else value
    return None


def _lower_or_none(value: object) -> str | None:
    return value.lower() if isinstance(value, str) else None


def _string_or_none(value: object) -> str | None:
    return str(value) if value is not None else None


def _int_value(value: str) -> int:
    try:
        return int(value, 16) if value.startswith("0x") else int(value)
    except ValueError:
        return 0
