from __future__ import annotations

from eth_utils import function_signature_to_4byte_selector

from src.config.known_selectors import SELECTOR_ACTIONS, SELECTOR_SIGNATURES
from src.models.proposal import Proposal
from src.models.trace import ParsedTrace, TraceCall, TraceResult, TraceStatus
from src.utils.abi import decode_function_args_from_abi, get_function_signature_from_abi


def static_decode_fallback(proposal: Proposal) -> TraceResult:
    """Decode payload calldata without execution when simulation is unavailable."""

    calls: list[TraceCall] = []
    raw_calls: list[dict[str, object]] = []

    for index, payload in enumerate(proposal.payloads):
        input_data = build_transaction_data(payload.calldata, payload.signature)
        selector = input_data[:10].lower() if len(input_data) >= 10 else None
        decoded_function = (
            get_function_signature_from_abi(proposal.chain_id, payload.target, selector)
            or (SELECTOR_SIGNATURES.get(selector) if selector else None)
            or payload.signature
        )
        decoded_args = decode_function_args_from_abi(
            proposal.chain_id,
            payload.target,
            selector,
            input_data,
        )
        high_risk_hint = SELECTOR_ACTIONS.get(selector or "")

        call = TraceCall(
            call_type="UNKNOWN",
            from_address=proposal.executor or proposal.timelock or proposal.governor,
            to_address=payload.target.lower(),
            value=str(payload.value),
            input=input_data,
            output=None,
            depth=0,
            function_selector=selector,
            decoded_function=decoded_function,
            decoded_args=decoded_args,
            error=None,
        )
        calls.append(call)
        raw_calls.append(
            {
                "payload_call_index": index,
                "target": payload.target,
                "value": str(payload.value),
                "input": input_data,
                "function_selector": selector,
                "known_selector_semantic": decoded_function,
                "decoded_args": decoded_args,
                "high_risk_selector_hint": high_risk_hint,
            }
        )

    return TraceResult(
        proposal_id=proposal.proposal_id,
        simulation_status=TraceStatus.PARTIAL,
        trace_source="static_decode",
        raw_trace={"calls": raw_calls},
        parsed_trace=_summarize_static(calls),
        fallback_used=True,
        confidence=0.35,
    )


def build_transaction_data(calldata: str, signature: str | None = None) -> str:
    """Return calldata with a 4-byte selector when the sample stores args only."""

    data = calldata if calldata.startswith("0x") else f"0x{calldata}"
    if signature:
        selector = function_signature_to_4byte_selector(signature).hex()
        selector_hex = f"0x{selector}"
        if data.lower().startswith(selector_hex.lower()):
            return data.lower()
        return f"{selector_hex}{data[2:]}".lower()
    return data.lower()


def _summarize_static(calls: list[TraceCall]) -> ParsedTrace:
    addresses = sorted(
        {
            address
            for call in calls
            for address in (call.from_address, call.to_address)
            if address is not None
        }
    )
    decoded = sorted({call.decoded_function for call in calls if call.decoded_function})
    return ParsedTrace(
        calls=calls,
        max_depth=0,
        unique_addresses=addresses,
        external_call_count=len(calls),
        value_transfer_count=sum(1 for call in calls if call.value not in {"0", "0x0"}),
        decoded_functions=decoded,
    )

