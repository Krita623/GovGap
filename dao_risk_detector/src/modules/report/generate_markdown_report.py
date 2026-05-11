from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


_SEVERITY_LABEL = {
    "LOW": "LOW",
    "MEDIUM": "MEDIUM",
    "HIGH": "HIGH",
    "CRITICAL": "CRITICAL",
}

_CONCLUSION_BY_LEVEL = {
    "LOW": (
        "The proposal text and the observed payload effects are broadly consistent. "
        "No clear Semantic Gap was found. Reviewers should still manually review any low-risk "
        "undisclosed addresses or unknown selectors."
    ),
    "MEDIUM": (
        "The proposal has some disclosure gaps or incomplete semantic coverage. Reviewers should "
        "verify the relevant addresses, functions, and call paths before voting or execution."
    ),
    "HIGH": (
        "The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently "
        "covered by the proposal text and may affect governance participants' judgment. "
        "Pausing or escalating to manual audit is recommended."
    ),
    "CRITICAL": (
        "The proposal has a critical Semantic Gap or potential attack indicators. The textual "
        "commitment and observed on-chain behavior are severely inconsistent. Do not execute "
        "without immediate manual security review."
    ),
}


def generate_markdown_report(final_audit: dict[str, Any]) -> str:
    """Render a Markdown report only from final_audit JSON facts."""

    metadata = _dict(final_audit.get("metadata"))
    overall = _dict(final_audit.get("overall"))
    dimensions = _dict(final_audit.get("dimensions"))
    semantics = _dict(final_audit.get("proposal_semantics"))
    trace_summary = _dict(final_audit.get("trace_summary"))
    hallucination_controls = _dict(final_audit.get("hallucination_controls"))
    risk_findings = _list(final_audit.get("risk_findings"))

    conflict = _dict(dimensions.get("conflict_detection"))
    depth = _dict(dimensions.get("depth_analysis"))
    function_match = _dict(dimensions.get("function_semantic_match"))

    lines: list[str] = [
        "# DAO Proposal Semantic Gap Audit Report",
        "",
        f"**Generated At**: {_format_timestamp(metadata.get('generated_at'))}",
        f"**Proposal ID**: {_unknown(metadata.get('proposal_id'))}",
        f"**Simulation Status**: {_unknown(metadata.get('simulation_status'))}",
        f"**Trace Source**: {_unknown(metadata.get('trace_source'))}",
        "",
        "---",
        "",
    ]

    _append_overall(lines, overall, risk_findings)
    _append_conflict(lines, conflict)
    _append_depth(lines, depth, trace_summary)
    _append_function_match(lines, function_match)
    _append_findings(lines, risk_findings)
    _append_conclusion(lines, overall)
    _append_summary(lines, semantics, trace_summary, dimensions, risk_findings)
    _append_machine_verifiable(lines, hallucination_controls)

    return "\n".join(lines).rstrip() + "\n"


def write_markdown_report(final_audit: dict[str, Any], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generate_markdown_report(final_audit), encoding="utf-8")
    return output_path


def generate_report_file(final_audit_path: Path, output_path: Path | None = None) -> Path:
    final_audit = json.loads(final_audit_path.read_text(encoding="utf-8"))
    target = output_path or Path("outputs/reports") / f"{final_audit_path.stem}.md"
    return write_markdown_report(final_audit, target)


def _append_overall(lines: list[str], overall: dict[str, Any], findings: list[Any]) -> None:
    score = overall.get("score", "unknown")
    scale = overall.get("score_scale", 10)
    risk_level = _risk_level(overall)
    high_or_critical = any(_dict(finding).get("severity") in {"HIGH", "CRITICAL"} for finding in findings)

    lines.extend(
        [
            "## Consistency Score",
            "",
            f"**Overall Score**: {_unknown(score)}/{scale}",
            f"**Risk Level**: {_unknown(risk_level)}",
            "**Scoring Method**: worst-case risk gating, not weighted average.",
            "",
            _sentence(overall.get("summary")),
        ]
    )
    if high_or_critical:
        lines.extend(
            [
                "",
                (
                    "Some dimensions may be acceptable, but the overall score is limited by "
                    "High or Critical rule-engine findings."
                ),
            ]
        )
    lines.extend(["", "---", ""])


