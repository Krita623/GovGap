from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from eth_abi import decode
from eth_utils import function_signature_to_4byte_selector

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_function_signature_from_abi(
    chain_id: int | None,
    address: str | None,
    selector: str | None,
) -> str | None:
    """Resolve a function selector from data/abis if available."""

    entry = get_function_abi_entry(chain_id, address, selector)
    if entry is None:
        return None
    inputs = entry.get("inputs", [])
    types = [_canonical_abi_type(item) for item in inputs if isinstance(item, dict) and "type" in item]
    return f"{entry.get('name')}({','.join(types)})"


def decode_function_args_from_abi(
    chain_id: int | None,
    address: str | None,
    selector: str | None,
    input_data: str | None,
) -> list[object] | None:
    """Decode calldata args with a matching local ABI entry."""

    if not input_data or not selector:
        return None
    entry = get_function_abi_entry(chain_id, address, selector)
    if entry is None:
        return None

    try:
        inputs = entry.get("inputs", [])
        types = [_canonical_abi_type(item) for item in inputs if isinstance(item, dict) and "type" in item]
        raw_args = bytes.fromhex(input_data[10:])
        decoded = decode(types, raw_args) if types else ()
        return [_json_safe(value) for value in decoded]
    except Exception:
        return None


def clear_abi_caches() -> None:
    """Clear local ABI resolver caches after new ABI files are written."""

    _load_abi_entries.cache_clear()
    _load_abi_entries_from_path.cache_clear()
    _abi_roots.cache_clear()
    _abi_target_indexes.cache_clear()
    _implementation_abi_index.cache_clear()
    _global_selector_index.cache_clear()


def get_function_abi_entry(
    chain_id: int | None,
    address: str | None,
    selector: str | None,
) -> dict[str, Any] | None:
    if not chain_id or not address or not selector:
        return None

    normalized_address = address.lower()
    normalized_selector = selector.lower()

    direct = _find_entry_in_entries(_load_abi_entries(chain_id, normalized_address), normalized_selector)
    if direct is not None:
        return direct

    implementation = _find_implementation_entry(chain_id, normalized_address, normalized_selector)
    if implementation is not None:
        return implementation

    return _find_globally_unique_selector_entry(chain_id, normalized_selector)


def _find_implementation_entry(
    chain_id: int,
    address: str,
    selector: str,
) -> dict[str, Any] | None:
    for abi_path in _implementation_abi_paths(chain_id, address):
        entry = _find_entry_in_entries(_load_abi_entries_from_path(str(abi_path)), selector)
        if entry is not None:
            return entry
    return None


@lru_cache(maxsize=4096)
def _load_abi_entries(chain_id: int, address: str) -> tuple[dict[str, Any], ...]:
    for root in _abi_roots():
        abi_path = root / str(chain_id) / f"{address}.json"
        if not abi_path.exists():
            continue
        entries = _load_abi_entries_from_path(str(abi_path))
        if entries:
            return entries
    return ()


@lru_cache(maxsize=4096)
def _load_abi_entries_from_path(path_value: str) -> tuple[dict[str, Any], ...]:
    abi_path = Path(path_value)
    if not abi_path.exists():
        return ()
    try:
        abi = json.loads(abi_path.read_text(encoding="utf-8"))
        entries = abi if isinstance(abi, list) else abi.get("abi", [])
        return tuple(entry for entry in entries if isinstance(entry, dict))
    except Exception:
        return ()


def _find_entry_in_entries(
    entries: tuple[dict[str, Any], ...],
    selector: str,
) -> dict[str, Any] | None:
    for entry in entries:
        if entry.get("type") != "function":
            continue
        signature = _signature_for_entry(entry)
        if not signature:
            continue
        entry_selector = f"0x{function_signature_to_4byte_selector(signature).hex()}".lower()
        if entry_selector == selector:
            return entry
    return None


