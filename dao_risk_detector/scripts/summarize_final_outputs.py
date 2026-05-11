from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent

DIMENSIONS = ("conflict_detection", "depth_analysis", "function_semantic_match")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a canonical offline summary from final GovGap outputs."
    )
    parser.add_argument("--samples-dir", type=Path, default=Path("data/raw_samples"))
    parser.add_argument("--decoded-dir", type=Path, default=Path("data/decoded_samples"))
    parser.add_argument("--traces-dir", type=Path, default=Path("outputs/traces"))
    parser.add_argument("--risk-actions-dir", type=Path, default=Path("outputs/risk_actions"))
    parser.add_argument("--semantics-dir", type=Path, default=Path("outputs/semantics"))
    parser.add_argument("--scores-dir", type=Path, default=Path("outputs/scores"))
    parser.add_argument("--reports-dir", type=Path, default=Path("outputs/reports"))
    parser.add_argument(
        "--sampling-report",
        type=Path,
        default=Path("../benchmark/dao_benchmark_collector/outputs/sampling_report.json"),
    )
    parser.add_argument("--summary-dir", type=Path, default=Path("outputs/derived_summaries"))
    args = parser.parse_args()

    samples_dir = _resolve_path(args.samples_dir)
    decoded_dir = _resolve_path(args.decoded_dir)
    traces_dir = _resolve_path(args.traces_dir)
    risk_actions_dir = _resolve_path(args.risk_actions_dir)
    semantics_dir = _resolve_path(args.semantics_dir)
    scores_dir = _resolve_path(args.scores_dir)
    reports_dir = _resolve_path(args.reports_dir)
    sampling_report = _resolve_path(args.sampling_report, must_exist=False)
    summary_dir = _resolve_path(args.summary_dir, must_exist=False)
    summary_dir.mkdir(parents=True, exist_ok=True)

    sample_paths = sorted(samples_dir.glob("*.json"))
    rows: list[dict[str, Any]] = []
    risk_action_type_counts: Counter[str] = Counter()

    for index, sample_path in enumerate(sample_paths, start=1):
        sample = _load_json(sample_path)
        benchmark_id = _sample_benchmark_id(sample, sample_path)
        score_path = scores_dir / f"{benchmark_id}-score.json"
        trace_path = traces_dir / f"{benchmark_id}-trace.json"
        risk_actions_path = risk_actions_dir / f"{benchmark_id}-risk-actions.json"
        semantics_path = semantics_dir / f"{benchmark_id}-semantics.json"
        report_path = reports_dir / f"{benchmark_id}-score.md"
        decoded_path = decoded_dir / f"decoded-{benchmark_id.removeprefix('real-')}.json"

        row: dict[str, Any] = {
            "index": index,
            "benchmark_id": benchmark_id,
            "dao": _sample_dao(sample),
            "chain_id": _sample_chain_id(sample),
            "proposal_id": _sample_proposal_id(sample),
            "sample_exists": True,
            "decoded_exists": decoded_path.exists(),
            "trace_exists": trace_path.exists(),
            "risk_actions_exists": risk_actions_path.exists(),
            "semantics_exists": semantics_path.exists(),
            "score_exists": score_path.exists(),
            "report_exists": report_path.exists(),
            "simulation_status": None,
            "trace_source": None,
            "llm_status": None,
            "overall_score": None,
            "risk_level": None,
            "risk_action_count": None,
            "call_count": None,
            "max_depth": None,
            "delegatecall_count": None,
            "error": None,
        }

        if score_path.exists():
            try:
                score = _load_json(score_path)
                metadata = score.get("metadata", {})
                overall = score.get("overall", {})
                semantics = score.get("proposal_semantics", {})
                trace_summary = score.get("trace_summary", {})
                risk_actions = score.get("risk_actions", [])
                dimensions = score.get("dimensions", {})

                row.update(
                    {
                        "simulation_status": metadata.get("simulation_status"),
                        "trace_source": metadata.get("trace_source"),
                        "llm_status": semantics.get("llm_status"),
                        "overall_score": overall.get("score"),
                        "risk_level": overall.get("risk_level"),
                        "risk_action_count": len(risk_actions) if isinstance(risk_actions, list) else None,
                        "call_count": len(trace_summary.get("calls", []))
                        if isinstance(trace_summary.get("calls", []), list)
                        else None,
                        "max_depth": trace_summary.get("max_depth"),
                        "delegatecall_count": trace_summary.get("delegatecall_count"),
                    }
                )
                for dimension in DIMENSIONS:
                    dimension_score = dimensions.get(dimension, {})
                    row[f"{dimension}_score"] = dimension_score.get("score")
                    row[f"{dimension}_severity"] = dimension_score.get("severity")

                if isinstance(risk_actions, list):
                    risk_action_type_counts.update(
                        str(action.get("action_type", "unknown"))
                        for action in risk_actions
                        if isinstance(action, dict)
                    )
            except Exception as exc:
                row["error"] = f"{type(exc).__name__}: {exc}"
        else:
            row["error"] = "missing score output"

        rows.append(row)

    summary = _build_summary(
        rows=rows,
        samples_dir=samples_dir,
        decoded_dir=decoded_dir,
        traces_dir=traces_dir,
        risk_actions_dir=risk_actions_dir,
        semantics_dir=semantics_dir,
        scores_dir=scores_dir,
        reports_dir=reports_dir,
        risk_action_type_counts=risk_action_type_counts,
        sampling_report=sampling_report,
    )

    _write_json(summary_dir / "final-evaluation-summary.json", {"summary": summary, "rows": rows})
    _write_csv(summary_dir / "final-evaluation-summary.csv", rows)
    (summary_dir / "paper-tables.md").write_text(
        _build_markdown_tables(summary, rows, sampling_report),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


def _resolve_path(path: Path, *, must_exist: bool = True) -> Path:
    if path.is_absolute():
        return path
    candidates = [Path.cwd() / path, PROJECT_ROOT / path, REPO_ROOT / path]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if must_exist else candidates[0]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _sample_benchmark_id(sample: dict[str, Any], path: Path) -> str:
    return str(sample.get("benchmark_id") or sample.get("metadata", {}).get("benchmark_id") or path.stem)


def _sample_dao(sample: dict[str, Any]) -> str:
    dao = sample.get("dao")
    if isinstance(dao, dict):
        return str(dao.get("name", ""))
    return str(sample.get("metadata", {}).get("dao", ""))


def _sample_chain_id(sample: dict[str, Any]) -> int | None:
    dao = sample.get("dao")
    value = dao.get("chain_id") if isinstance(dao, dict) else sample.get("chain_id")
    return int(value) if isinstance(value, int | str) and str(value).isdigit() else None


def _sample_proposal_id(sample: dict[str, Any]) -> str:
    proposal = sample.get("proposal")
    if isinstance(proposal, dict):
        return str(proposal.get("proposal_id", ""))
    return str(sample.get("proposal_id", ""))


def _build_summary(
    *,
    rows: list[dict[str, Any]],
    samples_dir: Path,
    decoded_dir: Path,
    traces_dir: Path,
    risk_actions_dir: Path,
    semantics_dir: Path,
    scores_dir: Path,
    reports_dir: Path,
    risk_action_type_counts: Counter[str],
    sampling_report: Path,
) -> dict[str, Any]:
    complete_rows = [
        row
        for row in rows
        if row["sample_exists"]
        and row["decoded_exists"]
        and row["trace_exists"]
        and row["risk_actions_exists"]
        and row["semantics_exists"]
        and row["score_exists"]
        and row["report_exists"]
        and not row["error"]
    ]
    return {
        "total_samples": len(rows),
        "complete_samples": len(complete_rows),
        "file_counts": {
            "raw_samples": _count_json(samples_dir),
            "decoded_samples": _count_json(decoded_dir),
            "traces": len(list(traces_dir.glob("*-trace.json"))),
            "risk_actions": len(list(risk_actions_dir.glob("*-risk-actions.json"))),
            "semantics": len(list(semantics_dir.glob("*-semantics.json"))),
            "scores": len(list(scores_dir.glob("*-score.json"))),
            "reports": len(list(reports_dir.glob("*-score.md"))),
        },
        "simulation_status_counts": _counter_from_rows(rows, "simulation_status"),
        "trace_source_counts": _counter_from_rows(rows, "trace_source"),
        "llm_status_counts": _counter_from_rows(rows, "llm_status"),
        "risk_level_counts": _counter_from_rows(rows, "risk_level"),
        "risk_action_type_counts": dict(risk_action_type_counts.most_common()),
        "total_risk_actions": sum(int(row["risk_action_count"] or 0) for row in rows),
        "by_dao": _summarize_by_dao(rows),
        "sampling_report_available": sampling_report.exists(),
        "warning_rows": [
            {
                "benchmark_id": row["benchmark_id"],
                "dao": row["dao"],
                "error": row["error"],
                "missing": [
                    name.removesuffix("_exists")
                    for name in (
                        "decoded_exists",
                        "trace_exists",
                        "risk_actions_exists",
                        "semantics_exists",
                        "score_exists",
                        "report_exists",
                    )
                    if not row[name]
                ],
            }
            for row in rows
            if row["error"]
            or not (
                row["decoded_exists"]
                and row["trace_exists"]
                and row["risk_actions_exists"]
                and row["semantics_exists"]
                and row["score_exists"]
                and row["report_exists"]
            )
        ],
    }


def _count_json(path: Path) -> int:
    return len(list(path.glob("*.json"))) if path.exists() else 0


def _counter_from_rows(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in rows if row[key] is not None).items()))


