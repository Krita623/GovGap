from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.modules.abi.trace_abi_preparer import (
    AbiFetchConfig,
    load_abi_target_records_jsonl,
    prepare_trace_abis_for_targets,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch detector-local ABIs for trace-internal targets."
    )
    parser.add_argument(
        "--missing-targets",
        type=Path,
        default=Path("analysis/unknown_selectors/missing-trace-abi-targets.jsonl"),
    )
    parser.add_argument("--abi-dir", type=Path, default=None)
    parser.add_argument("--abi-targets", type=Path, default=None)
    parser.add_argument("--analysis-dir", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    targets = load_abi_target_records_jsonl(args.missing_targets)
    if args.limit > 0:
        targets = targets[: args.limit]

    config = AbiFetchConfig.from_env(
        abi_dir=args.abi_dir,
        abi_targets_path=args.abi_targets,
        analysis_dir=args.analysis_dir,
        dry_run=args.dry_run,
    )
    summary = prepare_trace_abis_for_targets(
        targets,
        config=config,
        write_diagnostics=True,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
