from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.modules.report.generate_markdown_report import write_markdown_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Markdown Semantic Gap audit report from final_audit JSON.")
    parser.add_argument("final_audit", type=Path, help="Path to final audit JSON.")
    parser.add_argument("--output", type=Path, default=None, help="Markdown output path.")
    args = parser.parse_args()

    final_audit = json.loads(args.final_audit.read_text(encoding="utf-8"))
    output_path = args.output or Path("outputs/reports") / f"{args.final_audit.stem}.md"
    write_markdown_report(final_audit, output_path)
    print(json.dumps({"report_output": str(output_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
