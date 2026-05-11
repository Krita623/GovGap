from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class TraceStatus(StrEnum):
    SUCCESS = "success"
    REVERTED = "reverted_with_trace"
    PARTIAL = "partial"
    FAILED = "failed"


class TraceCall(BaseModel):
    """Normalized trace call frame."""

    call_type: str
    from_address: str | None = None
    to_address: str | None = None
    value: str = "0"
    input: str | None = None
    output: str | None = None
    depth: int = 0
    function_selector: str | None = None
    decoded_function: str | None = None
    decoded_args: list[object] | None = None
    error: str | None = None


class ParsedTrace(BaseModel):
    """Trace format consumed by deterministic risk extraction."""

    calls: list[TraceCall] = Field(default_factory=list)
    max_depth: int = 0
    unique_addresses: list[str] = Field(default_factory=list)
    delegatecall_count: int = 0
    staticcall_count: int = 0
    external_call_count: int = 0
    value_transfer_count: int = 0
    decoded_functions: list[str] = Field(default_factory=list)


class TraceResult(BaseModel):
    """Simulation or fallback trace result."""

    proposal_id: str
    simulation_status: TraceStatus
    trace_source: str
    raw_trace: dict[str, object] = Field(default_factory=dict)
    parsed_trace: ParsedTrace | None = None
    revert_reason: str | None = None
    error: str | None = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
    fallback_used: bool = False
