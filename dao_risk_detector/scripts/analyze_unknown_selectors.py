from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.abi import get_function_signature_from_abi


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze remaining unknown risk selectors.")
    parser.add_argument("--scores-dir", type=Path, default=Path("outputs/scores"))
    parser.add_argument("--samples-dir", type=Path, default=Path("data/raw_samples"))
    parser.add_argument("--abi-dir", type=Path, default=Path("data/abis"))
    parser.add_argument("--abi-targets", type=Path, default=Path("data/abi_targets.jsonl"))
    parser.add_argument("--output-dir", type=Path, default=Path("analysis/unknown_selectors"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    sample_meta = _load_sample_meta(args.samples_dir)
    implementation_index = _load_implementation_index(args.abi_targets)
    rows: list[dict[str, Any]] = []

    for score_path in sorted(args.scores_dir.glob("*-score.json")):
        benchmark_id = score_path.name.removesuffix("-score.json")
        score = json.loads(score_path.read_text(encoding="utf-8"))
        chain_id = score.get("metadata", {}).get("chain_id")
        for action in score.get("risk_actions", []):
            if not isinstance(action, dict) or action.get("action_type") != "unknown":
                continue
            to_address = _normalize_address(action.get("to_address"))
            selector = str(action.get("function_selector") or "").lower()
            raw = action.get("raw_evidence", {})
            call_type = str(raw.get("call_type") or "").upper() if isinstance(raw, dict) else ""
            input_data = str(raw.get("input") or "") if isinstance(raw, dict) else ""
            output_data = raw.get("output") if isinstance(raw, dict) else None
            error = raw.get("error") if isinstance(raw, dict) else None
            direct_abi = _abi_path(args.abi_dir, chain_id, to_address)
            implementation_paths = implementation_index.get((int(chain_id), to_address), []) if chain_id else []
            resolver_signature = get_function_signature_from_abi(
                int(chain_id) if isinstance(chain_id, int) else None,
                to_address,
                selector,
            )

            rows.append(
                {
                    "benchmark_id": benchmark_id,
                    "dao": sample_meta.get(benchmark_id, {}).get("dao", ""),
                    "proposal_id": score.get("metadata", {}).get("proposal_id"),
                    "chain_id": chain_id,
                    "selector": selector or "missing",
                    "to_address": to_address or "",
                    "from_address": _normalize_address(action.get("from_address")) or "",
                    "call_type": call_type,
                    "depth": action.get("depth"),
                    "value": action.get("value"),
                    "error": error or "",
                    "input_bytes": _hex_bytes_len(input_data),
                    "output_bytes": _hex_bytes_len(str(output_data or "")),
                    "has_direct_abi": direct_abi.exists() if direct_abi else False,
                    "direct_abi_path": str(direct_abi) if direct_abi and direct_abi.exists() else "",
                    "implementation_abi_count": len(implementation_paths),
                    "implementation_abi_paths": ";".join(str(path) for path in implementation_paths),
                    "resolver_signature": resolver_signature or "",
                    "likely_reason": _classify_reason(
                        selector=selector,
                        direct_abi_exists=direct_abi.exists() if direct_abi else False,
                        implementation_abi_count=len(implementation_paths),
                        resolver_signature=resolver_signature,
                        call_type=call_type,
                        error=str(error or ""),
                    ),
                }
            )

    summary = _summarize(rows)
    _write_json(args.output_dir / "unknown-selector-summary.json", summary)
    _write_csv(args.output_dir / "unknown-selector-rows.csv", rows)
    _write_jsonl(args.output_dir / "missing-trace-abi-targets.jsonl", _build_missing_targets(rows))
    (args.output_dir / "unknown-selector-top.md").write_text(_build_markdown(summary), encoding="utf-8")
    print(
        json.dumps(
            {
                "total_unknown_actions": summary["total_unknown_actions"],
                "unique_selectors": summary["unique_selectors"],
                "unique_target_addresses": summary["unique_target_addresses"],
                "reason_counts": summary["reason_counts"],
                "call_type_counts": summary["call_type_counts"],
            },
            indent=2,
            ensure_ascii=False,
        ),
        flush=True,
    )


def _load_sample_meta(samples_dir: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(samples_dir.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        benchmark_id = str(payload.get("benchmark_id") or path.stem)
        dao = payload.get("dao", {})
        proposal = payload.get("proposal", {})
        result[benchmark_id] = {
            "dao": dao.get("name", "") if isinstance(dao, dict) else "",
            "proposal_id": proposal.get("proposal_id", "") if isinstance(proposal, dict) else "",
        }
    return result


def _load_implementation_index(path: Path) -> dict[tuple[int, str], list[Path]]:
    result: dict[tuple[int, str], list[Path]] = defaultdict(list)
    if not path.exists():
        return {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except ValueError:
            continue
        chain_id = record.get("chain_id")
        target = _normalize_address(record.get("target_contract"))
        implementation_abi_file = record.get("implementation_abi_file")
        implementation_address = _normalize_address(record.get("implementation_address"))
        if chain_id is None or not target:
            continue
        if implementation_abi_file:
            candidate = PROJECT_ROOT / str(implementation_abi_file)
            if candidate.exists():
                result[(int(chain_id), target)].append(candidate)
        if implementation_address:
            candidate = PROJECT_ROOT / "data" / "abis" / str(chain_id) / f"{implementation_address}.json"
            if candidate.exists():
                result[(int(chain_id), target)].append(candidate)
    return {key: list(dict.fromkeys(paths)) for key, paths in result.items()}


def _abi_path(abi_dir: Path, chain_id: object, address: str | None) -> Path | None:
    if chain_id is None or not address:
        return None
    return abi_dir / str(chain_id) / f"{address}.json"


def _normalize_address(value: object) -> str | None:
    return str(value).lower() if isinstance(value, str) and value else None


def _hex_bytes_len(value: str) -> int:
    if not value.startswith("0x"):
        return 0
    body = value[2:]
    return len(body) // 2


def _classify_reason(
    *,
    selector: str,
    direct_abi_exists: bool,
    implementation_abi_count: int,
    resolver_signature: str | None,
    call_type: str,
    error: str,
) -> str:
    if resolver_signature:
        return "resolver_can_decode_but_action_remained_unknown"
    if not selector or selector == "missing":
        return "missing_selector"
    if not direct_abi_exists and implementation_abi_count == 0:
        return "abi_missing_for_trace_target"
    if direct_abi_exists or implementation_abi_count:
        return "selector_not_in_available_abi"
    if call_type == "STATICCALL":
        return "staticcall_without_abi"
    if error:
        return "reverted_unknown_call"
    return "unknown"


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    selector_counts = Counter(str(row["selector"]) for row in rows)
    reason_counts = Counter(str(row["likely_reason"]) for row in rows)
    dao_counts = Counter(str(row["dao"]) for row in rows)
    call_type_counts = Counter(str(row["call_type"]) for row in rows)
    address_counts = Counter(str(row["to_address"]) for row in rows)
    missing_abi_rows = [row for row in rows if row["likely_reason"] == "abi_missing_for_trace_target"]
    selector_not_in_abi_rows = [row for row in rows if row["likely_reason"] == "selector_not_in_available_abi"]
    return {
        "total_unknown_actions": len(rows),
        "unique_selectors": len(selector_counts),
        "unique_target_addresses": len(address_counts),
        "reason_counts": dict(reason_counts.most_common()),
        "dao_counts": dict(dao_counts.most_common()),
        "call_type_counts": dict(call_type_counts.most_common()),
        "top_selectors": [
            _with_examples(selector, count, rows, "selector")
            for selector, count in selector_counts.most_common(20)
        ],
        "top_target_addresses": [
            _with_examples(address, count, rows, "to_address")
            for address, count in address_counts.most_common(20)
        ],
        "missing_abi_targets": [
            _with_examples(address, count, missing_abi_rows, "to_address")
            for address, count in Counter(str(row["to_address"]) for row in missing_abi_rows).most_common(20)
        ],
        "selector_not_in_available_abi": [
            _with_examples(selector, count, selector_not_in_abi_rows, "selector")
            for selector, count in Counter(str(row["selector"]) for row in selector_not_in_abi_rows).most_common(20)
        ],
    }


def _with_examples(value: str, count: int, rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    examples = [
        {
            "benchmark_id": row["benchmark_id"],
            "dao": row["dao"],
            "selector": row["selector"],
            "to_address": row["to_address"],
            "call_type": row["call_type"],
            "likely_reason": row["likely_reason"],
        }
        for row in rows
        if str(row[key]) == value
    ][:5]
    return {"value": value, "count": count, "examples": examples}


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def _build_missing_targets(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("likely_reason") != "abi_missing_for_trace_target":
            continue
        chain_id = row.get("chain_id")
        target = row.get("to_address")
        if chain_id is None or not target:
            continue
        grouped[(int(chain_id), str(target))].append(row)

    targets: list[dict[str, Any]] = []
    for (chain_id, target), target_rows in grouped.items():
        targets.append(
            {
                "chain_id": chain_id,
                "target_contract": target,
                "unknown_action_count": len(target_rows),
                "selectors": sorted({str(row["selector"]) for row in target_rows}),
                "call_types": sorted({str(row["call_type"]) for row in target_rows if row.get("call_type")}),
                "daos": sorted({str(row["dao"]) for row in target_rows if row.get("dao")}),
                "example_benchmark_ids": sorted({str(row["benchmark_id"]) for row in target_rows})[:10],
            }
        )
    return sorted(targets, key=lambda item: (-int(item["unknown_action_count"]), item["target_contract"]))


def _build_markdown(summary: dict[str, Any]) -> str:
    lines = ["# Unknown Selector Analysis", ""]
    lines.extend(_table("Reason Counts", summary["reason_counts"]))
    lines.extend(_table("DAO Counts", summary["dao_counts"]))
    lines.extend(_table("Call Type Counts", summary["call_type_counts"]))
    lines.extend(["## Top Selectors", "", "| Selector | Count | Example samples |", "| --- | ---: | --- |"])
    for item in summary["top_selectors"]:
        examples = ", ".join(example["benchmark_id"] for example in item["examples"])
        lines.append(f"| {item['value']} | {item['count']} | {examples} |")
    lines.extend(["", "## Missing ABI Targets", "", "| Address | Count | Example samples |", "| --- | ---: | --- |"])
    for item in summary["missing_abi_targets"]:
        examples = ", ".join(example["benchmark_id"] for example in item["examples"])
        lines.append(f"| {item['value']} | {item['count']} | {examples} |")
    return "\n".join(lines) + "\n"


def _table(title: str, counts: dict[str, int]) -> list[str]:
    lines = [f"## {title}", "", "| Value | Count |", "| --- | ---: |"]
    for value, count in counts.items():
        lines.append(f"| {value} | {count} |")
    lines.append("")
    return lines


if __name__ == "__main__":
    main()
