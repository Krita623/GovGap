from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.modules.data_loader import load_proposal
from src.modules.llm.extract_proposal_semantics import extract_proposal_semantics


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract proposal text semantics for one sample.")
    parser.add_argument("sample", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    proposal = load_proposal(args.sample)
    semantics = extract_proposal_semantics(proposal)
    output_id = proposal.metadata.get("benchmark_id") or args.sample.stem
    output = args.output or Path("outputs/semantics") / f"{output_id}-semantics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(semantics.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"proposal_id": proposal.proposal_id, "llm_status": semantics.llm_status, "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
