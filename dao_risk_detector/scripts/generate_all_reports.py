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

from src.modules.report.generate_markdown_report import write_markdown_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Markdown reports for all final audit JSON files.")
    parser.add_argument("--scores-dir", type=Path, default=Path("outputs/scores"))
    parser.add_argument("--reports-dir", type=Path, default=Path("outputs/reports"))
    parser.add_argument("--summary-dir", type=Path, default=Path("outputs/run_summaries"))
    args = parser.parse_args()

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    args.summary_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    start = perf_counter()

    for index, score_path in enumerate(sorted(args.scores_dir.glob("*-score.json")), start=1):
        item_start = perf_counter()
        report_path = args.reports_dir / f"{score_path.stem}.md"
        row: dict[str, object] = {
            "index": index,
            "score_input": str(score_path),
            "report_output": str(report_path),
            "proposal_id": None,
            "status": "failed",
            "overall_score": None,
            "risk_level": None,
            "error": None,
            "elapsed_seconds": 0.0,
        }

        try:
            final_audit = json.loads(score_path.read_text(encoding="utf-8"))
            write_markdown_report(final_audit, report_path)
            row.update(
                {
                    "status": "success",
                    "proposal_id": final_audit.get("metadata", {}).get("proposal_id"),
                    "overall_score": final_audit.get("overall", {}).get("score"),
                    "risk_level": final_audit.get("overall", {}).get("risk_level"),
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
                        "status": row["status"],
                        "score": row["overall_score"],
                        "risk_level": row["risk_level"],
                        "elapsed_seconds": row["elapsed_seconds"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    _write_summary(args.summary_dir, rows, perf_counter() - start)


def _write_summary(summary_dir: Path, rows: list[dict[str, object]], elapsed_seconds: float) -> None:
    summary = {
        "total_scores": len(rows),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "status_counts": dict(sorted(Counter(str(row["status"]) for row in rows).items())),
        "risk_level_counts": dict(sorted(Counter(str(row["risk_level"]) for row in rows).items())),
        "report_success_count": sum(1 for row in rows if row["status"] == "success"),
        "warning_rows": [
            {
                "score_input": row["score_input"],
                "status": row["status"],
                "error": row["error"],
            }
            for row in rows
            if row["status"] == "failed" or row["error"]
        ],
    }
    (summary_dir / "reports-batch-summary.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    with (summary_dir / "reports-batch-summary.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
