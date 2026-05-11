from __future__ import annotations

import os
import shlex
import socket
import subprocess
import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

from src.models.proposal import Proposal
from src.models.trace import TraceResult, TraceStatus
from src.modules.abi.trace_abi_preparer import (
    AbiFetchConfig,
    prepare_trace_abis_for_parsed_trace,
)
from src.modules.trace.parse_trace import parse_raw_trace
from src.modules.trace.resolve_execution_context import resolve_execution_context
from src.modules.trace.static_decode_fallback import build_transaction_data, static_decode_fallback
from src.utils.rpc import rpc_call

DEFAULT_ANVIL_HOST = "0.0.0.0"
DEFAULT_ANVIL_PORT = "8545"


@dataclass(frozen=True)
class AnvilHandle:
    rpc_url: str
    process: subprocess.Popen[str] | None
    reused_existing: bool = False
    reset_existing: bool = False


def simulate_payload(proposal: Proposal) -> TraceResult:
    """Simulate proposal payload execution in the expected execution context.

    Failures must be converted into TraceResult instead of raising through the
    pipeline.
    """

    load_dotenv()

    rpc_url = _resolve_rpc_url(proposal)
    if not rpc_url:
        fallback = static_decode_fallback(proposal)
        fallback.error = "RPC URL is not configured."
        return fallback

    execution_context = resolve_execution_context(proposal, rpc_url)
    executor = execution_context.executor
    if not executor:
        fallback = static_decode_fallback(proposal)
        fallback.error = "No executor, timelock, or governor address is configured."
        return fallback

    anvil = _prepare_anvil(rpc_url, proposal.fork_block_number)
    anvil_error: str | None = None
    try:
        if anvil is not None and _wait_for_anvil(anvil):
            result = _simulate_on_rpc(
                proposal,
                anvil.rpc_url,
                executor,
                trace_source="simulated_trace",
                execution_context=execution_context.evidence | {
                    "source": execution_context.source,
                    "confidence": execution_context.confidence,
                    "anvil_rpc_url": anvil.rpc_url,
                    "anvil_reused_existing": anvil.reused_existing,
                    "anvil_reset_existing": anvil.reset_existing,
                },
            )
            if result.simulation_status != TraceStatus.FAILED:
                return result
            anvil_error = result.error
        else:
            anvil_error = "Anvil was unavailable or did not become ready before timeout."

        rpc_result = _simulate_on_rpc(
            proposal,
            rpc_url,
            executor,
            trace_source="rpc_debug_trace",
            execution_context=execution_context.evidence | {
                "source": execution_context.source,
                "confidence": execution_context.confidence,
            },
        )
        if rpc_result.simulation_status != TraceStatus.FAILED:
            return rpc_result

        fallback = static_decode_fallback(proposal)
        fallback.error = "; ".join(item for item in [anvil_error, rpc_result.error] if item)
        return fallback
    except Exception as exc:
        fallback = static_decode_fallback(proposal)
        fallback.error = str(exc)
        return fallback
    finally:
        if anvil is not None and anvil.process is not None:
            _stop_anvil(anvil.process)


def _resolve_rpc_url(proposal: Proposal) -> str | None:
    if proposal.chain_id is None:
        return None
    env_name = _default_rpc_env_for_chain(proposal.chain_id)
    return os.getenv(env_name)


def _default_rpc_env_for_chain(chain_id: int) -> str:
    explicit_names = {
        1: "MAINNET_RPC_URL",
        42161: "ARBITRUM_RPC_URL",
    }
    return explicit_names.get(chain_id, "")


def _prepare_anvil(rpc_url: str, fork_block_number: int | None) -> AnvilHandle | None:
    configured_rpc_url = _anvil_rpc_url()
    if _rpc_available(configured_rpc_url):
        if _reset_existing_anvil(configured_rpc_url, rpc_url, fork_block_number):
            return AnvilHandle(
                rpc_url=configured_rpc_url,
                process=None,
                reused_existing=True,
                reset_existing=True,
            )
        if not _allow_dynamic_anvil_port():
            return None
        port = _find_free_port()
        process = _start_anvil(rpc_url, fork_block_number, port=str(port))
        return AnvilHandle(rpc_url=f"http://127.0.0.1:{port}", process=process) if process else None

    port = os.getenv("ANVIL_PORT", DEFAULT_ANVIL_PORT)
    process = _start_anvil(rpc_url, fork_block_number, port=port)
    return AnvilHandle(rpc_url=configured_rpc_url, process=process) if process else None


