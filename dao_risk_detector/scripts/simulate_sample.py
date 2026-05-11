from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.modules.data_loader import load_proposal
from src.modules.trace.extract_risk_actions import extract_risk_actions_with_summary
from src.modules.trace.simulate_payload import simulate_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate one DAO proposal payload sample.")
    parser.add_argument("sample", type=Path, help="Path to a raw proposal JSON sample.")
    parser.add_argument("--trace-output", type=Path, default=None)
    parser.add_argument(
        "--actions-output",
        type=Path,
        default=None,
    )
    args = parser.parse_args()

    proposal = load_proposal(args.sample)
    trace_result = simulate_payload(proposal)
    extraction = extract_risk_actions_with_summary(trace_result)
    risk_actions = extraction["risk_actions"]

    output_id = proposal.metadata.get("benchmark_id") or args.sample.stem
    trace_output = args.trace_output or Path("outputs/traces") / f"{output_id}-trace.json"
    actions_output = args.actions_output or Path("outputs/risk_actions") / f"{output_id}-risk-actions.json"

    trace_output.parent.mkdir(parents=True, exist_ok=True)
    actions_output.parent.mkdir(parents=True, exist_ok=True)
    trace_output.write_text(
        json.dumps(trace_result.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    actions_output.write_text(
        json.dumps(
            {
                "risk_actions": [action.model_dump() for action in risk_actions],
                "filtering_summary": extraction["filtering_summary"],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "proposal_id": proposal.proposal_id,
                "simulation_status": trace_result.simulation_status,
                "trace_source": trace_result.trace_source,
                "call_count": len(trace_result.parsed_trace.calls) if trace_result.parsed_trace else 0,
                "max_depth": trace_result.parsed_trace.max_depth if trace_result.parsed_trace else 0,
                "risk_action_count": len(risk_actions),
                "filtering_summary": extraction["filtering_summary"],
                "trace_output": str(trace_output),
                "actions_output": str(actions_output),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
