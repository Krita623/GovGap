"""ABI preparation for decoded sample generation.

This module scans existing raw samples, extracts unique target contracts, and
fetches missing ABIs into the local abis/{chain_id}/ directory.
"""

from __future__ import annotations

import json
import os
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import requests


ETHERSCAN_V2_ENDPOINT = "https://api.etherscan.io/v2/api"


def prepare_abis(
    raw_samples_dir: Path,
    project_root: Path,
    output_dir: Path,
    sleep_seconds: float = 0.3,
    max_retries: int = 2,
) -> dict:
    """Prepare local ABI files for all unique raw sample target contracts."""
    targets = collect_abi_targets(raw_samples_dir, project_root)
    targets_path = output_dir / "abi_targets.jsonl"
    report_path = output_dir / "abi_report.json"
    log_path = output_dir / "abi_log.jsonl"
    _reset_file(targets_path)
    _reset_file(log_path)

    api_key = os.getenv("ETHERSCAN_API_KEY")
    status_counts: dict[str, int] = {}
    targets_with_abi = 0

    for target in targets:
        status, detail, implementation = prepare_one_abi_target(
            target=target,
            project_root=project_root,
            api_key=api_key,
            sleep_seconds=sleep_seconds,
            max_retries=max_retries,
        )
        target_record = {
            "chain_id": target["chain_id"],
            "target_contract": target["target_contract"],
            "abi_file": target["abi_file"],
            "abi_status": status,
            "implementation_address": implementation["implementation_address"],
            "implementation_abi_file": implementation["implementation_abi_file"],
            "implementation_abi_status": implementation["implementation_abi_status"],
            "used_by_samples": target["used_by_samples"],
        }
        _append_jsonl(targets_path, target_record)
        status_counts[status] = status_counts.get(status, 0) + 1

        if status in {"local_hit", "fetched_ok"}:
            targets_with_abi += 1
        else:
            _append_jsonl(
                log_path,
                {
                    **target_record,
                    "reason": detail,
                },
            )
        if is_problem_implementation_status(implementation["implementation_abi_status"]):
            _append_jsonl(
                log_path,
                {
                    **target_record,
                    "reason": implementation["implementation_detail"],
                },
            )

    report = {
        "unique_targets": len(targets),
        "status_counts": status_counts,
        "targets_with_abi": targets_with_abi,
        "targets_without_abi": len(targets) - targets_with_abi,
        "etherscan_api_key_detected": bool(api_key),
    }
    _write_json(report_path, report)
    return report


def collect_abi_targets(raw_samples_dir: Path, project_root: Path) -> list[dict]:
    """Collect unique chain/address targets from raw sample payloads."""
    used_by: dict[tuple[int, str], set[str]] = defaultdict(set)
    for raw_path in sorted(raw_samples_dir.glob("*.json")):
        sample = _read_json(raw_path)
        benchmark_id = str(sample.get("benchmark_id") or raw_path.stem)
        chain_id = int(sample["dao"]["chain_id"])
        targets = (sample.get("payload") or {}).get("targets") or []
        for target in targets:
            target_address = str(target or "").strip()
            if not target_address:
                continue
            used_by[(chain_id, target_address.lower())].add(benchmark_id)

    records = []
    for chain_id, target_address in sorted(used_by):
        abi_path = local_abi_path(project_root, chain_id, target_address)
        records.append(
            {
                "chain_id": chain_id,
                "target_contract": target_address,
                "abi_file": _relative_posix(abi_path, project_root),
                "abi_path": abi_path,
                "used_by_samples": sorted(used_by[(chain_id, target_address)]),
            }
        )
    return records


