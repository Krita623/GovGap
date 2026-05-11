from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.modules.data_loader import load_proposal
from src.modules.trace.extract_risk_actions import extract_risk_actions_with_summary
from src.modules.trace.simulate_payload import simulate_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate all DAO proposal raw samples.")
    parser.add_argument("--samples-dir", type=Path, default=Path("data/raw_samples"))
    parser.add_argument("--traces-dir", type=Path, default=Path("outputs/traces"))
    parser.add_argument("--risk-actions-dir", type=Path, default=Path("outputs/risk_actions"))
    parser.add_argument("--summary-dir", type=Path, default=Path("outputs/run_summaries"))
    parser.add_argument(
        "--require-anvil",
        action="store_true",
        help="Stop the batch if a sample cannot use simulated_trace.",
    )
    args = parser.parse_args()

    args.traces_dir.mkdir(parents=True, exist_ok=True)
    args.risk_actions_dir.mkdir(parents=True, exist_ok=True)
    args.summary_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    start = perf_counter()

    for index, sample_path in enumerate(sorted(args.samples_dir.glob("*.json")), start=1):
        item_start = perf_counter()
        proposal = load_proposal(sample_path)
        benchmark_id = proposal.metadata.get("benchmark_id") or sample_path.stem
        trace_output = args.traces_dir / f"{benchmark_id}-trace.json"
        risk_actions_output = args.risk_actions_dir / f"{benchmark_id}-risk-actions.json"

        row: dict[str, object] = {
            "index": index,
            "benchmark_id": benchmark_id,
            "sample_path": str(sample_path),
            "proposal_id": proposal.proposal_id,
            "dao": proposal.metadata.get("dao", ""),
            "chain_id": proposal.chain_id,
            "simulation_status": "failed",
            "trace_source": None,
            "call_count": 0,
            "max_depth": 0,
            "delegatecall_count": 0,
            "risk_action_count": 0,
            "raw_detected_count": 0,
            "filtered_count": 0,
            "deduplicated_count": 0,
            "risk_action_types": "",
            "error": None,
            "elapsed_seconds": 0.0,
            "trace_output": str(trace_output),
            "risk_actions_output": str(risk_actions_output),
        }

        try:
            trace_result = simulate_payload(proposal)
            extraction = extract_risk_actions_with_summary(trace_result)
            risk_actions = extraction["risk_actions"]
            filtering_summary = extraction["filtering_summary"]

            trace_output.write_text(
                json.dumps(trace_result.model_dump(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            risk_actions_output.write_text(
                json.dumps(
                    {
                        "risk_actions": [action.model_dump() for action in risk_actions],
                        "filtering_summary": filtering_summary,
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            parsed = trace_result.parsed_trace
            action_type_counts = Counter(action.action_type.value for action in risk_actions)
            row.update(
                {
                    "simulation_status": trace_result.simulation_status.value,
                    "trace_source": trace_result.trace_source,
                    "call_count": len(parsed.calls) if parsed else 0,
                    "max_depth": parsed.max_depth if parsed else 0,
                    "delegatecall_count": parsed.delegatecall_count if parsed else 0,
                    "risk_action_count": len(risk_actions),
                    "raw_detected_count": filtering_summary["raw_detected_count"],
                    "filtered_count": filtering_summary["filtered_count"],
                    "deduplicated_count": filtering_summary["deduplicated_count"],
                    "risk_action_types": ";".join(
                        f"{action_type}:{count}" for action_type, count in sorted(action_type_counts.items())
                    ),
                    "error": trace_result.error,
                }
            )
            if args.require_anvil and trace_result.trace_source != "simulated_trace":
                row["error"] = row["error"] or "required Anvil simulated_trace but got fallback trace source"
                raise RuntimeError(str(row["error"]))
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
            if args.require_anvil:
                row["elapsed_seconds"] = round(perf_counter() - item_start, 3)
                rows.append(row)
                print(
                    json.dumps(
                        {
                            "index": index,
                            "benchmark_id": benchmark_id,
                            "status": row["simulation_status"],
                            "source": row["trace_source"],
                            "calls": row["call_count"],
                            "risk_actions": row["risk_action_count"],
                            "elapsed_seconds": row["elapsed_seconds"],
                            "error": row["error"],
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                _write_outputs(args.summary_dir, rows, perf_counter() - start)
                raise SystemExit(1)
        finally:
            if row not in rows:
                row["elapsed_seconds"] = round(perf_counter() - item_start, 3)
                rows.append(row)
                print(
                    json.dumps(
                        {
                            "index": index,
                            "benchmark_id": benchmark_id,
                            "status": row["simulation_status"],
                            "source": row["trace_source"],
                            "calls": row["call_count"],
                            "risk_actions": row["risk_action_count"],
                            "elapsed_seconds": row["elapsed_seconds"],
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )

    _write_outputs(args.summary_dir, rows, perf_counter() - start)


def _summarize(rows: list[dict[str, object]], elapsed_seconds: float) -> dict[str, object]:
    status_counts = Counter(str(row["simulation_status"]) for row in rows)
    source_counts = Counter(str(row["trace_source"]) for row in rows)
    risk_positive = sum(1 for row in rows if int(row["risk_action_count"]) > 0)
    trace_with_calls = sum(1 for row in rows if int(row["call_count"]) > 0)
    return {
        "total_samples": len(rows),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "simulation_status_counts": dict(sorted(status_counts.items())),
        "trace_source_counts": dict(sorted(source_counts.items())),
        "trace_with_calls": trace_with_calls,
        "trace_without_calls": len(rows) - trace_with_calls,
        "risk_action_positive": risk_positive,
        "risk_action_empty": len(rows) - risk_positive,
        "total_risk_actions": sum(int(row["risk_action_count"]) for row in rows),
        "raw_detected_count": sum(int(row["raw_detected_count"]) for row in rows),
        "filtered_count": sum(int(row["filtered_count"]) for row in rows),
        "deduplicated_count": sum(int(row["deduplicated_count"]) for row in rows),
        "warning_rows": [
            {
                "benchmark_id": row["benchmark_id"],
                "simulation_status": row["simulation_status"],
                "trace_source": row["trace_source"],
                "error": row["error"],
            }
            for row in rows
            if row["simulation_status"] == "failed" or row["error"]
        ],
    }


def _write_outputs(summary_dir: Path, rows: list[dict[str, object]], elapsed_seconds: float) -> None:
    summary = _summarize(rows, elapsed_seconds)
    (summary_dir / "batch-summary.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (summary_dir / "batch-summary.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
