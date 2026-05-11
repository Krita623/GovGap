from __future__ import annotations

import json
import os
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from eth_utils import function_signature_to_4byte_selector, is_address, to_checksum_address

from src.models.trace import ParsedTrace
from src.utils.abi import clear_abi_caches

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ETHERSCAN_V2_ENDPOINT = "https://api.etherscan.io/v2/api"
SOURCIFY_REPO_ENDPOINT = "https://repo.sourcify.dev/contracts"
EIP1967_IMPLEMENTATION_SLOT = (
    "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
)
EIP1967_BEACON_SLOT = "0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50"
BEACON_IMPLEMENTATION_SELECTOR = "0x5c60da1b"
CREATION_CALL_TYPES = {"CREATE", "CREATE2"}


@dataclass(frozen=True)
class AbiFetchConfig:
    """Detector-local ABI acquisition settings.

    The risk detector owns these paths and environment variables. It does not
    read or write the benchmark collector ABI directories at runtime.
    """

    project_root: Path = PROJECT_ROOT
    abi_dir: Path = PROJECT_ROOT / "data" / "abis"
    abi_targets_path: Path = PROJECT_ROOT / "data" / "abi_targets.jsonl"
    analysis_dir: Path = PROJECT_ROOT / "analysis" / "unknown_selectors"
    etherscan_api_key: str | None = None
    sourcify_enabled: bool = True
    etherscan_enabled: bool = True
    refresh_existing_abi: bool = True
    rpc_implementation_resolution_enabled: bool = True
    sleep_seconds: float = 0.15
    max_retries: int = 2
    http_timeout_seconds: float = 10.0
    rpc_timeout_seconds: float = 6.0
    dry_run: bool = False

    @classmethod
    def from_env(
        cls,
        *,
        project_root: Path = PROJECT_ROOT,
        abi_dir: Path | None = None,
        abi_targets_path: Path | None = None,
        analysis_dir: Path | None = None,
        dry_run: bool = False,
    ) -> "AbiFetchConfig":
        load_dotenv(project_root / ".env")
        return cls(
            project_root=project_root,
            abi_dir=_resolve_path(project_root, abi_dir or _env_path("DAO_RISK_ABI_DIR", "data/abis")),
            abi_targets_path=_resolve_path(
                project_root,
                abi_targets_path or _env_path("DAO_RISK_ABI_TARGETS", "data/abi_targets.jsonl"),
            ),
            analysis_dir=_resolve_path(
                project_root,
                analysis_dir or _env_path("DAO_RISK_ABI_ANALYSIS_DIR", "analysis/unknown_selectors"),
            ),
            etherscan_api_key=os.getenv("ETHERSCAN_API_KEY") or None,
            sourcify_enabled=_env_bool("DAO_RISK_ABI_FETCH_SOURCIFY", True),
            etherscan_enabled=_env_bool("DAO_RISK_ABI_FETCH_ETHERSCAN", True),
            refresh_existing_abi=_env_bool("DAO_RISK_ABI_REFRESH_EXISTING", True),
            rpc_implementation_resolution_enabled=_env_bool(
                "DAO_RISK_ABI_FETCH_IMPLEMENTATION_RPC",
                True,
            ),
            sleep_seconds=_env_float("DAO_RISK_ABI_FETCH_SLEEP_SECONDS", 0.15),
            max_retries=_env_int("DAO_RISK_ABI_FETCH_MAX_RETRIES", 2),
            dry_run=dry_run,
        )

def prepare_trace_abis_for_parsed_trace(
    parsed_trace: ParsedTrace | None,
    chain_id: int | None,
    *,
    sample_id: str | None = None,
    config: AbiFetchConfig | None = None,
    write_diagnostics: bool = False,
) -> dict[str, Any]:
    """Fetch local ABIs for unresolved trace call targets.

    This function is intended for use after an initial trace parse. If it
    writes any ABI files or updates proxy implementation metadata, callers
    should parse the same raw trace again so the resolver can use the new ABI
    corpus.
    """

    if parsed_trace is None or chain_id is None:
        return _empty_report(dry_run=bool(config and config.dry_run))
    targets = collect_unresolved_trace_abi_targets(parsed_trace, int(chain_id), sample_id=sample_id)
    return prepare_trace_abis_for_targets(
        targets,
        config=config or AbiFetchConfig.from_env(),
        write_diagnostics=write_diagnostics,
    )


