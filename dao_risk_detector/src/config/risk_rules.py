"""Shared deterministic risk rule constants.

LLM output must not be used to decide trace facts, severity caps, or numeric
scores. These caps encode the conservative triage policy used by rule-based
scoring and reporting.
"""

SEVERITY_SCORE_CAPS: dict[str, int] = {
    "critical": 2,
    "high": 4,
    "medium": 7,
    "low": 9,
    "none": 10,
}
