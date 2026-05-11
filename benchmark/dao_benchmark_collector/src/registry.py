"""DAO registry loading and validation.

The registry maps benchmark DAO identifiers to Tally slugs and expected chain
IDs. Later collection steps should use this module as the only source of DAO
configuration.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DaoConfig:
    """Static DAO configuration from config/dao_registry.json."""

    dao_id: str
    name: str
    tally_slug: str
    expected_chain_id: int


def load_registry(path: Path) -> list[DaoConfig]:
    """Load DAO registry JSON from disk."""
    if not path.exists():
        raise FileNotFoundError(f"DAO registry file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        raw_daos = json.load(file)

    if not isinstance(raw_daos, list):
        raise ValueError(f"DAO registry must be a JSON array: {path}")

    daos: list[DaoConfig] = []
    for index, raw_dao in enumerate(raw_daos):
        if not isinstance(raw_dao, dict):
            raise ValueError(f"DAO registry entry #{index} must be an object.")
        try:
            daos.append(
                DaoConfig(
                    dao_id=str(raw_dao["dao_id"]),
                    name=str(raw_dao["name"]),
                    tally_slug=str(raw_dao["tally_slug"]),
                    expected_chain_id=int(raw_dao["expected_chain_id"]),
                )
            )
        except KeyError as exc:
            raise ValueError(f"DAO registry entry #{index} missing field: {exc}") from exc
        except (TypeError, ValueError) as exc:
            raise ValueError(f"DAO registry entry #{index} has invalid field values.") from exc

    validate_registry(daos)
    return daos


def validate_registry(daos: list[DaoConfig]) -> None:
    """Validate required DAO fields and check for duplicate dao_id values."""
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()

    for dao in daos:
        if not dao.dao_id.strip():
            raise ValueError("DAO registry contains an empty dao_id.")
        if not dao.name.strip():
            raise ValueError(f"DAO {dao.dao_id} contains an empty name.")
        if not dao.tally_slug.strip():
            raise ValueError(f"DAO {dao.dao_id} contains an empty tally_slug.")
        if dao.expected_chain_id <= 0:
            raise ValueError(f"DAO {dao.dao_id} has invalid expected_chain_id.")

        if dao.dao_id in seen_ids:
            raise ValueError(f"Duplicate dao_id in registry: {dao.dao_id}")
        if dao.tally_slug in seen_slugs:
            raise ValueError(f"Duplicate tally_slug in registry: {dao.tally_slug}")

        seen_ids.add(dao.dao_id)
        seen_slugs.add(dao.tally_slug)
