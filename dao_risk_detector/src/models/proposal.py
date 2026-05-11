from __future__ import annotations

from pydantic import BaseModel, Field


class ProposalPayload(BaseModel):
    """Executable payload item supplied by a proposal."""

    target: str
    value: int = 0
    calldata: str
    signature: str | None = None
    description: str | None = None


class SimulationConfig(BaseModel):
    """Execution context used for direct payload simulation."""

    rpc_url_env: str | None = None
    fork_block_number: int | None = None
    anvil_rpc_url: str = "http://127.0.0.1:8545"
    simulation_timeout_seconds: int = 60


class Proposal(BaseModel):
    """Normalized proposal input."""

    proposal_id: str
    title: str
    body: str
    proposer: str | None = None
    chain_id: int | None = None
    governor: str | None = None
    timelock: str | None = None
    executor: str | None = None
    rpc_url_env: str | None = None
    fork_block_number: int | None = None
    executed_tx_hash: str | None = None
    payloads: list[ProposalPayload] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)