def _start_anvil(
    rpc_url: str,
    fork_block_number: int | None,
    port: str | None = None,
) -> subprocess.Popen[str] | None:
    anvil_command = os.getenv("ANVIL_COMMAND") or os.getenv("ANVIL_BIN") or "anvil"
    command = _split_command(anvil_command)
    command.extend(
        [
            "--fork-url",
            rpc_url,
            "--host",
            os.getenv("ANVIL_HOST", DEFAULT_ANVIL_HOST),
            "--port",
            port or os.getenv("ANVIL_PORT", DEFAULT_ANVIL_PORT),
        ]
    )
    if fork_block_number:
        command.extend(["--fork-block-number", str(fork_block_number)])
    try:
        return subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None


def _split_command(command: str) -> list[str]:
    return shlex.split(command, posix=os.name != "nt")


def _anvil_rpc_url() -> str:
    return os.getenv(
        "ANVIL_RPC_URL",
        f"http://127.0.0.1:{os.getenv('ANVIL_PORT', DEFAULT_ANVIL_PORT)}",
    )


def _rpc_available(rpc_url: str) -> bool:
    try:
        _rpc(rpc_url, "eth_chainId", [])
        return True
    except Exception:
        return False


def _allow_dynamic_anvil_port() -> bool:
    return os.getenv("ANVIL_ALLOW_DYNAMIC_PORT", "").lower() in {"1", "true", "yes"}


def _reset_existing_anvil(
    anvil_rpc_url: str,
    fork_rpc_url: str,
    fork_block_number: int | None,
) -> bool:
    fork_config: dict[str, object] = {"jsonRpcUrl": fork_rpc_url}
    if fork_block_number is not None:
        fork_config["blockNumber"] = fork_block_number
    try:
        _rpc(anvil_rpc_url, "anvil_reset", [{"forking": fork_config}])
        _rpc(anvil_rpc_url, "eth_chainId", [])
        return True
    except Exception:
        return False


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _simulate_on_rpc(
    proposal: Proposal,
    rpc_url: str,
    executor: str,
    trace_source: str,
    execution_context: dict[str, object],
) -> TraceResult:
    raw_traces: list[dict[str, Any]] = []
    errors: list[str] = []
    reverted = False

    if trace_source == "simulated_trace":
        _rpc(rpc_url, "anvil_impersonateAccount", [executor])
        _rpc(rpc_url, "anvil_setBalance", [executor, hex(_required_executor_balance(proposal))])

    transaction_params = _transaction_params(rpc_url)
    for index, payload in enumerate(proposal.payloads):
        tx = {
            "from": executor,
            "to": payload.target,
            "value": hex(payload.value),
            "data": build_transaction_data(payload.calldata, payload.signature),
            **transaction_params,
        }
        tx_hash: str | None = None
        try:
            sent = _rpc(rpc_url, "eth_sendTransaction", [tx])
            tx_hash = sent if isinstance(sent, str) else None
            receipt = _wait_for_receipt(rpc_url, tx_hash)
            trace = _debug_trace_transaction(rpc_url, tx_hash)
            if trace is None:
                trace = _debug_trace_call(rpc_url, tx)
            if trace is not None:
                raw_traces.append({"payload_call_index": index, "trace": trace})
            if isinstance(receipt, dict) and receipt.get("status") == "0x0":
                reverted = True
        except Exception as exc:
            errors.append(f"payload {index} eth_sendTransaction failed: {exc}")
            trace = _debug_trace_call(rpc_url, tx)
            if trace is not None:
                reverted = _trace_has_error(trace)
                raw_traces.append({"payload_call_index": index, "trace": trace})
            else:
                errors.append(f"payload {index} debug_traceCall failed or unsupported")

    if not raw_traces:
        return TraceResult(
            proposal_id=proposal.proposal_id,
            simulation_status=TraceStatus.FAILED,
            trace_source=trace_source,
            error="; ".join(errors) or "No trace was returned.",
            confidence=0.0,
        )

    raw_trace_payloads = [item["trace"] for item in raw_traces if isinstance(item.get("trace"), dict)]
    parsed = parse_raw_trace(raw_trace_payloads, proposal.chain_id)
    abi_fetch_report = prepare_trace_abis_for_parsed_trace(
        parsed,
        proposal.chain_id,
        sample_id=str(proposal.metadata.get("benchmark_id") or proposal.proposal_id),
        config=AbiFetchConfig.from_env(),
        write_diagnostics=False,
    )
    if int(abi_fetch_report.get("changed_targets") or 0) > 0:
        parsed = parse_raw_trace(raw_trace_payloads, proposal.chain_id)

    raw_trace_payload: dict[str, object] = {
        "execution_context": execution_context,
        "payload_traces": raw_traces,
    }
    raw_trace_payload["abi_fetch_report"] = abi_fetch_report

    return TraceResult(
        proposal_id=proposal.proposal_id,
        simulation_status=TraceStatus.REVERTED if reverted else TraceStatus.SUCCESS,
        trace_source=trace_source,
        raw_trace=raw_trace_payload,
        parsed_trace=parsed,
        revert_reason=_first_revert_reason(raw_traces),
        error="; ".join(errors) if errors else None,
        confidence=0.9 if trace_source == "simulated_trace" else 0.75,
    )