def prepare_one_abi_target(
    target: dict,
    project_root: Path,
    api_key: str | None,
    sleep_seconds: float,
    max_retries: int,
) -> tuple[str, str | None, dict]:
    """Prepare one ABI target and return status plus optional detail."""
    abi_path: Path = target["abi_path"]
    implementation = default_implementation_record()
    if abi_path.exists():
        implementation = prepare_implementation_abi(
            target=target,
            project_root=project_root,
            api_key=api_key,
            sleep_seconds=sleep_seconds,
            max_retries=max_retries,
        )
        return "local_hit", None, implementation
    if not api_key:
        return (
            "failed: api_key_missing",
            "ETHERSCAN_API_KEY is not set.",
            implementation,
        )

    status, detail, abi = fetch_abi_from_etherscan_v2(
        chain_id=target["chain_id"],
        target_contract=target["target_contract"],
        api_key=api_key,
        sleep_seconds=sleep_seconds,
        max_retries=max_retries,
    )
    if status != "fetched_ok":
        implementation = prepare_implementation_abi(
            target=target,
            project_root=project_root,
            api_key=api_key,
            sleep_seconds=sleep_seconds,
            max_retries=max_retries,
        )
        return status, detail, implementation

    abi_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(abi_path, abi)
    implementation = prepare_implementation_abi(
        target=target,
        project_root=project_root,
        api_key=api_key,
        sleep_seconds=sleep_seconds,
        max_retries=max_retries,
    )
    return "fetched_ok", None, implementation


def prepare_implementation_abi(
    target: dict,
    project_root: Path,
    api_key: str | None,
    sleep_seconds: float,
    max_retries: int,
) -> dict:
    """Fetch implementation source metadata and prepare implementation ABI."""
    if not api_key:
        return default_implementation_record()

    source_status, source_detail, implementation_address = fetch_implementation_address(
        chain_id=target["chain_id"],
        target_contract=target["target_contract"],
        api_key=api_key,
        sleep_seconds=sleep_seconds,
        max_retries=max_retries,
    )
    if source_status != "source_ok" or not implementation_address:
        if source_status == "source_no_implementation":
            return default_implementation_record(status=None, detail=None)
        return default_implementation_record(
            status=source_status.replace("source_", "failed: "),
            detail=source_detail,
        )

    implementation_address = implementation_address.lower()
    if implementation_address == target["target_contract"].lower():
        return default_implementation_record(
            implementation_address=implementation_address,
            status="same_as_target",
        )

    implementation_path = local_abi_path(
        project_root,
        target["chain_id"],
        implementation_address,
    )
    implementation_record = {
        "implementation_address": implementation_address,
        "implementation_abi_file": _relative_posix(implementation_path, project_root),
        "implementation_abi_status": "local_hit" if implementation_path.exists() else "",
        "implementation_detail": None,
    }
    if implementation_path.exists():
        return implementation_record

    abi_status, abi_detail, abi = fetch_abi_from_etherscan_v2(
        chain_id=target["chain_id"],
        target_contract=implementation_address,
        api_key=api_key,
        sleep_seconds=sleep_seconds,
        max_retries=max_retries,
    )
    implementation_record["implementation_abi_status"] = abi_status
    implementation_record["implementation_detail"] = abi_detail
    if abi_status == "fetched_ok":
        implementation_path.parent.mkdir(parents=True, exist_ok=True)
        _write_json(implementation_path, abi)
    return implementation_record


def default_implementation_record(
    implementation_address: str | None = None,
    status: str | None = None,
    detail: str | None = None,
) -> dict:
    """Build an empty implementation ABI record."""
    return {
        "implementation_address": implementation_address,
        "implementation_abi_file": None,
        "implementation_abi_status": status,
        "implementation_detail": detail,
    }


def is_problem_implementation_status(status: str | None) -> bool:
    """Return true when an implementation status should be logged as a problem."""
    return bool(status and status.startswith("failed:"))