def _append_conflict(lines: list[str], conflict: dict[str, Any]) -> None:
    lines.extend(
        [
            "## Conflict Detection",
            "",
            f"- Dimension score: {_score(conflict)}",
            f"- Severity: {_unknown(conflict.get('severity'))}",
            f"- Summary: {_sentence(conflict.get('summary'))}",
        ]
    )

    disclosed = _list(conflict.get("disclosed_addresses"))
    system_addresses = _list(conflict.get("system_addresses"))
    unaccounted = _list(conflict.get("unaccounted_addresses"))

    if disclosed:
        lines.extend(["", "### Addresses Disclosed In Proposal Text"])
        lines.extend(f"- `{address}`" for address in disclosed)

    if system_addresses:
        lines.extend(["", "### System-Level Calls"])
        for address in system_addresses:
            lines.extend(
                [
                    f"- `{address}`",
                    "  - Type: precompile",
                    "  - Note: system whitelist address; usually does not need explicit proposal disclosure.",
                ]
            )

    if unaccounted:
        lines.extend(["", "### Unaccounted Addresses"])
        severity = _unknown(conflict.get("severity"))
        related_actions = _related_actions(conflict)
        for address in unaccounted:
            action_names = _actions_for_address(address, related_actions)
            lines.extend(
                [
                    f"- `{address}`",
                    f"  - Risk level: {severity}",
                    f"  - Related actions: {_join_or_unknown(action_names)}",
                    "  - Evidence source: trace",
                    (
                        "  - Note: this address was not explicitly disclosed in the proposal text. "
                        "If the system cannot verify its role, manual review is required."
                    ),
                ]
            )

    _append_dimension_findings(lines, conflict)
    lines.extend(["", "---", ""])


def _append_depth(lines: list[str], depth: dict[str, Any], trace_summary: dict[str, Any]) -> None:
    claimed = _unknown(depth.get("claimed_complexity"))
    actual_depth = _unknown(depth.get("actual_max_depth"))
    delegatecall_count = _unknown(trace_summary.get("delegatecall_count", _evidence_value(depth, "delegatecall_count")))
    multicall_count = _count_action(trace_summary, "multicall")

    lines.extend(
        [
            "## Depth Analysis",
            "",
            f"- Claimed complexity: {claimed}",
            f"- Actual max depth: {actual_depth}",
            f"- Depth mismatch: {_yes_no(depth.get('depth_mismatch'))}",
            f"- Delegatecall count: {delegatecall_count}",
        ]
    )
    if multicall_count is not None:
        lines.append(f"- Multicall count: {multicall_count}")

    if claimed == "unknown":
        lines.extend(
            [
                "",
                (
                    "The proposal text does not explicitly claim execution complexity. This section "
                    "therefore evaluates actual call depth and high-risk call patterns."
                ),
            ]
        )
    if _as_int(depth.get("actual_max_depth")) > 8:
        lines.extend(["", "The actual call chain is deep and may increase review difficulty."])

    lines.extend(["", f"Summary: {_sentence(depth.get('summary'))}"])
    _append_dimension_findings(lines, depth)
    lines.extend(["", "---", ""])


def _append_function_match(lines: list[str], function_match: dict[str, Any]) -> None:
    claimed_actions = _list(function_match.get("claimed_actions"))
    actual_actions = _list(function_match.get("actual_actions"))
    matched_functions = _list(function_match.get("matched_functions"))
    unmatched_functions = _list(function_match.get("unmatched_functions"))
    unknown_selectors = _list(function_match.get("unknown_selectors"))

    lines.extend(
        [
            "## Function Semantic Match",
            "",
            f"- Dimension score: {_score(function_match)}",
            f"- Severity: {_unknown(function_match.get('severity'))}",
            f"- Summary: {_sentence(function_match.get('summary'))}",
            f"- Claimed actions: {_join_or_unknown(claimed_actions)}",
            f"- Actual actions: {_join_or_unknown(actual_actions)}",
        ]
    )

    if matched_functions:
        lines.extend(["", "### Matched Functions"])
        lines.extend(f"- `{function}`" for function in matched_functions)

    if unmatched_functions:
        lines.extend(["", "### Unmatched Or Additional Actions"])
        for function in unmatched_functions:
            lines.extend(
                [
                    f"- `{function}`",
                    f"  - Risk level: {_unknown(function_match.get('severity'))}",
                    (
                        "  - Note: this action was not fully matched to the claimed proposal action. "
                        "Review the linked evidence before relying on the proposal text."
                    ),
                ]
            )

    if unknown_selectors:
        lines.extend(["", "### Unknown Selectors Requiring Review"])
        lines.extend(
            f"- `{selector}`: unable to confirm function semantics; manual review is required."
            for selector in unknown_selectors
        )

    _append_dimension_findings(lines, function_match)
    lines.extend(["", "---", ""])


