"""Proposal listing and lightweight normalization.

This module will fetch governance proposals for a selected governor and expose
the fields required by sampling and later hydration.
"""

from __future__ import annotations

from dataclasses import dataclass

from .governors import GovernorInfo, normalize_chain_id
from .registry import DaoConfig
from .tally_client import TallyClient


PROPOSALS_QUERY = """
query Proposals($input: ProposalsInput!) {
  proposals(input: $input) {
    nodes {
      ... on Proposal {
        id
        onchainId
        chainId
        status
        block {
          number
          timestamp
        }
      }
    }
    pageInfo {
      firstCursor
      lastCursor
      count
    }
  }
}
"""


@dataclass(frozen=True)
class ProposalSummary:
    """Minimal proposal metadata used before full raw sample hydration."""

    proposal_tally_id: str
    proposal_id: str
    status: str
    created_block: int | None
    created_timestamp: str | None
    chain_id: int | None
    executed_block: int | None


@dataclass(frozen=True)
class ProposalIndexEntry:
    """Proposal metadata joined with DAO and governor context."""

    dao_id: str
    dao_name: str
    tally_slug: str
    governor_id: str
    governor_address: str
    governance_system: str
    proposal_tally_id: str
    proposal_id: str
    chain_id: int | None
    created_block: int | None
    created_timestamp: str | None
    status: str


def fetch_proposals(client: TallyClient, governor: GovernorInfo) -> list[ProposalSummary]:
    """Fetch proposals for a governor from Tally."""
    proposals: list[ProposalSummary] = []
    after_cursor: str | None = None
    seen_cursors: set[str] = set()

    while True:
        data = client.execute(
            PROPOSALS_QUERY,
            variables={
                "input": {
                    "filters": {
                        "governorId": governor.governor_id,
                    },
                    "page": _build_page_input(limit=20, after_cursor=after_cursor),
                    "sort": {
                        "sortBy": "id",
                        "isDescending": False,
                    },
                }
            },
        )
        payload = data.get("proposals") or {}
        nodes = payload.get("nodes") or []
        page_info = payload.get("pageInfo") or {}

        proposals.extend(normalize_proposal(node) for node in nodes if node)

        last_cursor = page_info.get("lastCursor")
        if not nodes or not last_cursor or last_cursor in seen_cursors:
            break

        seen_cursors.add(last_cursor)
        after_cursor = str(last_cursor)

    return proposals


def normalize_proposal(raw: dict) -> ProposalSummary:
    """Convert a raw Tally proposal object into ProposalSummary."""
    block = raw.get("block") or {}
    chain_id = raw.get("chainId")

    return ProposalSummary(
        proposal_tally_id=str(raw.get("id") or ""),
        proposal_id=str(raw.get("onchainId") or ""),
        status=str(raw.get("status") or ""),
        created_block=_optional_int(block.get("number")),
        created_timestamp=_optional_str(block.get("timestamp")),
        chain_id=normalize_chain_id(chain_id) if chain_id is not None else None,
        executed_block=None,
    )


def build_proposal_index(
    dao: DaoConfig,
    governor: GovernorInfo,
    proposals: list[ProposalSummary],
) -> list[ProposalIndexEntry]:
    """Join proposal summaries with DAO and governor metadata."""
    return [
        ProposalIndexEntry(
            dao_id=dao.dao_id,
            dao_name=dao.name,
            tally_slug=dao.tally_slug,
            governor_id=governor.governor_id,
            governor_address=governor.address,
            governance_system=governor.governance_system,
            proposal_tally_id=proposal.proposal_tally_id,
            proposal_id=proposal.proposal_id,
            chain_id=proposal.chain_id,
            created_block=proposal.created_block,
            created_timestamp=proposal.created_timestamp,
            status=proposal.status,
        )
        for proposal in proposals
    ]


def _build_page_input(limit: int, after_cursor: str | None) -> dict:
    """Build the Tally page input object."""
    page = {
        "limit": limit,
    }
    if after_cursor:
        page["afterCursor"] = after_cursor
    return page


def _optional_int(value: object) -> int | None:
    """Convert optional Tally numeric fields to int."""
    if value is None:
        return None
    return int(value)


def _optional_str(value: object) -> str | None:
    """Convert optional Tally scalar fields to str."""
    if value is None:
        return None
    return str(value)
