from __future__ import annotations

from dataclasses import dataclass, field

from eth_abi import decode, encode
from eth_utils import function_signature_to_4byte_selector

from src.models.proposal import Proposal
from src.utils.rpc import rpc_call


@dataclass(frozen=True)
class ExecutionContext:
    executor: str | None
    source: str
    confidence: float
    evidence: dict[str, object] = field(default_factory=dict)


def resolve_execution_context(proposal: Proposal, rpc_url: str) -> ExecutionContext:
    """Resolve the best msg.sender for direct payload simulation.

    This is deterministic chain-state inference. It does not use LLMs.
    """

    if proposal.executor:
        return ExecutionContext(
            executor=proposal.executor,
            source="proposal.executor",
            confidence=1.0,
            evidence={"executor": proposal.executor},
        )
    if proposal.timelock:
        return ExecutionContext(
            executor=proposal.timelock,
            source="proposal.timelock",
            confidence=0.95,
            evidence={"executor": proposal.timelock},
        )

    governor_context = _resolve_from_governor(proposal, rpc_url)
    if governor_context.executor:
        return governor_context

    owner_context = _resolve_from_payload_owners(proposal, rpc_url)
    if owner_context.executor:
        return owner_context

    if proposal.governor:
        return ExecutionContext(
            executor=proposal.governor,
            source="dao.governor_address",
            confidence=0.4,
            evidence={"executor": proposal.governor, "warning": "fallback_to_governor"},
        )

    return ExecutionContext(
        executor=None,
        source="unresolved",
        confidence=0.0,
        evidence={"error": "no executor, timelock, governor, or target owner resolved"},
    )


def _resolve_from_governor(proposal: Proposal, rpc_url: str) -> ExecutionContext:
    governor = proposal.governor
    if not governor:
        return ExecutionContext(None, "governor_unavailable", 0.0)

    proposal_id = _safe_int(proposal.proposal_id)
    attempts: list[dict[str, object]] = []

    for signature, args, confidence in (
        ("getExecutor(uint256)", [proposal_id] if proposal_id is not None else None, 0.9),
        ("executor()", [], 0.85),
        ("timelock()", [], 0.85),
    ):
        if args is None:
            continue
        result = _eth_call_address(rpc_url, governor, _calldata(signature, args), proposal.fork_block_number)
        attempts.append({"signature": signature, "result": result})
        if result:
            return ExecutionContext(
                executor=result,
                source=f"governor.{signature}",
                confidence=confidence,
                evidence={"governor": governor, "attempts": attempts},
            )

    return ExecutionContext(None, "governor_methods_unresolved", 0.0, {"governor": governor, "attempts": attempts})


def _resolve_from_payload_owners(proposal: Proposal, rpc_url: str) -> ExecutionContext:
    owners: list[dict[str, str | None]] = []
    for payload in proposal.payloads:
        owner = _eth_call_address(
            rpc_url,
            payload.target,
            _calldata("owner()", []),
            proposal.fork_block_number,
        )
        owners.append({"target": payload.target, "owner": owner})

    resolved = [item["owner"] for item in owners if item["owner"]]
    unique = sorted(set(resolved))
    if len(unique) == 1:
        return ExecutionContext(
            executor=unique[0],
            source="payload_target.owner()",
            confidence=0.8,
            evidence={"owners": owners},
        )
    if unique:
        return ExecutionContext(
            executor=unique[0],
            source="payload_target.owner()",
            confidence=0.65,
            evidence={"owners": owners, "warning": "multiple_target_owners"},
        )
    return ExecutionContext(None, "payload_target_owner_unresolved", 0.0, {"owners": owners})


def _eth_call_address(
    rpc_url: str,
    to_address: str,
    calldata: str,
    block_number: int | None,
) -> str | None:
    block = hex(block_number) if block_number is not None else "latest"
    try:
        result = rpc_call(rpc_url, "eth_call", [{"to": to_address, "data": calldata}, block])
    except Exception:
        return None
    if not isinstance(result, str) or result in {"0x", "0x0"}:
        return None
    try:
        decoded = decode(["address"], bytes.fromhex(result[2:]))
    except Exception:
        return None
    address = str(decoded[0]).lower()
    if address == "0x0000000000000000000000000000000000000000":
        return None
    return address


def _calldata(signature: str, args: list[object]) -> str:
    selector = function_signature_to_4byte_selector(signature)
    types = signature.split("(", 1)[1].rstrip(")")
    arg_types = [] if types == "" else types.split(",")
    encoded_args = encode(arg_types, args) if arg_types else b""
    return f"0x{(selector + encoded_args).hex()}"


def _safe_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
