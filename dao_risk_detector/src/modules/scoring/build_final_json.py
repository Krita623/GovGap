from __future__ import annotations

from datetime import UTC, datetime

from src.models.proposal import Proposal
from src.models.risk_action import RiskAction
from src.models.scoring import FinalAuditJSON, FinalMetadata
from src.models.semantics import ProposalSemantics
from src.models.trace import TraceResult
from src.modules.scoring.calculate_overall_score import calculate_overall_score
from src.modules.scoring.score_conflict_detection import score_conflict_detection
from src.modules.scoring.score_depth_analysis import score_depth_analysis
from src.modules.scoring.score_function_semantic_match import score_function_semantic_match


def build_final_json(
    proposal: Proposal,
    trace: TraceResult,
    risk_actions: list[RiskAction],
    proposal_semantics: ProposalSemantics,
) -> FinalAuditJSON:
    """Build final structured JSON from validated artifacts.

    This function does not call LLMs.
    """

    conflict = score_conflict_detection(proposal_semantics, trace, risk_actions)
    depth = score_depth_analysis(proposal_semantics, trace, risk_actions)
    semantic = score_function_semantic_match(proposal_semantics, trace, risk_actions)
    findings = [*conflict.findings, *depth.findings, *semantic.findings]
    overall = calculate_overall_score(conflict, depth, semantic, findings)

    return FinalAuditJSON(
        metadata=FinalMetadata(
            proposal_id=proposal.proposal_id,
            generated_at=datetime.now(UTC).isoformat(),
            chain_id=proposal.chain_id,
            simulation_status=trace.simulation_status.value,
            trace_source=trace.trace_source,
        ),
        overall=overall,
        proposal_semantics=proposal_semantics.model_dump(),
        trace_summary=trace.parsed_trace.model_dump() if trace.parsed_trace else {},
        risk_actions=[action.model_dump() for action in risk_actions],
        dimensions={
            "conflict_detection": conflict.model_dump(),
            "depth_analysis": depth.model_dump(),
            "function_semantic_match": semantic.model_dump(),
        },
        risk_findings=findings,
    )
