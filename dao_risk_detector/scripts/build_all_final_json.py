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

from src.models.risk_action import RiskAction
from src.models.semantics import ProposalSemantics
from src.models.trace import TraceResult
from src.modules.data_loader import load_proposal
from src.modules.scoring.build_final_json import build_final_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Build final deterministic audit JSON for all samples.")
    parser.add_argument("--samples-dir", type=Path, default=Path("data/raw_samples"))
    parser.add_argument("--traces-dir", type=Path, default=Path("outputs/traces"))
    parser.add_argument("--risk-actions-dir", type=Path, default=Path("outputs/risk_actions"))
    parser.add_argument("--semantics-dir", type=Path, default=Path("outputs/semantics"))
    parser.add_argument("--scores-dir", type=Path, default=Path("outputs/scores"))
    parser.add_argument("--summary-dir", type=Path, default=Path("outputs/run_summaries"))
    args = parser.parse_args()

    args.scores_dir.mkdir(parents=True, exist_ok=True)
    args.summary_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    start = perf_counter()

    for index, sample_path in enumerate(sorted(args.samples_dir.glob("*.json")), start=1):
        item_start = perf_counter()
        proposal = load_proposal(sample_path)
        benchmark_id = proposal.metadata.get("benchmark_id") or sample_path.stem
        trace_path = args.traces_dir / f"{benchmark_id}-trace.json"
        risk_actions_path = args.risk_actions_dir / f"{benchmark_id}-risk-actions.json"
        semantics_path = args.semantics_dir / f"{benchmark_id}-semantics.json"
        score_path = args.scores_dir / f"{benchmark_id}-score.json"
        row: dict[str, object] = {
            "index": index,
            "benchmark_id": benchmark_id,
            "sample_path": str(sample_path),
            "proposal_id": proposal.proposal_id,
            "dao": proposal.metadata.get("dao", ""),
            "chain_id": proposal.chain_id,
            "status": "failed",
            "simulation_status": None,
            "trace_source": None,
            "risk_action_count": 0,
            "llm_status": None,
            "overall_score": None,
            "risk_level": None,
            "error": None,
            "elapsed_seconds": 0.0,
            "trace_input": str(trace_path),
            "risk_actions_input": str(risk_actions_path),
            "semantics_input": str(semantics_path),
            "score_output": str(score_path),
        }

        try:
            trace = TraceResult.model_validate(json.loads(trace_path.read_text(encoding="utf-8")))
            risk_actions = _load_risk_actions(risk_actions_path)
            semantics = ProposalSemantics.model_validate(json.loads(semantics_path.read_text(encoding="utf-8")))
            final_json = build_final_json(proposal, trace, risk_actions, semantics)
            score_path.write_text(json.dumps(final_json.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
            row.update(
                {
                    "status": "success",
                    "simulation_status": trace.simulation_status.value,
                    "trace_source": trace.trace_source,
                    "risk_action_count": len(risk_actions),
                    "llm_status": semantics.llm_status,
                    "overall_score": final_json.overall.score,
                    "risk_level": final_json.overall.risk_level,
                }
            )
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
                        "overall_score": row["overall_score"],
                        "risk_level": row["risk_level"],
                        "elapsed_seconds": row["elapsed_seconds"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    _write_summary(args.summary_dir, rows, perf_counter() - start)


def _load_risk_actions(path: Path) -> list[RiskAction]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("risk_actions", []) if isinstance(payload, dict) else payload
    return [RiskAction.model_validate(item) for item in items]


def _write_summary(summary_dir: Path, rows: list[dict[str, object]], elapsed_seconds: float) -> None:
    summary = {
        "total_samples": len(rows),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "status_counts": dict(sorted(Counter(str(row["status"]) for row in rows).items())),
        "trace_source_counts": dict(sorted(Counter(str(row["trace_source"]) for row in rows).items())),
        "risk_level_counts": dict(sorted(Counter(str(row["risk_level"]) for row in rows).items())),
        "score_success_count": sum(1 for row in rows if row["status"] == "success"),
        "total_risk_actions": sum(int(row["risk_action_count"] or 0) for row in rows),
        "warning_rows": [
            {
                "benchmark_id": row["benchmark_id"],
                "status": row["status"],
                "trace_source": row["trace_source"],
                "error": row["error"],
            }
            for row in rows
            if row["status"] == "failed" or row["error"]
        ],
    }
    (summary_dir / "scores-batch-summary.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    with (summary_dir / "scores-batch-summary.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