def _summarize_by_dao(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["dao"])].append(row)

    result: dict[str, dict[str, Any]] = {}
    for dao, dao_rows in sorted(grouped.items()):
        scores = [int(row["overall_score"]) for row in dao_rows if row["overall_score"] is not None]
        result[dao] = {
            "count": len(dao_rows),
            "risk_level_counts": _counter_from_rows(dao_rows, "risk_level"),
            "average_score": round(sum(scores) / len(scores), 2) if scores else None,
        }
    return result


def _build_markdown_tables(summary: dict[str, Any], rows: list[dict[str, Any]], sampling_report: Path) -> str:
    lines = [
        "# GovGap Paper Tables",
        "",
        "## Output Completeness",
        "",
        "| Item | Count |",
        "| --- | ---: |",
    ]
    for key, value in summary["file_counts"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Risk Levels",
            "",
            "| Risk level | Count |",
            "| --- | ---: |",
        ]
    )
    for key, value in summary["risk_level_counts"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Risk Action Types",
            "",
            "| Type | Count |",
            "| --- | ---: |",
        ]
    )
    for key, value in summary["risk_action_type_counts"].items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## DAO Breakdown",
            "",
            "| DAO | Count | CRITICAL | HIGH | MEDIUM | LOW | Average score |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for dao, item in summary["by_dao"].items():
        counts = item["risk_level_counts"]
        lines.append(
            f"| {dao} | {item['count']} | {counts.get('CRITICAL', 0)} | {counts.get('HIGH', 0)} | "
            f"{counts.get('MEDIUM', 0)} | {counts.get('LOW', 0)} | {item['average_score']} |"
        )

    if sampling_report.exists():
        sampling = _load_json(sampling_report)
        daos = sampling.get("daos", {})
        if isinstance(daos, dict):
            lines.extend(
                [
                    "",
                    "## Dataset Sampling",
                    "",
                    "| DAO | Indexed | Eligible | Sampled |",
                    "| --- | ---: | ---: | ---: |",
                ]
            )
            for dao, item in sorted(daos.items()):
                if not isinstance(item, dict):
                    continue
                lines.append(
                    f"| {dao} | {item.get('indexed_total', '')} | {item.get('eligible_total', '')} | "
                    f"{item.get('sampled_total', '')} |"
                )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Generated from final score JSON files, not from stale batch logs.",
            "- Unknown risk actions are conservative review signals, not confirmed vulnerabilities.",
        ]
    )
    if summary["warning_rows"]:
        lines.append("- Warning rows exist; inspect `final-evaluation-summary.json` before reporting numbers.")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
