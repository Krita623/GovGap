"""Proposal sampling rules.

This module applies deterministic two-dimensional stratified sampling over the
in-memory proposal index built from Tally proposal lists.
"""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import asdict, dataclass

from .proposals import ProposalIndexEntry
from .registry import DaoConfig


RANDOM_SEED = 20260429

EXECUTED_LIKE_STATUSES = {
    "executed",
    "queued",
    "succeeded",
    "callexecuted",
    "crosschainexecuted",
    "pendingexecution",
}
NON_EXECUTED_LIKE_STATUSES = {
    "defeated",
    "canceled",
    "expired",
    "vetoed",
    "archived",
}

TIME_BUCKETS = ("early", "middle", "recent")
STATUS_BUCKETS = ("executed_like", "non_executed_like")
QUOTA = {
    "early": {
        "executed_like": 4,
        "non_executed_like": 2,
    },
    "middle": {
        "executed_like": 5,
        "non_executed_like": 1,
    },
    "recent": {
        "executed_like": 6,
        "non_executed_like": 2,
    },
}


@dataclass(frozen=True)
class SampleSelection:
    """A selected proposal and its assigned benchmark identifier."""

    benchmark_id: str
    dao_id: str
    proposal_id: str
    proposal_tally_id: str
    governor_id: str
    time_bucket: str
    status_bucket: str
    status: str
    created_block: int


@dataclass(frozen=True)
class BucketedProposal:
    """Proposal index entry with sampling bucket metadata."""

    entry: ProposalIndexEntry
    time_bucket: str
    status_bucket: str


def sample_dao_proposals(
    dao: DaoConfig,
    proposal_index: list[ProposalIndexEntry],
    rng: random.Random,
) -> tuple[list[SampleSelection], dict]:
    """Sample one DAO and return selections plus a JSON-serializable report."""
    bucketed, excluded_status_counts, missing_created_block = bucket_eligible_proposals(
        proposal_index
    )
    selected: list[BucketedProposal] = []
    selected_keys: set[str] = set()
    fallback_events: list[dict] = []

    buckets = _group_bucketed_proposals(bucketed)

    for time_bucket in TIME_BUCKETS:
        for status_bucket in STATUS_BUCKETS:
            needed = QUOTA[time_bucket][status_bucket]
            before = len(selected)

            selected.extend(
                _take_random(
                    buckets[(time_bucket, status_bucket)],
                    needed,
                    selected_keys,
                    rng,
                )
            )

            remaining = needed - (len(selected) - before)
            if remaining > 0:
                fallback_events.append(
                    _fallback_event(
                        time_bucket,
                        status_bucket,
                        "same_time_other_status",
                        remaining,
                    )
                )
                other_status = _other_status_bucket(status_bucket)
                selected.extend(
                    _take_random(
                        buckets[(time_bucket, other_status)],
                        remaining,
                        selected_keys,
                        rng,
                    )
                )

            remaining = needed - (len(selected) - before)
            if remaining > 0:
                fallback_events.append(
                    _fallback_event(
                        time_bucket,
                        status_bucket,
                        "same_status_other_time",
                        remaining,
                    )
                )
                same_status_other_time = [
                    proposal
                    for proposal in bucketed
                    if proposal.status_bucket == status_bucket
                    and proposal.time_bucket != time_bucket
                ]
                selected.extend(
                    _take_random(
                        same_status_other_time,
                        remaining,
                        selected_keys,
                        rng,
                    )
                )

            remaining = needed - (len(selected) - before)
            if remaining > 0:
                fallback_events.append(
                    _fallback_event(
                        time_bucket,
                        status_bucket,
                        "remaining_eligible",
                        remaining,
                    )
                )
                selected.extend(_take_random(bucketed, remaining, selected_keys, rng))

            shortfall = needed - (len(selected) - before)
            if shortfall > 0:
                fallback_events.append(
                    _fallback_event(
                        time_bucket,
                        status_bucket,
                        "shortfall",
                        shortfall,
                    )
                )

    selections = [
        SampleSelection(
            benchmark_id=build_benchmark_id(dao.dao_id, index),
            dao_id=dao.dao_id,
            proposal_id=proposal.entry.proposal_id,
            proposal_tally_id=proposal.entry.proposal_tally_id,
            governor_id=proposal.entry.governor_id,
            time_bucket=proposal.time_bucket,
            status_bucket=proposal.status_bucket,
            status=proposal.entry.status,
            created_block=proposal.entry.created_block or 0,
        )
        for index, proposal in enumerate(selected, start=1)
    ]
    report = build_sampling_report(
        proposal_index=proposal_index,
        bucketed=bucketed,
        selections=selections,
        excluded_status_counts=excluded_status_counts,
        missing_created_block=missing_created_block,
        fallback_events=fallback_events,
    )
    return selections, report