@lru_cache(maxsize=1)
def _abi_roots() -> tuple[Path, ...]:
    candidates = (
        PROJECT_ROOT / "data" / "abis",
        PROJECT_ROOT / "abis",
    )
    return tuple(path for path in candidates if path.exists())


@lru_cache(maxsize=1)
def _abi_target_indexes() -> tuple[Path, ...]:
    candidates = (
        PROJECT_ROOT / "data" / "abi_targets.jsonl",
    )
    return tuple(path for path in candidates if path.exists())


@lru_cache(maxsize=1)
def _implementation_abi_index() -> dict[tuple[int, str], tuple[Path, ...]]:
    index: dict[tuple[int, str], list[Path]] = {}
    for index_path in _abi_target_indexes():
        for line in index_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except ValueError:
                continue

            chain_id = record.get("chain_id")
            target = record.get("target_contract")
            implementation_address = record.get("implementation_address")
            implementation_abi_file = record.get("implementation_abi_file")
            if chain_id is None or not target:
                continue

            key = (int(chain_id), str(target).lower())
            paths: list[Path] = []
            if implementation_abi_file:
                paths.extend(_resolve_indexed_abi_path(index_path, str(implementation_abi_file)))
            if implementation_address:
                for root in _abi_roots():
                    paths.append(root / str(chain_id) / f"{str(implementation_address).lower()}.json")

            existing = [path for path in paths if path.exists()]
            if existing:
                index.setdefault(key, []).extend(existing)

    return {key: tuple(dict.fromkeys(paths)) for key, paths in index.items()}


def _implementation_abi_paths(chain_id: int, address: str) -> tuple[Path, ...]:
    return _implementation_abi_index().get((chain_id, address), ())


def _resolve_indexed_abi_path(index_path: Path, abi_file: str) -> tuple[Path, ...]:
    path = Path(abi_file)
    if path.is_absolute():
        return (path,)
    bases = (
        PROJECT_ROOT,
        index_path.parent,
        index_path.parent.parent,
    )
    return tuple(base / path for base in bases)


def _find_globally_unique_selector_entry(chain_id: int, selector: str) -> dict[str, Any] | None:
    signatures = _global_selector_index().get((chain_id, selector), {})
    if len(signatures) == 1:
        return next(iter(signatures.values()))
    return None


@lru_cache(maxsize=1)
def _global_selector_index() -> dict[tuple[int, str], dict[str, dict[str, Any]]]:
    index: dict[tuple[int, str], dict[str, dict[str, Any]]] = {}
    for root in _abi_roots():
        for chain_dir in root.iterdir():
            if not chain_dir.is_dir() or not chain_dir.name.isdigit():
                continue
            chain_id = int(chain_dir.name)
            for abi_path in chain_dir.glob("*.json"):
                for entry in _load_abi_entries_from_path(str(abi_path)):
                    signature = _signature_for_entry(entry)
                    if not signature:
                        continue
                    selector = f"0x{function_signature_to_4byte_selector(signature).hex()}".lower()
                    index.setdefault((chain_id, selector), {})[signature] = entry
    return index


def _signature_for_entry(entry: dict[str, Any]) -> str | None:
    name = entry.get("name")
    if not isinstance(name, str):
        return None
    inputs = entry.get("inputs", [])
    types = [_canonical_abi_type(item) for item in inputs if isinstance(item, dict) and "type" in item]
    return f"{name}({','.join(types)})"


def _canonical_abi_type(input_item: dict[str, Any]) -> str:
    abi_type = str(input_item.get("type") or "")
    if abi_type.startswith("tuple"):
        suffix = abi_type[len("tuple") :]
        components = input_item.get("components") or []
        inner = ",".join(
            _canonical_abi_type(component)
            for component in components
            if isinstance(component, dict)
        )
        return f"({inner}){suffix}"
    return abi_type


def _json_safe(value: object) -> object:
    if isinstance(value, bytes):
        return f"0x{value.hex()}"
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value
