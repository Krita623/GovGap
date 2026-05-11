from __future__ import annotations

from src.models.semantics import ClaimedAction, ProposalSemantics


_ACTION_RULES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("adjust parameter", "change reserve factor", "set parameter"), "parameter_update"),
    (("upgrade implementation", "update logic", "arbos upgrade"), "upgrade"),
    (("send funds", "transfer tokens", "move assets"), "transfer"),
    (("approve spending", "allowance"), "approval"),
    (("deploy contract", "create contract", "contract creation"), "contract_creation"),
    (("grant role", "set operator", "change admin", "owner"), "role_change"),
    (("create proposal", "on-chain vote", "governor propose"), "governance_proposal_creation"),
    (("bridge", "relay", "cross-chain message"), "bridge"),
)


def normalize_semantics(semantics: ProposalSemantics) -> ProposalSemantics:
    """Deterministically normalize LLM-extracted semantics.

    This function does not call LLMs and does not inspect trace data.
    """

    normalized_actions = [
        action.model_copy(update={"canonical_action": _normalize_action(action)})
        for action in semantics.claimed_actions
    ]
    return semantics.model_copy(update={"claimed_actions": normalized_actions})


def _normalize_action(action: ClaimedAction) -> str:
    if action.canonical_action != "unknown":
        canonical_from_text = _canonical_from_text(action)
        return canonical_from_text or action.canonical_action
    return _canonical_from_text(action) or "unknown"


def _canonical_from_text(action: ClaimedAction) -> str | None:
    text = " ".join(
        part
        for part in (action.raw_action, action.object or "", action.claimed_effect, action.textual_evidence)
        if part
    ).lower()

    for keywords, canonical in _ACTION_RULES:
        if any(keyword in text for keyword in keywords):
            return canonical

    if "maintenance" in text or "routine" in text:
        return "maintenance"
    if "treasury" in text:
        return "treasury_operation"
    return None