def _transaction_params(rpc_url: str) -> dict[str, str]:
    """Build gas and fee params compatible with the fork block hardfork."""

    try:
        block = _rpc(rpc_url, "eth_getBlockByNumber", ["latest", False])
    except Exception:
        return {"gas": hex(15_000_000), "gasPrice": "0x3b9aca00"}

    params = {"gas": hex(_gas_limit_for_block(block))}
    if isinstance(block, dict) and block.get("baseFeePerGas"):
        base_fee = _hex_to_int(str(block["baseFeePerGas"]))
        max_priority_fee = 1_000_000_000
        max_fee = max(base_fee * 2 + max_priority_fee, max_priority_fee)
        params.update({
            "maxFeePerGas": hex(max_fee),
            "maxPriorityFeePerGas": hex(max_priority_fee),
        })
        return params

    params["gasPrice"] = "0x3b9aca00"
    return params


def _gas_limit_for_block(block: object) -> int:
    default_gas = 15_000_000
    if not isinstance(block, dict) or not block.get("gasLimit"):
        return default_gas
    block_gas_limit = _hex_to_int(str(block["gasLimit"]))
    if block_gas_limit <= 21_000:
        return default_gas
    return max(21_000, min(default_gas, block_gas_limit - 1))


def _hex_to_int(value: str) -> int:
    try:
        return int(value, 16) if value.startswith("0x") else int(value)
    except ValueError:
        return 0


def _rpc(rpc_url: str, method: str, params: Sequence[object]) -> object:
    return rpc_call(rpc_url, method, params)


def _required_executor_balance(proposal: Proposal) -> int:
    total_value = sum(payload.value for payload in proposal.payloads)
    buffer = 100 * 10**18
    return max(buffer, total_value + buffer)


def _wait_for_rpc(rpc_url: str, timeout_seconds: int = 60) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            _rpc(rpc_url, "eth_chainId", [])
            return True
        except Exception:
            time.sleep(0.5)
    return False


def _wait_for_anvil(anvil: AnvilHandle, timeout_seconds: int = 60) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if anvil.process is not None and anvil.process.poll() is not None:
            return False
        try:
            _rpc(anvil.rpc_url, "eth_chainId", [])
            return True
        except Exception:
            time.sleep(0.5)
    return False


def _wait_for_receipt(rpc_url: str, tx_hash: str | None, timeout_seconds: int = 30) -> object:
    if not tx_hash:
        return None
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        receipt = _rpc(rpc_url, "eth_getTransactionReceipt", [tx_hash])
        if receipt is not None:
            return receipt
        time.sleep(0.5)
    return None


def _debug_trace_transaction(rpc_url: str, tx_hash: str | None) -> dict[str, Any] | None:
    if not tx_hash:
        return None
    try:
        result = _rpc(rpc_url, "debug_traceTransaction", [tx_hash, {"tracer": "callTracer"}])
        return result if isinstance(result, dict) else None
    except Exception:
        return None


def _debug_trace_call(rpc_url: str, tx: dict[str, object]) -> dict[str, Any] | None:
    try:
        result = _rpc(rpc_url, "debug_traceCall", [tx, "latest", {"tracer": "callTracer"}])
        return result if isinstance(result, dict) else None
    except Exception:
        return None


def _trace_has_error(trace: dict[str, Any]) -> bool:
    if trace.get("error") or trace.get("revertReason"):
        return True
    for child in trace.get("calls", []) or []:
        if isinstance(child, dict) and _trace_has_error(child):
            return True
    return False


def _first_revert_reason(raw_traces: list[dict[str, Any]]) -> str | None:
    for item in raw_traces:
        trace = item.get("trace")
        if isinstance(trace, dict):
            reason = trace.get("revertReason") or trace.get("error")
            if reason:
                return str(reason)
    return None


def _stop_anvil(process: subprocess.Popen[str]) -> None:
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
