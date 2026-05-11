from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter
from pathlib import Path
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.modules.data_loader import load_proposal
from src.modules.llm.extract_proposal_semantics import extract_proposal_semantics


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract proposal semantics for all DAO proposal raw samples.")
    parser.add_argument("--samples-dir", type=Path, default=Path("data/raw_samples"))
    parser.add_argument("--semantics-dir", type=Path, default=Path("outputs/semantics"))
    parser.add_argument("--summary-dir", type=Path, default=Path("outputs/run_summaries"))
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument(
        "--rerun-failed",
        action="store_true",
        help="When used with --skip-existing, rerun existing semantics files whose llm_status is failed.",
    )
    parser.add_argument("--delay-seconds", type=float, default=0.0, help="Delay between LLM calls.")
    args = parser.parse_args()

    args.semantics_dir.mkdir(parents=True, exist_ok=True)
    args.summary_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    start = perf_counter()

    for index, sample_path in enumerate(sorted(args.samples_dir.glob("*.json")), start=1):
        item_start = perf_counter()
        proposal = load_proposal(sample_path)
        benchmark_id = proposal.metadata.get("benchmark_id") or sample_path.stem
        output = args.semantics_dir / f"{benchmark_id}-semantics.json"
        row: dict[str, object] = {
            "index": index,
            "benchmark_id": benchmark_id,
            "sample_path": str(sample_path),
            "proposal_id": proposal.proposal_id,
            "dao": proposal.metadata.get("dao", ""),
            "status": "failed",
            "llm_status": None,
            "error": None,
            "elapsed_seconds": 0.0,
            "semantics_output": str(output),
        }

        try:
            should_skip = False
            if args.skip_existing and output.exists():
                payload = json.loads(output.read_text(encoding="utf-8"))
                should_skip = not (args.rerun_failed and payload.get("llm_status") == "failed")
                if should_skip:
                    row.update({"status": "skipped", "llm_status": payload.get("llm_status")})
            if should_skip:
                pass
            else:
                if args.delay_seconds > 0:
                    time.sleep(args.delay_seconds)
                semantics = extract_proposal_semantics(proposal)
                output.write_text(json.dumps(semantics.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
                row.update({"status": "success", "llm_status": semantics.llm_status})
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
                        "llm_status": row["llm_status"],
                        "elapsed_seconds": row["elapsed_seconds"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    _write_summary(args.summary_dir, rows, perf_counter() - start)


def _write_summary(summary_dir: Path, rows: list[dict[str, object]], elapsed_seconds: float) -> None:
    summary = {
        "total_samples": len(rows),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "status_counts": dict(sorted(Counter(str(row["status"]) for row in rows).items())),
        "llm_status_counts": dict(sorted(Counter(str(row["llm_status"]) for row in rows).items())),
        "warning_rows": [
            {
                "benchmark_id": row["benchmark_id"],
                "status": row["status"],
                "llm_status": row["llm_status"],
                "error": row["error"],
            }
            for row in rows
            if row["status"] == "failed" or row["error"]
        ],
    }
    (summary_dir / "semantics-batch-summary.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    with (summary_dir / "semantics-batch-summary.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
