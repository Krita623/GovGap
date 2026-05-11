from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


EntityType = Literal[
    "governor",
    "timelock",
    "treasury",
    "token",
    "bridge",
    "multisig",
    "proxy",
    "implementation",
    "external_contract",
    "unknown",
]

DisclosureLevel = Literal["explicit", "implicit", "not_disclosed"]

CanonicalAction = Literal[
    "parameter_update",
    "upgrade",
    "transfer",
    "approval",
    "contract_creation",
    "governance_proposal_creation",
    "role_change",
    "bridge",
    "treasury_operation",
    "maintenance",
    "unknown",
]

ClaimedComplexityLevel = Literal["simple", "moderate", "complex", "unknown"]
LLMStatus = Literal["success", "repaired", "failed"]


class StrictSemanticsModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DisclosedEntity(StrictSemanticsModel):
    name: str
    address: str | None = None
    entity_type: EntityType
    disclosure_level: DisclosureLevel
    textual_evidence: str

    @field_validator("address")
    @classmethod
    def validate_optional_address(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not _is_evm_address(value):
            raise ValueError("address must be a 20-byte hex EVM address or null")
        return value.lower()


class DisclosedAddress(StrictSemanticsModel):
    address: str
    textual_evidence: str

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str) -> str:
        if not _is_evm_address(value):
            raise ValueError("address must be a 20-byte hex EVM address")
        return value.lower()


class ClaimedAction(StrictSemanticsModel):
    raw_action: str
    canonical_action: CanonicalAction
    object: str | None = None
    claimed_effect: str
    textual_evidence: str
    confidence: float = Field(ge=0.0, le=1.0)


class ClaimedComplexity(StrictSemanticsModel):
    level: ClaimedComplexityLevel
    reason: str
    textual_evidence: str


class DisclosedFunction(StrictSemanticsModel):
    function_name: str
    textual_evidence: str


class ProposalSemantics(StrictSemanticsModel):
    """LLM-extracted proposal text claims.

    This model represents textual claims only. It must not contain trace facts,
    risk severity, scoring fields, or final security conclusions.
    """

    proposal_summary: str
    disclosed_entities: list[DisclosedEntity] = Field(default_factory=list)
    disclosed_addresses: list[DisclosedAddress] = Field(default_factory=list)
    claimed_actions: list[ClaimedAction] = Field(default_factory=list)
    claimed_complexity: ClaimedComplexity
    disclosed_functions: list[DisclosedFunction] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    llm_status: LLMStatus
    llm_used_for_scoring: Literal[False] = False


def failed_semantics_fallback(summary: str, reason: str) -> ProposalSemantics:
    """Return a legal fallback schema when LLM extraction fails."""

    return ProposalSemantics(
        proposal_summary=summary or "unknown",
        disclosed_entities=[],
        disclosed_addresses=[],
        claimed_actions=[],
        claimed_complexity=ClaimedComplexity(
            level="unknown",
            reason=reason,
            textual_evidence="unknown",
        ),
        disclosed_functions=[],
        limitations=[reason],
        llm_status="failed",
        llm_used_for_scoring=False,
    )


def _is_evm_address(value: str) -> bool:
    if not isinstance(value, str) or len(value) != 42 or not value.startswith("0x"):
        return False
    return all(character in "0123456789abcdefABCDEF" for character in value[2:])