def collect_unresolved_trace_abi_targets(
    parsed_trace: ParsedTrace,
    chain_id: int,
    *,
    sample_id: str | None = None,
) -> list[dict[str, Any]]:
    """Collect chain/address targets for calls that remain undecoded."""

    grouped: dict[tuple[int, str], list[Any]] = defaultdict(list)
    for call in parsed_trace.calls:
        if call.decoded_function or not call.function_selector:
            continue
        if call.call_type.upper() in CREATION_CALL_TYPES:
            continue
        address = _normalize_address(call.to_address)
        if not address:
            continue
        grouped[(chain_id, address)].append(call)

    records: list[dict[str, Any]] = []
    for (target_chain, target_address), calls in grouped.items():
        sample_ids = [sample_id] if sample_id else []
        records.append(
            {
                "chain_id": target_chain,
                "target_contract": target_address,
                "unknown_action_count": len(calls),
                "selectors": sorted({str(call.function_selector).lower() for call in calls}),
                "call_types": sorted({str(call.call_type).upper() for call in calls if call.call_type}),
                "example_benchmark_ids": sample_ids,
            }
        )
    return sorted(records, key=lambda item: (-int(item["unknown_action_count"]), item["target_contract"]))


def load_abi_target_records_jsonl(path: Path) -> list[dict[str, Any]]:
    """Load target records such as analysis/unknown_selectors/missing-trace-abi-targets.jsonl."""

    targets: list[dict[str, Any]] = []
    if not path.exists():
        return targets
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        address = _normalize_address(record.get("target_contract"))
        chain_id = record.get("chain_id")
        if address and chain_id is not None:
            record["target_contract"] = address
            record["chain_id"] = int(chain_id)
            targets.append(record)
    return targets