def fetch_abi_from_etherscan_v2(
    chain_id: int,
    target_contract: str,
    api_key: str,
    sleep_seconds: float,
    max_retries: int,
) -> tuple[str, str | None, list[dict] | None]:
    """Fetch one ABI through Etherscan V2 getabi."""
    params = {
        "chainid": str(chain_id),
        "module": "contract",
        "action": "getabi",
        "address": target_contract,
        "apikey": api_key,
    }
    last_detail = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                ETHERSCAN_V2_ENDPOINT,
                params=params,
                timeout=10,
            )
            time.sleep(sleep_seconds)
        except requests.Timeout as exc:
            last_detail = str(exc)
            if attempt == max_retries:
                return "failed: timeout", last_detail, None
            continue
        except requests.RequestException as exc:
            last_detail = str(exc)
            if attempt == max_retries:
                return "failed: api_error", last_detail, None
            continue

        if response.status_code >= 500:
            last_detail = f"HTTP {response.status_code}: {response.text[:300]}"
            if attempt == max_retries:
                return "failed: api_error", last_detail, None
            continue
        if response.status_code >= 400:
            return "failed: api_error", f"HTTP {response.status_code}: {response.text[:300]}", None

        try:
            payload = response.json()
        except ValueError:
            return "failed: api_error", f"Invalid JSON response: {response.text[:300]}", None

        result = payload.get("result")
        if str(payload.get("status")) == "0":
            message = str(payload.get("message") or result or "")
            if _looks_unverified(message) or _looks_unverified(str(result or "")):
                return "failed: not_verified", message or str(result), None
            return "failed: api_error", message or str(result), None
        if not result:
            return "failed: invalid_abi", "Empty ABI result.", None

        try:
            abi = json.loads(result)
        except (TypeError, ValueError) as exc:
            return "failed: invalid_abi", str(exc), None
        if not isinstance(abi, list):
            return "failed: invalid_abi", "ABI response is not a JSON array.", None
        return "fetched_ok", None, abi

    return "failed: api_error", last_detail, None


def fetch_implementation_address(
    chain_id: int,
    target_contract: str,
    api_key: str,
    sleep_seconds: float,
    max_retries: int,
) -> tuple[str, str | None, str | None]:
    """Fetch implementation address from Etherscan V2 getsourcecode."""
    params = {
        "chainid": str(chain_id),
        "module": "contract",
        "action": "getsourcecode",
        "address": target_contract,
        "apikey": api_key,
    }
    last_detail = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                ETHERSCAN_V2_ENDPOINT,
                params=params,
                timeout=10,
            )
            time.sleep(sleep_seconds)
        except requests.Timeout as exc:
            last_detail = str(exc)
            if attempt == max_retries:
                return "source_timeout", last_detail, None
            continue
        except requests.RequestException as exc:
            last_detail = str(exc)
            if attempt == max_retries:
                return "source_api_error", last_detail, None
            continue

        if response.status_code >= 500:
            last_detail = f"HTTP {response.status_code}: {response.text[:300]}"
            if attempt == max_retries:
                return "source_api_error", last_detail, None
            continue
        if response.status_code >= 400:
            return "source_api_error", f"HTTP {response.status_code}: {response.text[:300]}", None

        try:
            payload = response.json()
        except ValueError:
            return "source_api_error", f"Invalid JSON response: {response.text[:300]}", None

        if str(payload.get("status")) == "0":
            return "source_api_error", str(payload.get("message") or payload.get("result")), None
        result = payload.get("result")
        if not isinstance(result, list) or not result:
            return "source_invalid_response", "Missing getsourcecode result array.", None

        implementation = result[0].get("Implementation") or result[0].get("ImplementationAddress")
        if not implementation:
            return "source_no_implementation", None, None
        implementation = str(implementation).strip()
        if not implementation or implementation == "0x0000000000000000000000000000000000000000":
            return "source_no_implementation", None, None
        return "source_ok", None, implementation

    return "source_api_error", last_detail, None


def local_abi_path(project_root: Path, chain_id: int, target_contract: str) -> Path:
    """Return local ABI path for a chain/address pair."""
    return project_root / "abis" / str(chain_id) / f"{target_contract.lower()}.json"


def _looks_unverified(message: str) -> bool:
    """Detect common Explorer messages for unverified contracts."""
    normalized = message.lower()
    return "not verified" in normalized or "source code not verified" in normalized


def _read_json(path: Path) -> Any:
    """Read JSON from disk."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_json(path: Path, data: Any) -> None:
    """Write JSON with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")


def _append_jsonl(path: Path, record: dict) -> None:
    """Append one JSONL record."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        json.dump(record, file)
        file.write("\n")


def _reset_file(path: Path) -> None:
    """Reset an output file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")


def _relative_posix(path: Path, root: Path) -> str:
    """Return root-relative POSIX path where possible."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
