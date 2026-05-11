from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.risk_action import RiskAction
from src.models.semantics import ProposalSemantics
from src.models.trace import TraceResult
from src.modules.data_loader import load_proposal
from src.modules.scoring.build_final_json import build_final_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Build final audit JSON for one sample.")
    parser.add_argument("sample", type=Path)
    parser.add_argument("--trace", type=Path, default=None)
    parser.add_argument("--risk-actions", type=Path, default=None)
    parser.add_argument("--semantics", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    proposal = load_proposal(args.sample)
    output_id = proposal.metadata.get("benchmark_id") or args.sample.stem
    trace_path = args.trace or Path("outputs/traces") / f"{output_id}-trace.json"
    risk_actions_path = args.risk_actions or Path("outputs/risk_actions") / f"{output_id}-risk-actions.json"
    semantics_path = args.semantics or Path("outputs/semantics") / f"{output_id}-semantics.json"
    output_path = args.output or Path("outputs/scores") / f"{output_id}-score.json"

    trace = TraceResult.model_validate(json.loads(trace_path.read_text(encoding="utf-8")))
    risk_actions_payload = json.loads(risk_actions_path.read_text(encoding="utf-8"))
    risk_action_items = (
        risk_actions_payload.get("risk_actions", [])
        if isinstance(risk_actions_payload, dict)
        else risk_actions_payload
    )
    risk_actions = [RiskAction.model_validate(item) for item in risk_action_items]
    semantics = ProposalSemantics.model_validate(json.loads(semantics_path.read_text(encoding="utf-8")))

    final_json = build_final_json(proposal, trace, risk_actions, semantics)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(final_json.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "proposal_id": proposal.proposal_id,
                "overall_score": final_json.overall.score,
                "risk_level": final_json.overall.risk_level,
                "output": str(output_path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