def prepare_trace_abis_for_targets(
    targets: list[dict[str, Any]],
    *,
    config: AbiFetchConfig | None = None,
    write_diagnostics: bool = False,
) -> dict[str, Any]:
    """Fetch and persist detector-local ABIs for explicit target records."""

    config = config or AbiFetchConfig.from_env()
    config.abi_dir.mkdir(parents=True, exist_ok=True)
    if write_diagnostics:
        config.analysis_dir.mkdir(parents=True, exist_ok=True)

    abi_index = _load_abi_target_index(config.abi_targets_path)
    logs: list[dict[str, Any]] = []
    log_path = config.analysis_dir / "fetch-trace-abi-log.jsonl"
    if write_diagnostics and not config.dry_run:
        log_path.write_text("", encoding="utf-8")

    for index, target in enumerate(targets, start=1):
        chain_id = int(target["chain_id"])
        address = _normalize_address(target["target_contract"])
        if not address:
            continue
        result = _prepare_target(target=target, chain_id=chain_id, address=address, config=config)
        record = _build_abi_target_record(target, result)
        abi_index[(chain_id, address)] = record
        log_record = {
            "index": index,
            "chain_id": chain_id,
            "target_contract": address,
            "abi_status": result["abi_status"],
            "abi_source": result["abi_source"],
            "implementation_address": result["implementation_address"],
            "implementation_abi_status": result["implementation_abi_status"],
            "implementation_source": result["implementation_source"],
            "detail": result["detail"],
            "implementation_detail": result["implementation_detail"],
            "selectors": target.get("selectors", []),
            "unknown_action_count": target.get("unknown_action_count"),
        }
        logs.append(log_record)
        if not config.dry_run:
            _write_abi_target_index(config.abi_targets_path, abi_index)
            if write_diagnostics:
                _append_jsonl(log_path, log_record)

    if not config.dry_run:
        clear_abi_caches()

    summary = _build_summary(logs, config=config)
    if write_diagnostics and not config.dry_run:
        (config.analysis_dir / "fetch-trace-abi-report.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return summary


def _prepare_target(
    *,
    target: dict[str, Any],
    chain_id: int,
    address: str,
    config: AbiFetchConfig,
) -> dict[str, Any]:
    abi_path = _abi_path(config.abi_dir, chain_id, address)
    abi_status = "local_hit" if abi_path.exists() else ""
    abi_source = "local" if abi_path.exists() else ""
    detail = None
    abi: list[dict[str, Any]] | None = _load_local_abi(abi_path) if abi_path.exists() else None

    if not abi_path.exists():
        abi_status, detail, abi, abi_source = _fetch_abi(
            chain_id=chain_id,
            address=address,
            config=config,
        )
        if abi_status == "fetched_ok" and abi is not None and not config.dry_run:
            _write_json(abi_path, abi)

    selectors = [str(selector).lower() for selector in target.get("selectors", [])]
    if abi is not None and _abi_covers_selectors(abi, selectors):
        return {
            "chain_id": chain_id,
            "target_contract": address,
            "abi_file": _relative_posix(abi_path, config.project_root),
            "abi_status": abi_status or "failed: not_attempted",
            "abi_source": abi_source,
            "detail": detail,
            "implementation_address": None,
            "implementation_abi_file": None,
            "implementation_abi_status": None,
            "implementation_source": None,
            "implementation_detail": "direct ABI covers requested selectors",
            "used_by_samples": target.get("example_benchmark_ids", []),
        }

    if (
        abi is not None
        and selectors
        and config.refresh_existing_abi
        and config.etherscan_enabled
        and config.etherscan_api_key
    ):
        refreshed_status, refreshed_detail, refreshed_abi = _fetch_abi_from_etherscan_v2(
            chain_id=chain_id,
            address=address,
            config=config,
        )
        if refreshed_status == "fetched_ok" and refreshed_abi is not None:
            abi = refreshed_abi
            abi_status = "fetched_ok"
            abi_source = "etherscan_v2"
            detail = refreshed_detail
            if not config.dry_run:
                _write_json(abi_path, refreshed_abi)
            if _abi_covers_selectors(abi, selectors):
                return {
                    "chain_id": chain_id,
                    "target_contract": address,
                    "abi_file": _relative_posix(abi_path, config.project_root),
                    "abi_status": abi_status,
                    "abi_source": abi_source,
                    "detail": detail,
                    "implementation_address": None,
                    "implementation_abi_file": None,
                    "implementation_abi_status": None,
                    "implementation_source": None,
                    "implementation_detail": "refreshed direct ABI covers requested selectors",
                    "used_by_samples": target.get("example_benchmark_ids", []),
                }
        elif refreshed_detail:
            detail = refreshed_detail

    implementation_address, implementation_source, implementation_detail = _resolve_implementation(
        chain_id=chain_id,
        address=address,
        config=config,
    )
    implementation_abi_status = None
    implementation_abi_file = None

    if implementation_address and implementation_address != address:
        implementation_path = _abi_path(config.abi_dir, chain_id, implementation_address)
        implementation_abi_file = _relative_posix(implementation_path, config.project_root)
        implementation_abi_status = "local_hit" if implementation_path.exists() else ""
        if not implementation_path.exists():
            (
                implementation_abi_status,
                implementation_detail,
                implementation_abi,
                implementation_abi_source,
            ) = _fetch_abi(
                chain_id=chain_id,
                address=implementation_address,
                config=config,
            )
            implementation_source = implementation_source or implementation_abi_source
            if (
                implementation_abi_status == "fetched_ok"
                and implementation_abi is not None
                and not config.dry_run
            ):
                _write_json(implementation_path, implementation_abi)

    return {
        "chain_id": chain_id,
        "target_contract": address,
        "abi_file": _relative_posix(abi_path, config.project_root),
        "abi_status": abi_status or "failed: not_attempted",
        "abi_source": abi_source,
        "detail": detail,
        "implementation_address": implementation_address,
        "implementation_abi_file": implementation_abi_file,
        "implementation_abi_status": implementation_abi_status,
        "implementation_source": implementation_source,
        "implementation_detail": implementation_detail,
        "used_by_samples": target.get("example_benchmark_ids", []),
    }


def _fetch_abi(
    *,
    chain_id: int,
    address: str,
    config: AbiFetchConfig,
) -> tuple[str, str | None, list[dict[str, Any]] | None, str]:
    source_detail = None
    if config.sourcify_enabled:
        source_status, source_detail, abi = _fetch_abi_from_sourcify(
            chain_id=chain_id,
            address=address,
            config=config,
        )
        if source_status == "fetched_ok":
            return source_status, source_detail, abi, "sourcify"

    if config.etherscan_enabled and config.etherscan_api_key:
        etherscan_status, etherscan_detail, etherscan_abi = _fetch_abi_from_etherscan_v2(
            chain_id=chain_id,
            address=address,
            config=config,
        )
        return etherscan_status, etherscan_detail or source_detail, etherscan_abi, "etherscan_v2"

    return "failed: not_verified", source_detail or "No verified ABI source succeeded.", None, "none"


def _fetch_abi_from_sourcify(
    *,
    chain_id: int,
    address: str,
    config: AbiFetchConfig,
) -> tuple[str, str | None, list[dict[str, Any]] | None]:
    last_detail = None
    for match_type in ("full_match", "partial_match"):
        for candidate in _address_candidates(address):
            url = f"{SOURCIFY_REPO_ENDPOINT}/{match_type}/{chain_id}/{candidate}/metadata.json"
            status, detail, metadata = _request_json(url, {}, config=config)
            if status == "not_found":
                last_detail = detail
                continue
            if status != "ok":
                last_detail = detail
                continue
            abi = ((metadata or {}).get("output") or {}).get("abi")
            if isinstance(abi, list):
                return "fetched_ok", None, abi
            return "failed: invalid_abi", "Sourcify metadata has no output.abi array.", None
    return "failed: not_verified", last_detail or "Sourcify metadata not found.", None


def _fetch_abi_from_etherscan_v2(
    *,
    chain_id: int,
    address: str,
    config: AbiFetchConfig,
) -> tuple[str, str | None, list[dict[str, Any]] | None]:
    params = {
        "chainid": str(chain_id),
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": config.etherscan_api_key or "",
    }
    status, detail, payload = _request_json(ETHERSCAN_V2_ENDPOINT, params, config=config)
    if status != "ok":
        return "failed: api_error", detail, None

    result = payload.get("result") if isinstance(payload, dict) else None
    if str(payload.get("status")) == "0":
        message = str(payload.get("message") or result or "")
        if _looks_unverified(message) or _looks_unverified(str(result or "")):
            return "failed: not_verified", message or str(result), None
        return "failed: api_error", message or str(result), None
    try:
        abi = json.loads(result)
    except (TypeError, ValueError) as exc:
        return "failed: invalid_abi", str(exc), None
    if not isinstance(abi, list):
        return "failed: invalid_abi", "ABI response is not a JSON array.", None
    return "fetched_ok", None, abi


def _resolve_implementation(
    *,
    chain_id: int,
    address: str,
    config: AbiFetchConfig,
) -> tuple[str | None, str | None, str | None]:
    if config.rpc_implementation_resolution_enabled:
        implementation, detail = _resolve_implementation_from_rpc(chain_id, address, config)
        if implementation:
            return implementation, "rpc_eip1967", detail

    if config.etherscan_enabled and config.etherscan_api_key:
        implementation, detail = _resolve_implementation_from_etherscan(
            chain_id=chain_id,
            address=address,
            config=config,
        )
        if implementation:
            return implementation, "etherscan_v2", detail
        return None, None, detail

    return None, None, None


def _resolve_implementation_from_rpc(
    chain_id: int,
    address: str,
    config: AbiFetchConfig,
) -> tuple[str | None, str | None]:
    rpc_url = _rpc_url_for_chain(chain_id)
    if not rpc_url:
        return None, "No RPC URL configured for chain."

    implementation_slot = _rpc_call(
        rpc_url,
        "eth_getStorageAt",
        [address, EIP1967_IMPLEMENTATION_SLOT, "latest"],
        config=config,
    )
    implementation = _address_from_storage(implementation_slot)
    if implementation:
        return implementation, None

    beacon_slot = _rpc_call(
        rpc_url,
        "eth_getStorageAt",
        [address, EIP1967_BEACON_SLOT, "latest"],
        config=config,
    )
    beacon_address = _address_from_storage(beacon_slot)
    if beacon_address:
        implementation_call = _rpc_call(
            rpc_url,
            "eth_call",
            [{"to": beacon_address, "data": BEACON_IMPLEMENTATION_SELECTOR}, "latest"],
            config=config,
        )
        implementation = _address_from_storage(implementation_call)
        if implementation:
            return implementation, f"Resolved through beacon {beacon_address}."

    return None, None


def _resolve_implementation_from_etherscan(
    *,
    chain_id: int,
    address: str,
    config: AbiFetchConfig,
) -> tuple[str | None, str | None]:
    params = {
        "chainid": str(chain_id),
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": config.etherscan_api_key or "",
    }
    status, detail, payload = _request_json(ETHERSCAN_V2_ENDPOINT, params, config=config)
    if status != "ok":
        return None, detail
    if str(payload.get("status")) == "0":
        return None, str(payload.get("message") or payload.get("result"))
    result = payload.get("result")
    if not isinstance(result, list) or not result:
        return None, "Missing getsourcecode result array."
    implementation = result[0].get("Implementation") or result[0].get("ImplementationAddress")
    return _normalize_address(implementation), None


def _request_json(
    url: str,
    params: dict[str, str],
    *,
    config: AbiFetchConfig,
) -> tuple[str, str | None, dict[str, Any]]:
    last_detail = None
    for attempt in range(1, config.max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=config.http_timeout_seconds)
            time.sleep(config.sleep_seconds)
        except requests.Timeout as exc:
            last_detail = str(exc)
            if attempt == config.max_retries:
                return "timeout", last_detail, {}
            continue
        except requests.RequestException as exc:
            last_detail = str(exc)
            if attempt == config.max_retries:
                return "api_error", last_detail, {}
            continue

        if response.status_code == 404:
            return "not_found", f"HTTP 404: {url}", {}
        if response.status_code >= 500:
            last_detail = f"HTTP {response.status_code}: {response.text[:300]}"
            if attempt == config.max_retries:
                return "api_error", last_detail, {}
            continue
        if response.status_code >= 400:
            return "api_error", f"HTTP {response.status_code}: {response.text[:300]}", {}
        try:
            payload = response.json()
        except ValueError:
            return "api_error", f"Invalid JSON response: {response.text[:300]}", {}
        return "ok", None, payload

    return "api_error", last_detail, {}


def _rpc_call(
    rpc_url: str,
    method: str,
    params: list[Any],
    *,
    config: AbiFetchConfig,
) -> str | None:
    try:
        response = requests.post(
            rpc_url,
            json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
            timeout=config.rpc_timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return None
    except ValueError:
        return None
    result = payload.get("result")
    return result if isinstance(result, str) else None


def _build_abi_target_record(target: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    return {
        "chain_id": result["chain_id"],
        "target_contract": result["target_contract"],
        "abi_file": result["abi_file"],
        "abi_status": result["abi_status"],
        "abi_source": result["abi_source"],
        "implementation_address": result["implementation_address"],
        "implementation_abi_file": result["implementation_abi_file"],
        "implementation_abi_status": result["implementation_abi_status"],
        "implementation_source": result["implementation_source"],
        "used_by_samples": result["used_by_samples"],
        "unknown_action_count": target.get("unknown_action_count"),
        "selectors": target.get("selectors", []),
        "call_types": target.get("call_types", []),
        "daos": target.get("daos", []),
    }


def _load_abi_target_index(path: Path) -> dict[tuple[int, str], dict[str, Any]]:
    records: dict[tuple[int, str], dict[str, Any]] = {}
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except ValueError:
            continue
        address = _normalize_address(record.get("target_contract"))
        chain_id = record.get("chain_id")
        if address and chain_id is not None:
            records[(int(chain_id), address)] = record
    return records


def _write_abi_target_index(path: Path, records: dict[tuple[int, str], dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [records[key] for key in sorted(records)]
    _write_jsonl(path, rows)


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_local_abi(path: Path) -> list[dict[str, Any]] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    entries = payload if isinstance(payload, list) else payload.get("abi", [])
    return entries if isinstance(entries, list) else None


def _abi_covers_selectors(abi: list[dict[str, Any]], selectors: list[str]) -> bool:
    if not selectors:
        return False
    available = {_selector_for_entry(entry) for entry in abi if isinstance(entry, dict)}
    return all(selector in available for selector in selectors)


def _selector_for_entry(entry: dict[str, Any]) -> str | None:
    if entry.get("type") != "function":
        return None
    name = entry.get("name")
    if not isinstance(name, str):
        return None
    inputs = entry.get("inputs", [])
    types = [_canonical_abi_type(item) for item in inputs if isinstance(item, dict)]
    signature = f"{name}({','.join(types)})"
    try:
        return f"0x{function_signature_to_4byte_selector(signature).hex()}".lower()
    except Exception:
        return None


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


def _build_summary(logs: list[dict[str, Any]], *, config: AbiFetchConfig) -> dict[str, Any]:
    written_or_updated = sum(
        1
        for row in logs
        if row["abi_status"] == "fetched_ok" or row["implementation_abi_status"] == "fetched_ok"
    )
    return {
        "dry_run": config.dry_run,
        "total_targets": len(logs),
        "changed_targets": written_or_updated,
        "abi_status_counts": dict(Counter(str(row["abi_status"]) for row in logs).most_common()),
        "implementation_abi_status_counts": dict(
            Counter(str(row["implementation_abi_status"]) for row in logs).most_common()
        ),
        "abi_source_counts": dict(Counter(str(row["abi_source"]) for row in logs).most_common()),
        "etherscan_api_key_detected": bool(config.etherscan_api_key),
        "failed_targets": [
            {
                "chain_id": row["chain_id"],
                "target_contract": row["target_contract"],
                "abi_status": row["abi_status"],
                "detail": row["detail"],
                "unknown_action_count": row["unknown_action_count"],
            }
            for row in logs
            if str(row["abi_status"]).startswith("failed:")
        ],
    }


def _empty_report(*, dry_run: bool) -> dict[str, Any]:
    return {
        "dry_run": dry_run,
        "total_targets": 0,
        "changed_targets": 0,
        "abi_status_counts": {},
        "implementation_abi_status_counts": {},
        "abi_source_counts": {},
        "etherscan_api_key_detected": False,
        "failed_targets": [],
    }


def _abi_path(abi_dir: Path, chain_id: int, address: str) -> Path:
    return abi_dir / str(chain_id) / f"{address.lower()}.json"


def _normalize_address(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    address = value.strip().lower()
    if not is_address(address):
        return None
    return address


def _address_from_storage(value: str | None) -> str | None:
    if not value or not isinstance(value, str) or not value.startswith("0x"):
        return None
    body = value[2:].rjust(64, "0")
    candidate = f"0x{body[-40:]}"
    if candidate == "0x0000000000000000000000000000000000000000":
        return None
    return candidate.lower() if is_address(candidate) else None


def _address_candidates(address: str) -> list[str]:
    checksum = to_checksum_address(address)
    candidates = [checksum, address.lower()]
    return list(dict.fromkeys(candidates))


def _rpc_url_for_chain(chain_id: int) -> str | None:
    env_names = {
        1: "MAINNET_RPC_URL",
        42161: "ARBITRUM_RPC_URL",
    }
    name = env_names.get(chain_id)
    if not name:
        return None
    value = os.getenv(name)
    return value if value else None


def _looks_unverified(message: str) -> bool:
    normalized = message.lower()
    return "not verified" in normalized or "source code not verified" in normalized


def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _env_path(name: str, default: str) -> Path:
    return Path(os.getenv(name, default))


def _resolve_path(root: Path, value: Path) -> Path:
    return value if value.is_absolute() else root / value


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default
