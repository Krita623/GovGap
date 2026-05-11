from __future__ import annotations

import json
from pathlib import Path

from src.models.proposal import Proposal, ProposalPayload


def load_proposal(path: Path) -> Proposal:
    """Load and validate a proposal input file."""

    data = json.loads(path.read_text(encoding="utf-8"))
    proposal_data = data.get("proposal", {})
    dao_data = data.get("dao", {})
    proposal_text = data.get("proposal_text", data.get("proposal", {}))
    payload = data.get("payload", {})
    transactions = data.get("transactions", {})

    targets = payload.get("targets", [])
    values = payload.get("values", [])
    signatures = payload.get("signatures", [])
    calldatas = payload.get("calldatas", [])

    payloads: list[ProposalPayload] = []
    for index, target in enumerate(targets):
        payloads.append(
            ProposalPayload(
                target=target,
                value=int(values[index]) if index < len(values) else 0,
                calldata=calldatas[index] if index < len(calldatas) else "0x",
                signature=signatures[index] if index < len(signatures) else None,
            )
        )

    chain_id = data.get("chain_id") or dao_data.get("chain_id") or proposal_data.get("chain_id")
    proposal_id = str(
        proposal_data.get("proposal_id")
        or data.get("proposal_id")
        or data.get("benchmark_id")
        or path.stem
    )

    executed_block = proposal_data.get("executed_block")
    fork_block_number = data.get("fork_block_number") or proposal_data.get("fork_block_number")
    if fork_block_number is None and executed_block is not None:
        fork_block_number = max(int(executed_block) - 1, 0)

    return Proposal(
        proposal_id=proposal_id,
        title=proposal_text.get("title", ""),
        body=proposal_text.get("description", proposal_text.get("body", "")),
        chain_id=int(chain_id) if chain_id is not None else None,
        governor=dao_data.get("governor_address") or data.get("governor"),
        timelock=data.get("timelock"),
        executor=data.get("executor"),
        rpc_url_env=data.get("rpc_url_env") or proposal_data.get("rpc_url_env"),
        fork_block_number=fork_block_number,
        executed_tx_hash=transactions.get("executed_tx_hash"),
        payloads=payloads,
        metadata={
            "benchmark_id": str(data.get("benchmark_id", "")),
            "dao": str(dao_data.get("name", data.get("dao", ""))),
            "source_path": str(path),
        },
    )
