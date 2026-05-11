from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskActionType(StrEnum):
    UNKNOWN = "unknown"
    UPGRADE = "upgrade"
    PERMISSION_CHANGE = "permission_change"
    TRANSFER = "transfer"
    APPROVAL = "approval"
    DELEGATECALL = "delegatecall"
    SELFDESTRUCT = "selfdestruct"
    BRIDGE = "bridge"
    MULTICALL = "multicall"
    ARBITRARY_CALL = "arbitrary_call"
    PROXY_CHANGE = "proxy_change"
    CONTRACT_CREATION = "contract_creation"


class RiskAction(BaseModel):
    """Fact extracted from trace or static calldata, never inferred by LLM."""

    id: str
    action_type: RiskActionType
    severity_hint: Severity = Severity.LOW
    from_address: str | None = None
    to_address: str | None = None
    depth: int = 0
    function_selector: str | None = None
    decoded_function: str | None = None
    value: str = "0"
    evidence_source: str
    raw_evidence: dict[str, object] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)
