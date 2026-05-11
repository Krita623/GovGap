from __future__ import annotations

from eth_utils import is_address, to_checksum_address


def normalize_address(address: str | None) -> str | None:
    """Normalize an EVM address to checksum format."""

    if not address:
        return None
    if not is_address(address):
        raise ValueError(f"Invalid EVM address: {address}")
    return to_checksum_address(address)