def _append_findings(lines: list[str], findings: list[Any]) -> None:
    lines.append("## Potential Risk Findings")
    if not findings:
        lines.extend(["", "No rule-engine risk findings were generated.", "", "---", ""])
        return

    for index, raw_finding in enumerate(findings, start=1):
        finding = _dict(raw_finding)
        severity = _unknown(finding.get("severity"))
        lines.extend(
            [
                "",
                f"### {index}. {_SEVERITY_LABEL.get(str(severity), 'INFO')} - {_unknown(finding.get('title'))}",
                "",
                f"- **Severity**: {severity}",
                f"- **Description**: {_sentence(finding.get('description'))}",
                f"- **Evidence Source**: {_unknown(finding.get('evidence_type'))}",
                f"- **Confidence**: {_unknown(finding.get('confidence'))}",
                f"- **Recommendation**: {_sentence(finding.get('recommendation'))}",
            ]
        )
        evidence_lines = _format_evidence(finding.get("evidence"))
        if evidence_lines:
            lines.extend(["- **Key Evidence**:"])
            lines.extend(f"  - {item}" for item in evidence_lines)

    lines.extend(["", "---", ""])


def _append_conclusion(lines: list[str], overall: dict[str, Any]) -> None:
    risk_level = _risk_level(overall)
    conclusion = _CONCLUSION_BY_LEVEL.get(
        risk_level,
        "Unable to confirm the overall risk level. Manual review of final_audit.json evidence is required.",
    )
    lines.extend(["## Security Conclusion", "", conclusion, "", "---", ""])


def _append_summary(
    lines: list[str],
    semantics: dict[str, Any],
    trace_summary: dict[str, Any],
    dimensions: dict[str, Any],
    findings: list[Any],
) -> None:
    proposal_summary = _sentence(semantics.get("proposal_summary"))
    actual_actions = _join_or_unknown(_list(_dict(dimensions.get("function_semantic_match")).get("actual_actions")))
    decoded_functions = _join_or_unknown(_list(trace_summary.get("decoded_functions")))
    lowest_dimension = _lowest_dimension(dimensions)
    severe_findings = [
        _dict(finding).get("title")
        for finding in findings
        if _dict(finding).get("severity") in {"HIGH", "CRITICAL"}
    ]

    lines.extend(["## Summary", ""])
    lines.append(f"The proposal text claims: {proposal_summary}")
    lines.append(f"The payload actually shows: {actual_actions}. Decoded functions include: {decoded_functions}.")
    if lowest_dimension:
        lines.append(
            f"The most important scoring issue is `{lowest_dimension[0]}`, which scored {lowest_dimension[1]}/10."
        )
    if severe_findings:
        lines.append(
            f"High-risk findings include: {_join_or_unknown(severe_findings)}. Pausing or escalating to manual audit is recommended."
        )
    else:
        lines.append("No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.")
    lines.extend(["", "---", ""])


def _append_machine_verifiable(lines: list[str], controls: dict[str, Any]) -> None:
    lines.extend(
        [
            "## Machine-Verifiable Controls",
            "",
            f"- LLM used for scoring: {_bool_text(controls.get('llm_used_for_scoring'))}",
            f"- LLM used for trace analysis: {_bool_text(controls.get('llm_used_for_trace_analysis'))}",
            f"- Unsupported claims allowed: {_bool_text(controls.get('unsupported_claims_allowed'))}",
            f"- Unknown fields preserved as unknown: {_bool_text(controls.get('unknown_fields_preserved_as_unknown'))}",
            "",
            (
                "This report is generated from structured rule-engine output and a deterministic template. "
                "The LLM is only used for proposal-text semantic extraction and is not used for scoring, "
                "trace analysis, or final conclusions."
            ),
        ]
    )