def bucket_eligible_proposals(
    proposal_index: list[ProposalIndexEntry],
) -> tuple[list[BucketedProposal], dict[str, int], int]:
    """Assign time and status buckets to eligible proposals."""
    excluded_status_counts: Counter[str] = Counter()
    missing_created_block = 0
    eligible_entries: list[ProposalIndexEntry] = []

    for entry in proposal_index:
        if entry.created_block is None:
            missing_created_block += 1
            continue
        if status_bucket_for(entry.status) is None:
            excluded_status_counts[entry.status or "<missing>"] += 1
            continue
        eligible_entries.append(entry)

    eligible_entries.sort(
        key=lambda entry: (
            entry.created_block if entry.created_block is not None else -1,
            entry.proposal_tally_id,
        )
    )

    bucketed: list[BucketedProposal] = []
    total = len(eligible_entries)
    for index, entry in enumerate(eligible_entries):
        time_bucket = time_bucket_for_index(index, total)
        status_bucket = status_bucket_for(entry.status)
        if status_bucket is None:
            continue
        bucketed.append(
            BucketedProposal(
                entry=entry,
                time_bucket=time_bucket,
                status_bucket=status_bucket,
            )
        )

    return bucketed, dict(excluded_status_counts), missing_created_block


def status_bucket_for(status: str) -> str | None:
    """Map a proposal status to a sampling status bucket."""
    normalized = status.lower()
    if normalized in EXECUTED_LIKE_STATUSES:
        return "executed_like"
    if normalized in NON_EXECUTED_LIKE_STATUSES:
        return "non_executed_like"
    return None


def time_bucket_for_index(index: int, total: int) -> str:
    """Assign sorted proposals to early, middle, or recent count terciles."""
    if total <= 0:
        raise ValueError("Cannot assign a time bucket without proposals.")
    first_cut = total // 3
    second_cut = (total * 2) // 3
    if index < first_cut:
        return "early"
    if index < second_cut:
        return "middle"
    return "recent"


def build_benchmark_id(dao_id: str, index: int) -> str:
    """Build IDs such as real-uniswap-0007."""
    return f"real-{dao_id}-{index:04d}"


def quota_as_dict() -> dict:
    """Return the fixed sampling quota."""
    return {
        time_bucket: dict(status_quotas)
        for time_bucket, status_quotas in QUOTA.items()
    }


def selection_to_dict(selection: SampleSelection) -> dict:
    """Convert a sample selection to a JSON-serializable dictionary."""
    return asdict(selection)


def _group_bucketed_proposals(
    bucketed: list[BucketedProposal],
) -> dict[tuple[str, str], list[BucketedProposal]]:
    """Group eligible proposals by time and status bucket."""
    grouped: dict[tuple[str, str], list[BucketedProposal]] = {}
    for time_bucket in TIME_BUCKETS:
        for status_bucket in STATUS_BUCKETS:
            grouped[(time_bucket, status_bucket)] = []
    for proposal in bucketed:
        grouped[(proposal.time_bucket, proposal.status_bucket)].append(proposal)
    return grouped


def _take_random(
    candidates: list[BucketedProposal],
    count: int,
    selected_keys: set[str],
    rng: random.Random,
) -> list[BucketedProposal]:
    """Take up to count unselected proposals from candidates."""
    available = [
        proposal
        for proposal in candidates
        if proposal.entry.proposal_tally_id not in selected_keys
    ]
    if not available or count <= 0:
        return []
    taken = rng.sample(available, k=min(count, len(available)))
    for proposal in taken:
        selected_keys.add(proposal.entry.proposal_tally_id)
    return taken


def _other_status_bucket(status_bucket: str) -> str:
    """Return the other status bucket."""
    if status_bucket == "executed_like":
        return "non_executed_like"
    return "executed_like"


def _fallback_event(
    time_bucket: str,
    status_bucket: str,
    strategy: str,
    needed_before_strategy: int,
) -> dict:
    """Build a fallback event report record."""
    return {
        "time_bucket": time_bucket,
        "status_bucket": status_bucket,
        "strategy": strategy,
        "needed_before_strategy": needed_before_strategy,
    }


def build_sampling_report(
    proposal_index: list[ProposalIndexEntry],
    bucketed: list[BucketedProposal],
    selections: list[SampleSelection],
    excluded_status_counts: dict[str, int],
    missing_created_block: int,
    fallback_events: list[dict],
) -> dict:
    """Build a per-DAO sampling report."""
    actual_distribution: dict[str, dict[str, int]] = {
        time_bucket: {status_bucket: 0 for status_bucket in STATUS_BUCKETS}
        for time_bucket in TIME_BUCKETS
    }
    for selection in selections:
        actual_distribution[selection.time_bucket][selection.status_bucket] += 1

    return {
        "indexed_total": len(proposal_index),
        "eligible_total": len(bucketed),
        "sampled_total": len(selections),
        "actual_distribution": actual_distribution,
        "fallback_events": fallback_events,
        "shortfall": max(0, 20 - len(selections)),
        "excluded_status_counts": excluded_status_counts,
        "missing_created_block": missing_created_block,
    }
