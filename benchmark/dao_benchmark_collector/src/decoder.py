"""Calldata decoding for raw DAO benchmark samples.

This module reads raw sample JSON files and produces decoded call records. It
uses payload signatures when available, and falls back to local ABI files when
signatures are missing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eth_abi import decode as abi_decode
from eth_utils import keccak, to_hex


@dataclass(frozen=True)
class DecodeResult:
    """Decoded sample plus per-sample report fields."""

    sample: dict
    report: dict


def decode_raw_sample_file(raw_path: Path, project_root: Path) -> DecodeResult:
    """Decode one raw sample file into the decoded sample schema."""
    raw_sample = _read_json(raw_path)
    raw_relative_path = _relative_posix(raw_path, project_root)
    benchmark_id = str(raw_sample.get("benchmark_id") or "")
    payload = raw_sample.get("payload") or {}
    arrays = {
        "targets": payload.get("targets") or [],
        "values": payload.get("values") or [],
        "signatures": payload.get("signatures") or [],
        "calldatas": payload.get("calldatas") or [],
    }
    lengths = {name: len(value) for name, value in arrays.items()}
    min_length = min(lengths.values()) if lengths else 0
    payload_length_mismatch = len(set(lengths.values())) > 1
    implementation_index = load_implementation_abi_index(project_root)

    decoded_calls = []
    for index in range(min_length):
        decoded_calls.append(
            decode_payload_call(
                payload_call_index=index,
                target_contract=str(arrays["targets"][index] or ""),
                native_value=str(arrays["values"][index]),
                signature=str(arrays["signatures"][index] or ""),
                calldata=str(arrays["calldatas"][index] or ""),
                chain_id=int(raw_sample["dao"]["chain_id"]),
                project_root=project_root,
                implementation_index=implementation_index,
            )
        )

    if payload_length_mismatch:
        for index in range(min_length, max(lengths.values())):
            decoded_calls.append(
                {
                    "payload_call_index": index,
                    "target_contract": _value_at(arrays["targets"], index, ""),
                    "native_value": str(_value_at(arrays["values"], index, "")),
                    "function": _value_at(arrays["signatures"], index, ""),
                    "arguments": [],
                    "decode_status": "failed: payload_length_mismatch",
                }
            )

    decoded_sample = {
        "benchmark_id": benchmark_id,
        "source_raw_sample": raw_relative_path,
        "proposal": {
            "dao": raw_sample["dao"]["name"],
            "chain_id": raw_sample["dao"]["chain_id"],
            "proposal_id": raw_sample["proposal"]["proposal_id"],
            "status": raw_sample["proposal"]["status"],
            "title": raw_sample["proposal_text"]["title"],
            "description": raw_sample["proposal_text"]["description"],
        },
        "decoded_calls": decoded_calls,
    }
    decoded_ok = sum(1 for call in decoded_calls if call["decode_status"] == "ok")
    decoded_failed = len(decoded_calls) - decoded_ok
    report = {
        "benchmark_id": benchmark_id,
        "total_calls": len(decoded_calls),
        "decoded_ok": decoded_ok,
        "decoded_failed": decoded_failed,
        "payload_length_mismatch": payload_length_mismatch,
        "payload_lengths": lengths,
        "status_counts": _status_counts(decoded_calls),
        "call_errors": [
            {
                "payload_call_index": call["payload_call_index"],
                "target_contract": call["target_contract"],
                "decode_status": call["decode_status"],
            }
            for call in decoded_calls
            if call["decode_status"] != "ok"
        ],
    }
    return DecodeResult(sample=decoded_sample, report=report)


def decode_payload_call(
    payload_call_index: int,
    target_contract: str,
    native_value: str,
    signature: str,
    calldata: str,
    chain_id: int,
    project_root: Path,
    implementation_index: dict[tuple[int, str], Path] | None = None,
) -> dict:
    """Decode one payload call."""
    base = {
        "payload_call_index": payload_call_index,
        "target_contract": target_contract,
        "native_value": native_value,
        "function": signature if signature.strip() else None,
        "arguments": [],
    }
    calldata_hex = _normalize_hex(calldata)

    if signature.strip():
        try:
            function_name, arg_types = parse_function_signature(signature)
        except ValueError:
            return base | {"decode_status": "failed: unsupported_signature"}

        abi_entry = find_abi_function_by_signature(
            load_contract_abi(project_root, chain_id, target_contract),
            function_name,
            arg_types,
        )
        arg_names = _argument_names(abi_entry, len(arg_types))
        try:
            values = decode_by_signature(signature, calldata_hex)
        except ValueError:
            return base | {
                "function": signature,
                "arguments": [],
                "decode_status": "failed: decode_error",
            }
        except Exception:
            return base | {
                "function": signature,
                "arguments": [],
                "decode_status": "failed: decode_error",
            }

        return base | {
            "function": canonical_signature(function_name, arg_types),
            "arguments": build_arguments(arg_types, values, arg_names),
            "decode_status": "ok",
            "decode_source": "signature",
        }

    calldata_body = _strip_0x(calldata_hex)
    if not calldata_body:
        return base | {"decode_status": "failed: calldata_empty"}
    if len(calldata_body) < 8:
        return base | {"decode_status": "failed: calldata_too_short"}

    abi = load_contract_abi(project_root, chain_id, target_contract)
    if not abi:
        return base | {"decode_status": "failed: abi_missing"}

    selector = _strip_0x(calldata_hex)[:8].lower()
    matches = find_abi_functions_by_selector(abi, selector)
    decode_source = "target_abi"
    if not matches and implementation_index:
        implementation_abi = load_implementation_abi(
            implementation_index,
            chain_id,
            target_contract,
        )
        if implementation_abi:
            implementation_matches = find_abi_functions_by_selector(
                implementation_abi,
                selector,
            )
            if implementation_matches:
                matches = implementation_matches
                decode_source = "implementation_abi"
    if not matches:
        return base | {"decode_status": "failed: selector_not_found"}
    if len(matches) > 1:
        return base | {"decode_status": "failed: selector_ambiguous"}

    abi_entry = matches[0]
    function_name = str(abi_entry["name"])
    arg_types = [canonical_abi_type(input_item) for input_item in abi_entry.get("inputs", [])]
    arg_names = _argument_names(abi_entry, len(arg_types))
    function_signature = canonical_signature(function_name, arg_types)
    try:
        values = abi_decode(arg_types, bytes.fromhex(_strip_0x(calldata_hex)[8:]))
    except Exception:
        return base | {
            "function": function_signature,
            "decode_status": "failed: decode_error",
        }

    return base | {
        "function": function_signature,
        "arguments": build_arguments(arg_types, values, arg_names),
        "decode_status": "ok",
        "decode_source": decode_source,
    }


def parse_function_signature(signature: str) -> tuple[str, list[str]]:
    """Parse a function signature into name and canonical argument types."""
    value = signature.strip()
    open_index = value.find("(")
    if open_index <= 0 or not value.endswith(")"):
        raise ValueError("Unsupported function signature.")
    function_name = value[:open_index].strip()
    arg_string = value[open_index + 1 : -1].strip()
    if not function_name:
        raise ValueError("Unsupported function signature.")
    if not arg_string:
        return function_name, []
    return function_name, split_signature_args(arg_string)


def split_signature_args(arg_string: str) -> list[str]:
    """Split signature argument types while respecting nested tuple parens."""
    args = []
    current = []
    depth = 0
    for char in arg_string:
        if char == "," and depth == 0:
            args.append("".join(current).strip())
            current = []
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("Unsupported function signature.")
        current.append(char)
    if depth != 0:
        raise ValueError("Unsupported function signature.")
    args.append("".join(current).strip())
    if any(not arg for arg in args):
        raise ValueError("Unsupported function signature.")
    return args


def decode_by_signature(signature: str, calldata_hex: str) -> tuple:
    """Decode calldata using a provided function signature."""
    function_name, arg_types = parse_function_signature(signature)
    selector = function_selector(canonical_signature(function_name, arg_types))
    data = _strip_0x(calldata_hex)
    if not data:
        if arg_types:
            raise ValueError("failed: calldata_empty")
        return tuple()
    if data.lower().startswith(selector):
        data = data[8:]
    try:
        call_bytes = bytes.fromhex(data)
    except ValueError as exc:
        raise ValueError("failed: decode_error") from exc
    return abi_decode(arg_types, call_bytes)


def load_contract_abi(project_root: Path, chain_id: int, target_address: str) -> list[dict] | None:
    """Load a contract ABI from local files only."""
    return load_local_abi(project_root, chain_id, target_address)


def load_local_abi(project_root: Path, chain_id: int, target_address: str) -> list[dict] | None:
    """Load abis/{chain_id}/{lowercase_target_address}.json if present."""
    if not target_address:
        return None
    path = project_root / "abis" / str(chain_id) / f"{target_address.lower()}.json"
    if not path.exists():
        return None
    abi = _read_json(path)
    if isinstance(abi, list):
        return abi
    return None


def load_implementation_abi_index(project_root: Path) -> dict[tuple[int, str], Path]:
    """Load target contract to implementation ABI file mapping."""
    index_path = project_root / "outputs" / "abi_targets.jsonl"
    if not index_path.exists():
        return {}
    index: dict[tuple[int, str], Path] = {}
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except ValueError:
            continue
        abi_file = record.get("implementation_abi_file")
        target = record.get("target_contract")
        chain_id = record.get("chain_id")
        if not abi_file or not target or chain_id is None:
            continue
        path = project_root / str(abi_file)
        if path.exists():
            index[(int(chain_id), str(target).lower())] = path
    return index


def load_implementation_abi(
    implementation_index: dict[tuple[int, str], Path],
    chain_id: int,
    target_address: str,
) -> list[dict] | None:
    """Load implementation ABI for a target when available locally."""
    path = implementation_index.get((chain_id, target_address.lower()))
    if not path or not path.exists():
        return None
    abi = _read_json(path)
    if isinstance(abi, list):
        return abi
    return None


def find_abi_function_by_signature(
    abi: list[dict] | None,
    function_name: str,
    arg_types: list[str],
) -> dict | None:
    """Find an ABI function entry matching name and input types."""
    if not abi:
        return None
    wanted = canonical_signature(function_name, arg_types)
    for entry in function_entries(abi):
        input_types = [canonical_abi_type(item) for item in entry.get("inputs", [])]
        if canonical_signature(str(entry.get("name") or ""), input_types) == wanted:
            return entry
    return None


def find_abi_functions_by_selector(abi: list[dict], selector: str) -> list[dict]:
    """Find ABI function entries matching a 4-byte selector."""
    matches = []
    for entry in function_entries(abi):
        function_name = str(entry.get("name") or "")
        input_types = [canonical_abi_type(item) for item in entry.get("inputs", [])]
        if function_selector(canonical_signature(function_name, input_types)) == selector:
            matches.append(entry)
    return matches


def function_entries(abi: list[dict]) -> list[dict]:
    """Return ABI entries with type function."""
    return [
        entry
        for entry in abi
        if isinstance(entry, dict) and entry.get("type") == "function" and entry.get("name")
    ]


def canonical_abi_type(input_item: dict) -> str:
    """Return the canonical ABI type for selector/signature computation."""
    abi_type = str(input_item.get("type") or "")
    if abi_type.startswith("tuple"):
        suffix = abi_type[len("tuple") :]
        components = input_item.get("components") or []
        inner = ",".join(canonical_abi_type(component) for component in components)
        return f"({inner}){suffix}"
    return abi_type


def canonical_signature(function_name: str, arg_types: list[str]) -> str:
    """Build canonical function signature."""
    return f"{function_name}({','.join(arg_types)})"


def function_selector(signature: str) -> str:
    """Compute the 4-byte selector hex without 0x."""
    return keccak(text=signature)[:4].hex()


def build_arguments(
    arg_types: list[str],
    values: tuple,
    arg_names: list[str | None],
) -> list[dict]:
    """Build decoded argument records."""
    return [
        {
            "index": index,
            "name": arg_names[index] if index < len(arg_names) else None,
            "type": arg_type,
            "value": serialize_value(values[index]),
        }
        for index, arg_type in enumerate(arg_types)
    ]


def serialize_value(value: Any) -> Any:
    """Convert eth_abi decoded values to JSON-serializable values."""
    if isinstance(value, bytes):
        return to_hex(value)
    if isinstance(value, tuple):
        return [serialize_value(item) for item in value]
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    if isinstance(value, int):
        return str(value)
    return value


def decoded_file_path(raw_path: Path, output_dir: Path) -> Path:
    """Build decoded output path for a raw sample path."""
    benchmark_id = raw_path.stem
    decoded_name = benchmark_id.replace("real-", "decoded-", 1)
    return output_dir / "decoded_samples" / f"{decoded_name}.json"


def _argument_names(abi_entry: dict | None, count: int) -> list[str | None]:
    """Extract ABI input names, using null for missing or empty names."""
    if not abi_entry:
        return [None] * count
    names = []
    for input_item in abi_entry.get("inputs", []):
        name = input_item.get("name")
        names.append(str(name) if name else None)
    while len(names) < count:
        names.append(None)
    return names[:count]


def _read_json(path: Path) -> Any:
    """Read JSON from disk."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _normalize_hex(value: str) -> str:
    """Normalize optional hex strings to 0x-prefixed lowercase hex."""
    stripped = str(value or "").strip()
    if not stripped:
        return "0x"
    if stripped.startswith("0x") or stripped.startswith("0X"):
        return "0x" + stripped[2:]
    return "0x" + stripped


def _strip_0x(value: str) -> str:
    """Remove a 0x prefix."""
    if value.startswith("0x") or value.startswith("0X"):
        return value[2:]
    return value


def _value_at(values: list, index: int, default: Any) -> Any:
    """Read list value at index with a default."""
    if index < len(values):
        return values[index]
    return default


def _status_counts(decoded_calls: list[dict]) -> dict[str, int]:
    """Count decode statuses."""
    counts: dict[str, int] = {}
    for call in decoded_calls:
        status = call["decode_status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def _relative_posix(path: Path, project_root: Path) -> str:
    """Return a project-relative path using POSIX separators."""
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return path.as_posix()
