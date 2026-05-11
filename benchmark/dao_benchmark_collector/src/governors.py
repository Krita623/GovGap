"""Governor discovery helpers.

This module will resolve Tally organizations to governor contracts and verify
that discovered governors match each DAO's expected chain ID.
"""

from __future__ import annotations

from dataclasses import dataclass

from .registry import DaoConfig
from .tally_client import TallyClient, TallyGraphQLError


GOVERNOR_QUERY = """
query Governor($input: GovernorInput!) {
  governor(input: $input) {
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
"""

ORGANIZATION_GOVERNORS_QUERY = """
query OrganizationGovernors($input: OrganizationInput!) {
  organization(input: $input) {
    id
    slug
    name
    chainIds
    governorIds
  }
}
"""


@dataclass(frozen=True)
class GovernorInfo:
    """Governor metadata needed for raw sample output."""

    governor_id: str
    address: str
    chain_id: int
    governance_system: str
    name: str | None = None
    slug: str | None = None


def fetch_governors(client: TallyClient, dao: DaoConfig) -> list[GovernorInfo]:
    """Fetch candidate governors for a DAO from Tally."""
    governors: list[GovernorInfo] = []

    try:
        governor = _fetch_governor(client, {"slug": dao.tally_slug})
        if governor:
            governors.append(governor)
    except TallyGraphQLError:
        pass

    for governor_id in _fetch_organization_governor_ids(client, dao.tally_slug):
        if any(governor.governor_id == governor_id for governor in governors):
            continue
        governor = _fetch_governor(client, {"id": governor_id})
        if governor:
            governors.append(governor)

    return governors


def select_primary_governor(governors: list[GovernorInfo], expected_chain_id: int) -> GovernorInfo:
    """Select the governor used for sampling."""
    for governor in governors:
        if governor.chain_id == expected_chain_id:
            return governor
    if governors:
        return governors[0]
    raise ValueError("No governors available for selection.")


def normalize_chain_id(chain_id: str | int) -> int:
    """Normalize Tally chain IDs such as eip155:1, 1, or '1' to integers."""
    if isinstance(chain_id, int):
        return chain_id
    if isinstance(chain_id, str):
        value = chain_id.strip()
        if value.startswith("eip155:"):
            value = value.split(":", 1)[1]
        return int(value)
    raise TypeError(f"Unsupported chain ID value: {chain_id!r}")


def _fetch_governor(client: TallyClient, input_value: dict) -> GovernorInfo | None:
    """Fetch one governor by Tally GovernorInput."""
    data = client.execute(
        GOVERNOR_QUERY,
        variables={
            "input": input_value,
        },
    )
    governor = data.get("governor")
    if not governor:
        return None
    return _normalize_governor(governor)


def _fetch_organization_governor_ids(client: TallyClient, slug: str) -> list[str]:
    """Fetch governor IDs from a Tally organization slug."""
    data = client.execute(
        ORGANIZATION_GOVERNORS_QUERY,
        variables={
            "input": {
                "slug": slug,
            }
        },
    )
    organization = data.get("organization") or {}
    return [str(governor_id) for governor_id in organization.get("governorIds", [])]


def _normalize_governor(raw: dict) -> GovernorInfo:
    """Convert a Tally governor response object into GovernorInfo."""
    contracts = raw.get("contracts") or {}
    contract_governor = contracts.get("governor") or {}
    address = contract_governor.get("address") or ""
    governance_system = contract_governor.get("type") or raw.get("type") or ""

    return GovernorInfo(
        governor_id=str(raw.get("id") or ""),
        address=str(address),
        chain_id=normalize_chain_id(raw["chainId"]),
        governance_system=str(governance_system),
        name=raw.get("name"),
        slug=raw.get("slug"),
    )
