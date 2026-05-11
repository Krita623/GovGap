"""Raw sample hydration and file writing.

This module fetches full proposal detail records from Tally and converts them
to the fixed raw benchmark JSON schema.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .governors import GovernorInfo, normalize_chain_id
from .registry import DaoConfig
from .sampling import SampleSelection
from .tally_client import TallyClient
from .utils import write_json


PROPOSAL_DETAIL_QUERY = """
query Proposal($input: ProposalInput!) {
  proposal(input: $input) {
    id
    onchainId
    chainId
    status
    block {
      number
      timestamp
    }
    metadata {
      title
      description
      txHash
    }
    events {
      type
      txHash
      chainId
      block {
        number
        timestamp
      }
    }
    executableCalls {
      index
      target
      value
      signature
      calldata
      chainId
      type
    }
    governor {
      id
      chainId
      name
      slug
      type
      contracts {
        governor {
          address
          type
        }
      }
    }
  }
}
"""

EXECUTED_EVENT_TYPES = {
    "executed",
    "callexecuted",
    "crosschainexecuted",
}


def hydrate_sample(
    client: TallyClient,
    dao: DaoConfig,
    governor: GovernorInfo,
    selection: SampleSelection,
) -> tuple[dict, list[dict]]:
    """Build one raw sample document matching the benchmark JSON schema."""
    proposal = fetch_proposal_detail(client, governor.governor_id, selection.proposal_id)
    if not proposal:
        raise ValueError(
            f"Proposal detail not found for {dao.dao_id} proposal {selection.proposal_id}."
        )

    metadata = proposal.get("metadata") or {}
    events = proposal.get("events") or []
    calls = sorted(
        proposal.get("executableCalls") or [],
        key=lambda call: _optional_int(call.get("index")) if call else -1,
    )
    detail_governor = proposal.get("governor") or {}
    raw_governor = _governor_from_detail(detail_governor, fallback=governor)
    created_event = _first_event(events, {"created"})
    executed_event = _first_event(events, EXECUTED_EVENT_TYPES)

    created_block = _block_number(proposal.get("block"))
    if created_block is None and created_event:
        created_block = _block_number(created_event.get("block"))

    sample = {
        "benchmark_id": selection.benchmark_id,
        "dao": {
            "name": dao.name,
            "chain_id": _proposal_chain_id(proposal, raw_governor),
            "governor_address": raw_governor.address,
            "governance_system": raw_governor.governance_system,
        },
        "proposal": {
            "proposal_id": str(proposal.get("onchainId") or selection.proposal_id),
            "proposal_url": _proposal_url(dao.tally_slug, selection.proposal_id),
            "source": "tally",
            "created_block": created_block,
            "executed_block": _block_number(executed_event.get("block")) if executed_event else None,
            "status": str(proposal.get("status") or selection.status),
        },
        "proposal_text": {
            "title": str(metadata.get("title") or ""),
            "description": str(metadata.get("description") or ""),
        },
        "payload": _payload_from_calls(calls),
        "transactions": {
            "created_tx_hash": _created_tx_hash(created_event, metadata),
            "executed_tx_hash": _tx_hash(executed_event) if executed_event else None,
        },
    }

    warnings = []
    if not calls:
        warnings.append(
            {
                "level": "warning",
                "type": "empty_executable_calls",
                "benchmark_id": selection.benchmark_id,
                "dao_id": dao.dao_id,
                "proposal_id": selection.proposal_id,
                "message": "Proposal detail contains no executableCalls.",
            }
        )
    return sample, warnings


def fetch_proposal_detail(
    client: TallyClient,
    governor_id: str,
    proposal_id: str,
) -> dict:
    """Fetch proposal detail by governor ID and on-chain proposal ID."""
    data = client.execute(
        PROPOSAL_DETAIL_QUERY,
        variables={
            "input": {
                "governorId": governor_id,
                "onchainId": proposal_id,
                "includeArchived": True,
            }
        },
    )
    return data.get("proposal") or {}


def write_raw_sample(sample: dict, output_dir: Path) -> Path:
    """Write a raw sample JSON document to outputs/raw_samples."""
    path = output_dir / f"{sample['benchmark_id']}.json"
    write_json(path, sample)
    return path


def build_manifest_record(
    sample: dict,
    dao: DaoConfig,
    selection: SampleSelection,
    file_path: Path,
) -> dict:
    """Build one manifest.jsonl record."""
    return {
        "benchmark_id": selection.benchmark_id,
        "dao_id": dao.dao_id,
        "dao_name": dao.name,
        "proposal_id": sample["proposal"]["proposal_id"],
        "chain_id": sample["dao"]["chain_id"],
        "status": sample["proposal"]["status"],
        "time_bucket": selection.time_bucket,
        "status_bucket": selection.status_bucket,
        "file": str(file_path.as_posix()),
    }


def _governor_from_detail(raw: dict, fallback: GovernorInfo) -> GovernorInfo:
    """Normalize governor metadata from proposal detail."""
    if not raw:
        return fallback
    contracts = raw.get("contracts") or {}
    contract_governor = contracts.get("governor") or {}
    address = contract_governor.get("address") or fallback.address
    governance_system = (
        contract_governor.get("type")
        or raw.get("type")
        or fallback.governance_system
    )
    chain_id = raw.get("chainId")
    return GovernorInfo(
        governor_id=str(raw.get("id") or fallback.governor_id),
        address=str(address),
        chain_id=normalize_chain_id(chain_id) if chain_id is not None else fallback.chain_id,
        governance_system=str(governance_system),
        name=raw.get("name") or fallback.name,
        slug=raw.get("slug") or fallback.slug,
    )


def _proposal_chain_id(proposal: dict, governor: GovernorInfo) -> int:
    """Return proposal chain ID, falling back to governor chain ID."""
    chain_id = proposal.get("chainId")
    if chain_id is None:
        return governor.chain_id
    return normalize_chain_id(chain_id)


def _proposal_url(tally_slug: str, proposal_id: str) -> str:
    """Build a Tally proposal URL."""
    return f"https://www.tally.xyz/gov/{tally_slug}/proposal/{proposal_id}"


def _payload_from_calls(calls: list[dict]) -> dict:
    """Build payload arrays from sorted executable calls."""
    return {
        "targets": [str(call.get("target") or "") for call in calls],
        "values": [str(call.get("value") if call.get("value") is not None else "0") for call in calls],
        "signatures": [str(call.get("signature") or "") for call in calls],
        "calldatas": [str(call.get("calldata") or "") for call in calls],
    }


def _first_event(events: list[dict], event_types: set[str]) -> dict | None:
    """Return the first event matching one of the requested event types."""
    for event in events:
        event_type = str(event.get("type") or "").lower()
        if event_type in event_types:
            return event
    return None


def _block_number(block: Any) -> int | None:
    """Extract an optional block number."""
    if not block:
        return None
    return _optional_int(block.get("number"))


def _optional_int(value: object) -> int | None:
    """Convert optional numeric values to int."""
    if value is None:
        return None
    return int(value)


def _created_tx_hash(created_event: dict | None, metadata: dict) -> str | None:
    """Extract created transaction hash from event or metadata fallback."""
    event_tx_hash = _tx_hash(created_event) if created_event else None
    if event_tx_hash:
        return event_tx_hash
    tx_hash = metadata.get("txHash")
    if tx_hash:
        return str(tx_hash)
    return None


def _tx_hash(event: dict | None) -> str | None:
    """Extract an optional tx hash from an event."""
    if not event:
        return None
    tx_hash = event.get("txHash")
    if tx_hash:
        return str(tx_hash)
    return None
