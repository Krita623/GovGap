from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from time import perf_counter
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.risk_action import RiskActionType
from src.models.semantics import ProposalSemantics
from src.models.trace import TraceResult
from src.modules.abi.trace_abi_preparer import (
    AbiFetchConfig,
    prepare_trace_abis_for_parsed_trace,
)
from src.modules.data_loader import load_proposal
from src.modules.report.generate_markdown_report import write_markdown_report
from src.modules.scoring.build_final_json import build_final_json
from src.modules.trace.extract_risk_actions import extract_risk_actions_with_summary
from src.modules.trace.parse_trace import parse_raw_trace


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Offline reparse existing raw traces with the current ABI resolver."
    )
    parser.add_argument("--samples-dir", type=Path, default=Path("data/raw_samples"))
    parser.add_argument("--traces-dir", type=Path, default=Path("outputs/traces"))
    parser.add_argument("--risk-actions-dir", type=Path, default=Path("outputs/risk_actions"))
    parser.add_argument("--semantics-dir", type=Path, default=Path("outputs/semantics"))
    parser.add_argument("--scores-dir", type=Path, default=Path("outputs/scores"))
    parser.add_argument("--reports-dir", type=Path, default=Path("outputs/reports"))
    parser.add_argument("--summary-dir", type=Path, default=Path("outputs/reparse_summaries"))
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute the reparsed outputs but do not write trace/risk/score/report files.",
    )
    parser.add_argument(
        "--fetch-missing-abis",
        action="store_true",
        help="Fetch detector-local ABIs for unresolved trace call targets before the final reparse.",
    )
    args = parser.parse_args()

    args.risk_actions_dir.mkdir(parents=True, exist_ok=True)
    args.scores_dir.mkdir(parents=True, exist_ok=True)
    args.reports_dir.mkdir(parents=True, exist_ok=True)
    args.summary_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    start = perf_counter()

    for index, sample_path in enumerate(sorted(args.samples_dir.glob("*.json")), start=1):
        item_start = perf_counter()
        proposal = load_proposal(sample_path)
        benchmark_id = str(proposal.metadata.get("benchmark_id") or sample_path.stem)
        trace_path = args.traces_dir / f"{benchmark_id}-trace.json"
        risk_actions_path = args.risk_actions_dir / f"{benchmark_id}-risk-actions.json"
        semantics_path = args.semantics_dir / f"{benchmark_id}-semantics.json"
        score_path = args.scores_dir / f"{benchmark_id}-score.json"
        report_path = args.reports_dir / f"{benchmark_id}-score.md"

        row: dict[str, Any] = {
            "index": index,
            "benchmark_id": benchmark_id,
            "dao": proposal.metadata.get("dao", ""),
            "proposal_id": proposal.proposal_id,
            "status": "failed",
            "old_decoded_call_count": None,
            "new_decoded_call_count": None,
            "old_unknown_risk_actions": None,
            "new_unknown_risk_actions": None,
            "old_risk_action_count": None,
            "new_risk_action_count": None,
            "overall_score": None,
            "risk_level": None,
            "abi_fetch_targets": None,
            "abi_fetch_changed_targets": None,
            "error": None,
            "elapsed_seconds": 0.0,
        }

        try:
            trace = TraceResult.model_validate(json.loads(trace_path.read_text(encoding="utf-8")))
            old_risk_actions = _load_risk_actions(risk_actions_path)
            raw_traces = _extract_raw_trace_payloads(trace)
            parsed = parse_raw_trace(raw_traces, proposal.chain_id)
            abi_fetch_report = None
            if args.fetch_missing_abis:
                abi_fetch_report = prepare_trace_abis_for_parsed_trace(
                    parsed,
                    proposal.chain_id,
                    sample_id=benchmark_id,
                    config=AbiFetchConfig.from_env(dry_run=args.dry_run),
                    write_diagnostics=False,
                )
                if int(abi_fetch_report.get("changed_targets") or 0) > 0:
                    parsed = parse_raw_trace(raw_traces, proposal.chain_id)
            reparsed_trace = trace.model_copy(update={"parsed_trace": parsed})
            extraction = extract_risk_actions_with_summary(reparsed_trace)
            new_risk_actions = extraction["risk_actions"]
            final_json = build_final_json(
                proposal,
                reparsed_trace,
                new_risk_actions,
                ProposalSemantics.model_validate(json.loads(semantics_path.read_text(encoding="utf-8"))),
            )

            row.update(
                {
                    "status": "success",
                    "old_decoded_call_count": _decoded_call_count(trace),
                    "new_decoded_call_count": _decoded_call_count(reparsed_trace),
                    "old_unknown_risk_actions": _unknown_risk_action_count(old_risk_actions),
                    "new_unknown_risk_actions": _unknown_risk_action_count(new_risk_actions),
                    "old_risk_action_count": len(old_risk_actions),
                    "new_risk_action_count": len(new_risk_actions),
                    "overall_score": final_json.overall.score,
                    "risk_level": final_json.overall.risk_level,
                    "abi_fetch_targets": (
                        abi_fetch_report.get("total_targets") if abi_fetch_report else None
                    ),
                    "abi_fetch_changed_targets": (
                        abi_fetch_report.get("changed_targets") if abi_fetch_report else None
                    ),
                }
            )

            if not args.dry_run:
                trace_path.write_text(
                    json.dumps(reparsed_trace.model_dump(), indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                risk_actions_path.write_text(
                    json.dumps(
                        {
                            "risk_actions": [action.model_dump() for action in new_risk_actions],
                            "filtering_summary": extraction["filtering_summary"],
                        },
                        indent=2,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )
                score_path.write_text(
                    json.dumps(final_json.model_dump(), indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                write_markdown_report(final_json.model_dump(), report_path)
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
        finally:
            row["elapsed_seconds"] = round(perf_counter() - item_start, 3)
            rows.append(row)
            print(
                json.dumps(
                    {
                        "index": index,
                        "benchmark_id": benchmark_id,
                        "status": row["status"],
                        "old_unknown": row["old_unknown_risk_actions"],
                        "new_unknown": row["new_unknown_risk_actions"],
                        "risk_level": row["risk_level"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    _write_summary(args.summary_dir, rows, perf_counter() - start, dry_run=args.dry_run)


def _extract_raw_trace_payloads(trace: TraceResult) -> list[object] | dict[str, object]:
    payload_traces = trace.raw_trace.get("payload_traces")
    if isinstance(payload_traces, list):
        traces = [item.get("trace") for item in payload_traces if isinstance(item, dict) and item.get("trace")]
        if traces:
            return traces
    calls = trace.raw_trace.get("calls")
    if isinstance(calls, list):
        return list(calls)
    return trace.raw_trace


def _load_risk_actions(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("risk_actions", []) if isinstance(payload, dict) else payload
    return [item for item in items if isinstance(item, dict)]


def _unknown_risk_action_count(actions: list[object]) -> int:
    return sum(
        1
        for action in actions
        if (
            action.action_type == RiskActionType.UNKNOWN
            if hasattr(action, "action_type")
            else isinstance(action, dict) and action.get("action_type") == "unknown"
        )
    )


def _decoded_call_count(trace: TraceResult) -> int:
    if not trace.parsed_trace:
        return 0
    return sum(1 for call in trace.parsed_trace.calls if call.decoded_function)


def _write_summary(
    summary_dir: Path,
    rows: list[dict[str, Any]],
    elapsed_seconds: float,
    *,
    dry_run: bool,
) -> None:
    summary = {
        "dry_run": dry_run,
        "total_samples": len(rows),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "status_counts": dict(sorted(Counter(str(row["status"]) for row in rows).items())),
        "risk_level_counts": dict(sorted(Counter(str(row["risk_level"]) for row in rows).items())),
        "old_unknown_risk_actions": sum(int(row["old_unknown_risk_actions"] or 0) for row in rows),
        "new_unknown_risk_actions": sum(int(row["new_unknown_risk_actions"] or 0) for row in rows),
        "old_decoded_call_count": sum(int(row["old_decoded_call_count"] or 0) for row in rows),
        "new_decoded_call_count": sum(int(row["new_decoded_call_count"] or 0) for row in rows),
        "warning_rows": [
            {
                "benchmark_id": row["benchmark_id"],
                "status": row["status"],
                "error": row["error"],
            }
            for row in rows
            if row["status"] == "failed" or row["error"]
        ],
    }
    suffix = "dry-run" if dry_run else "applied"
    (summary_dir / f"reparse-existing-traces-{suffix}.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    with (summary_dir / f"reparse-existing-traces-{suffix}.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