def _append_dimension_findings(lines: list[str], dimension: dict[str, Any]) -> None:
    findings = _list(dimension.get("findings"))
    if not findings:
        return
    lines.extend(["", "### Key Findings"])
    for finding in findings:
        item = _dict(finding)
        lines.extend(
            [
                f"- {_unknown(item.get('title'))}",
                f"  - Risk level: {_unknown(item.get('severity'))}",
                f"  - Description: {_sentence(item.get('description'))}",
                f"  - Evidence source: {_unknown(item.get('evidence_type'))}",
            ]
        )


def _format_evidence(evidence: Any) -> list[str]:
    items: list[str] = []
    for entry in _list(evidence)[:5]:
        item = _dict(entry)
        if not item:
            continue
        if "unaccounted_addresses" in item:
            items.append(f"Unaccounted addresses: {_join_or_unknown(_list(item.get('unaccounted_addresses')))}")
        if "claimed_complexity" in item or "actual_max_depth" in item:
            items.append(
                f"Complexity: claimed={_unknown(item.get('claimed_complexity'))}, "
                f"actual_max_depth={_unknown(item.get('actual_max_depth'))}"
            )
        if "claimed_actions" in item or "actual_actions" in item:
            items.append(
                f"Action comparison: claimed={_join_or_unknown(_list(item.get('claimed_actions')))}, "
                f"actual={_join_or_unknown(_list(item.get('actual_actions')))}"
            )
        if "unknown_selectors" in item and _list(item.get("unknown_selectors")):
            items.append(f"Unknown selectors: {_join_or_unknown(_list(item.get('unknown_selectors')))}")
    return items[:6]


def _related_actions(conflict: dict[str, Any]) -> list[dict[str, Any]]:
    for finding in _list(conflict.get("findings")):
        for evidence in _list(_dict(finding).get("evidence")):
            actions = _list(_dict(evidence).get("related_actions"))
            if actions:
                return [_dict(action) for action in actions]
    return []


def _actions_for_address(address: str, actions: list[dict[str, Any]]) -> list[str]:
    matched = []
    address_lower = address.lower()
    for action in actions:
        if str(action.get("from_address", "")).lower() == address_lower or str(action.get("to_address", "")).lower() == address_lower:
            matched.append(str(action.get("decoded_function") or action.get("action_type") or "unknown"))
    return sorted(set(matched))


def _lowest_dimension(dimensions: dict[str, Any]) -> tuple[str, int] | None:
    scored = []
    for name, value in dimensions.items():
        score = _as_int(_dict(value).get("score"), default=-1)
        if score >= 0:
            scored.append((name, score))
    return min(scored, key=lambda item: item[1]) if scored else None


def _count_action(trace_summary: dict[str, Any], action_name: str) -> int | None:
    functions = [str(function).lower() for function in _list(trace_summary.get("decoded_functions"))]
    count = sum(1 for function in functions if function.split("(", 1)[0] == action_name)
    return count if count else None


def _evidence_value(dimension: dict[str, Any], key: str) -> Any:
    for entry in _list(dimension.get("evidence")):
        item = _dict(entry)
        if key in item:
            return item[key]
    return None


def _risk_level(overall: dict[str, Any]) -> str:
    level = overall.get("risk_level")
    if level:
        return str(level)
    score = _as_int(overall.get("score"), default=-1)
    if score >= 8:
        return "LOW"
    if score >= 6:
        return "MEDIUM"
    if score >= 3:
        return "HIGH"
    if score >= 0:
        return "CRITICAL"
    return "unknown"


def _score(item: dict[str, Any]) -> str:
    score = item.get("score", "unknown")
    return f"{score}/10" if score != "unknown" else "unknown"


def _sentence(value: Any) -> str:
    text = str(value).strip() if value not in (None, "") else ""
    return text if text and text.lower() != "unknown" else "Unable to confirm."


def _unknown(value: Any) -> str:
    if value is None or value == "":
        return "unknown"
    if isinstance(value, str) and value.lower() == "unknown":
        return "unable to confirm"
    return str(value)


def _yes_no(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return "unable to confirm"


def _bool_text(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    return "unknown"


def _format_timestamp(value: Any) -> str:
    if value in (None, ""):
        return "unknown"
    if not isinstance(value, str):
        return str(value)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return _unknown(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")


def _join_or_unknown(values: list[Any]) -> str:
    cleaned = [str(value) for value in values if value not in (None, "")]
    return ", ".join(cleaned) if cleaned else "unable to confirm"


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
