"""Command-line entrypoint for the DAO benchmark collector.

The current CLI supports lightweight governor discovery. Full collection,
sampling, hydration, and reporting will be implemented in later iterations.
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv

from .abi_preparer import prepare_abis
from .decoder import decode_raw_sample_file, decoded_file_path
from .governors import GovernorInfo, fetch_governors, select_primary_governor
from .hydration import build_manifest_record, hydrate_sample, write_raw_sample
from .proposals import ProposalIndexEntry, build_proposal_index, fetch_proposals
from .registry import DaoConfig, load_registry
from .sampling import (
    RANDOM_SEED,
    quota_as_dict,
    sample_dao_proposals,
    selection_to_dict,
)
from .tally_client import TallyClient, TallyClientError
from .utils import append_jsonl, ensure_output_dirs, write_json


DEFAULT_REGISTRY_PATH = Path("config/dao_registry.json")
DEFAULT_OUTPUT_DIR = Path("outputs")


def build_parser() -> argparse.ArgumentParser:
    """Build the collector CLI parser."""
    parser = argparse.ArgumentParser(
        description="Collect raw DAO governance proposal benchmark samples from Tally."
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY_PATH,
        help="Path to DAO registry JSON.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for raw samples, manifest, report, and logs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate planned collection without writing raw sample files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "fetch-governors",
        help="Fetch and print governor metadata for all DAOs in the registry.",
    )
    subparsers.add_parser(
        "inspect-proposals",
        help="Fetch all proposals for each DAO and print proposal statistics.",
    )
    subparsers.add_parser(
        "sample-proposals",
        help="Fetch proposal indexes, sample proposals, and write sampling report.",
    )
    subparsers.add_parser(
        "collect",
        help="Collect final sampled raw proposal JSON files and indexes.",
    )
    subparsers.add_parser(
        "decode-samples",
        help="Decode existing raw sample payload calldata into decoded samples.",
    )
    subparsers.add_parser(
        "prepare-abis",
        help="Fetch missing local ABI files for raw sample target contracts.",
    )
    subparsers.add_parser(
        "decode",
        help="Run prepare-abis followed by offline decode-samples.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    """Run the collector workflow."""
    if args.command == "fetch-governors":
        return run_fetch_governors(args)
    if args.command == "inspect-proposals":
        return run_inspect_proposals(args)
    if args.command == "sample-proposals":
        return run_sample_proposals(args)
    if args.command == "collect":
        return run_collect(args)
    if args.command == "decode-samples":
        return run_decode_samples(args)
    if args.command == "prepare-abis":
        return run_prepare_abis(args)
    if args.command == "decode":
        prepare_code = run_prepare_abis(args)
        if prepare_code != 0:
            return prepare_code
        return run_decode_samples(args)
    raise ValueError(f"Unknown command: {args.command}")


def run_fetch_governors(args: argparse.Namespace) -> int:
    """Fetch governor metadata for each DAO and print it to the terminal."""
    daos = load_registry(args.registry)
    client = TallyClient.from_env()

    for dao in daos:
        print_governor_info(client, dao)
        time.sleep(client.sleep_seconds)
    return 0


def run_inspect_proposals(args: argparse.Namespace) -> int:
    """Fetch all proposal lists and print per-DAO statistics."""
    daos = load_registry(args.registry)
    client = TallyClient.from_env()

    for dao in daos:
        inspect_dao_proposals(client, dao)
        time.sleep(client.sleep_seconds)
    return 0


def run_sample_proposals(args: argparse.Namespace) -> int:
    """Fetch proposal indexes, sample proposals, and write sampling report."""
    daos = load_registry(args.registry)
    client = TallyClient.from_env()
    rng = random.Random(RANDOM_SEED)
    ensure_output_dirs(args.output_dir)

    report = {
        "random_seed": RANDOM_SEED,
        "quota": quota_as_dict(),
        "daos": {},
    }

    for dao in daos:
        try:
            proposal_index = fetch_dao_proposal_index(client, dao)
            selections, dao_report = sample_dao_proposals(dao, proposal_index, rng)
        except (TallyClientError, ValueError) as exc:
            report["daos"][dao.dao_id] = {
                "indexed_total": 0,
                "eligible_total": 0,
                "sampled_total": 0,
                "actual_distribution": {},
                "fallback_events": [],
                "shortfall": 20,
                "excluded_status_counts": {},
                "missing_created_block": 0,
                "error": str(exc),
            }
            print(f"dao_id: {dao.dao_id}")
            print(f"error: {exc}")
            print()
            continue

        report["daos"][dao.dao_id] = dao_report
        print_sampled_proposals(dao, selections)
        time.sleep(client.sleep_seconds)

    report_path = args.output_dir / "sampling_report.json"
    write_json(report_path, report)
    print(f"wrote_sampling_report: {report_path}")
    return 0


def run_collect(args: argparse.Namespace) -> int:
    """Run full raw sample collection."""
    daos = load_registry(args.registry)
    client = TallyClient.from_env()
    rng = random.Random(RANDOM_SEED)
    ensure_output_dirs(args.output_dir)

    manifest_path = args.output_dir / "manifest.jsonl"
    log_path = args.output_dir / "collection_log.jsonl"
    sampling_report_path = args.output_dir / "sampling_report.json"
    _reset_jsonl(manifest_path)
    _reset_jsonl(log_path)

    sampling_report = {
        "random_seed": RANDOM_SEED,
        "quota": quota_as_dict(),
        "daos": {},
    }

    written_count = 0
    for dao in daos:
        print(f"collecting_dao: {dao.dao_id}")
        try:
            proposal_index = fetch_dao_proposal_index(client, dao)
            selections, dao_report = sample_dao_proposals(dao, proposal_index, rng)
        except (TallyClientError, ValueError) as exc:
            sampling_report["daos"][dao.dao_id] = _empty_sampling_error(str(exc))
            append_jsonl(
                log_path,
                {
                    "level": "error",
                    "type": "dao_collection_failed",
                    "dao_id": dao.dao_id,
                    "message": str(exc),
                },
            )
            print(f"error: {exc}")
            print()
            continue

        sampling_report["daos"][dao.dao_id] = dao_report
        entry_by_tally_id = {
            entry.proposal_tally_id: entry for entry in proposal_index
        }

        for selection in selections:
            entry = entry_by_tally_id.get(selection.proposal_tally_id)
            if not entry:
                append_jsonl(
                    log_path,
                    {
                        "level": "error",
                        "type": "sample_entry_missing",
                        "benchmark_id": selection.benchmark_id,
                        "dao_id": dao.dao_id,
                        "proposal_id": selection.proposal_id,
                        "message": "Sampled proposal was not found in proposal index.",
                    },
                )
                continue

            governor = _governor_from_index_entry(entry)
            try:
                sample, warnings = hydrate_sample(client, dao, governor, selection)
                file_path = write_raw_sample(sample, args.output_dir / "raw_samples")
                append_jsonl(
                    manifest_path,
                    build_manifest_record(sample, dao, selection, file_path),
                )
                for warning in warnings:
                    append_jsonl(log_path, warning)
                written_count += 1
            except (TallyClientError, ValueError, TypeError) as exc:
                append_jsonl(
                    log_path,
                    {
                        "level": "error",
                        "type": "sample_hydration_failed",
                        "benchmark_id": selection.benchmark_id,
                        "dao_id": dao.dao_id,
                        "proposal_id": selection.proposal_id,
                        "message": str(exc),
                    },
                )
                print(
                    "hydrate_error: "
                    f"{selection.benchmark_id} proposal_id={selection.proposal_id} {exc}"
                )

        print(f"sampled_total: {len(selections)}")
        print()
        time.sleep(client.sleep_seconds)

    write_json(sampling_report_path, sampling_report)
    print(f"wrote_raw_samples: {written_count}")
    print(f"wrote_manifest: {manifest_path}")
    print(f"wrote_sampling_report: {sampling_report_path}")
    print(f"wrote_collection_log: {log_path}")
    return 0


def run_decode_samples(args: argparse.Namespace) -> int:
    """Decode existing raw sample files without recollecting raw data."""
    raw_dir = args.output_dir / "raw_samples"
    decoded_dir = args.output_dir / "decoded_samples"
    manifest_path = args.output_dir / "decoded_manifest.jsonl"
    report_path = args.output_dir / "decode_report.json"
    log_path = args.output_dir / "decode_log.jsonl"
    project_root = Path.cwd()

    decoded_dir.mkdir(parents=True, exist_ok=True)
    _reset_jsonl(manifest_path)
    _reset_jsonl(log_path)

    raw_files = sorted(raw_dir.glob("*.json"))
    report = {
        "total_samples": len(raw_files),
        "total_calls": 0,
        "decode_status_counts": {},
    }
    decoded_samples = 0
    failed_samples = 0

    for raw_file in raw_files:
        try:
            result = decode_raw_sample_file(raw_file, project_root)
            decoded_file = decoded_file_path(raw_file, args.output_dir)
            write_json(decoded_file, result.sample)

            sample_report = result.report
            decoded_samples += 1
            report["total_calls"] += sample_report["total_calls"]
            _merge_counts(report["decode_status_counts"], sample_report["status_counts"])

            raw_relative = _relative_posix(raw_file, project_root)
            decoded_relative = _relative_posix(decoded_file, project_root)
            append_jsonl(
                manifest_path,
                {
                    "benchmark_id": result.sample["benchmark_id"],
                    "raw_file": raw_relative,
                    "decoded_file": decoded_relative,
                    "total_calls": sample_report["total_calls"],
                    "decoded_ok": sample_report["decoded_ok"],
                    "decoded_failed": sample_report["decoded_failed"],
                },
            )
            for call_error in sample_report["call_errors"]:
                append_jsonl(
                    log_path,
                    {
                        "benchmark_id": result.sample["benchmark_id"],
                        "raw_file": raw_relative,
                        **call_error,
                    },
                )
            if sample_report["payload_length_mismatch"]:
                append_jsonl(
                    log_path,
                    {
                        "benchmark_id": result.sample["benchmark_id"],
                        "raw_file": raw_relative,
                        "decode_status": "failed: payload_length_mismatch",
                        "payload_lengths": sample_report["payload_lengths"],
                    },
                )
        except Exception as exc:
            failed_samples += 1
            append_jsonl(
                log_path,
                {
                    "raw_file": _relative_posix(raw_file, project_root),
                    "decode_status": "failed: sample_error",
                    "error": str(exc),
                },
            )
            print(f"decode_error: {raw_file.name} {exc}")

    write_json(report_path, report)
    print(f"decoded_samples: {decoded_samples}")
    print(f"failed_samples: {failed_samples}")
    print(f"total_calls: {report['total_calls']}")
    print(f"decoded_ok: {report['decode_status_counts'].get('ok', 0)}")
    print(f"decoded_failed: {report['total_calls'] - report['decode_status_counts'].get('ok', 0)}")
    print(f"wrote_decoded_samples: {decoded_dir}")
    print(f"wrote_decoded_manifest: {manifest_path}")
    print(f"wrote_decode_report: {report_path}")
    print(f"wrote_decode_log: {log_path}")
    return 0


def run_prepare_abis(args: argparse.Namespace) -> int:
    """Prepare local ABI files from existing raw sample target contracts."""
    project_root = Path.cwd()
    raw_dir = args.output_dir / "raw_samples"
    load_dotenv(project_root / ".env")
    report = prepare_abis(
        raw_samples_dir=raw_dir,
        project_root=project_root,
        output_dir=args.output_dir,
    )
    print(f"unique_targets: {report['unique_targets']}")
    print(f"targets_with_abi: {report['targets_with_abi']}")
    print(f"targets_without_abi: {report['targets_without_abi']}")
    print("status_counts:")
    for status, count in sorted(report["status_counts"].items()):
        print(f"  {status}: {count}")
    print(f"wrote_abi_targets: {args.output_dir / 'abi_targets.jsonl'}")
    print(f"wrote_abi_report: {args.output_dir / 'abi_report.json'}")
    print(f"wrote_abi_log: {args.output_dir / 'abi_log.jsonl'}")
    return 0


def fetch_dao_proposal_index(
    client: TallyClient,
    dao: DaoConfig,
) -> list[ProposalIndexEntry]:
    """Fetch the in-memory proposal index for one DAO."""
    governors = fetch_governors(client, dao)
    selected_governors = select_proposal_governors(governors, dao.expected_chain_id)
    proposal_index: list[ProposalIndexEntry] = []
    for governor in selected_governors:
        proposals = fetch_proposals(client, governor)
        proposal_index.extend(build_proposal_index(dao, governor, proposals))
    return proposal_index


def _governor_from_index_entry(entry: ProposalIndexEntry) -> GovernorInfo:
    """Build governor metadata from a proposal index entry."""
    return GovernorInfo(
        governor_id=entry.governor_id,
        address=entry.governor_address,
        chain_id=entry.chain_id or 0,
        governance_system=entry.governance_system,
    )


def _empty_sampling_error(message: str) -> dict:
    """Build an empty per-DAO sampling report with an error."""
    return {
        "indexed_total": 0,
        "eligible_total": 0,
        "sampled_total": 0,
        "actual_distribution": {},
        "fallback_events": [],
        "shortfall": 20,
        "excluded_status_counts": {},
        "missing_created_block": 0,
        "error": message,
    }


def _reset_jsonl(path: Path) -> None:
    """Reset a JSONL output file for a fresh collection run."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")


def _merge_counts(target: dict, source: dict) -> None:
    """Merge integer count dictionaries in place."""
    for key, value in source.items():
        target[key] = target.get(key, 0) + value


def _relative_posix(path: Path, root: Path) -> str:
    """Return a stable root-relative path if possible."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def print_sampled_proposals(dao: DaoConfig, selections: list) -> None:
    """Print sampled proposal IDs for one DAO."""
    print(f"dao_id: {dao.dao_id}")
    print(f"name: {dao.name}")
    print(f"sampled_total: {len(selections)}")
    print("sampled_proposals:")
    for selection in selections:
        record = selection_to_dict(selection)
        print(
            "  "
            f"{record['benchmark_id']} "
            f"proposal_id={record['proposal_id']} "
            f"status={record['status']} "
            f"time_bucket={record['time_bucket']} "
            f"status_bucket={record['status_bucket']} "
            f"created_block={record['created_block']}"
        )
    print()


def inspect_dao_proposals(client: TallyClient, dao: DaoConfig) -> None:
    """Fetch and print proposal statistics for one DAO."""
    try:
        governors = fetch_governors(client, dao)
        selected_governors = select_proposal_governors(governors, dao.expected_chain_id)
        proposal_index: list[ProposalIndexEntry] = []
        for governor in selected_governors:
            proposals = fetch_proposals(client, governor)
            proposal_index.extend(build_proposal_index(dao, governor, proposals))
    except (TallyClientError, ValueError) as exc:
        print(f"dao_id: {dao.dao_id}")
        print(f"name: {dao.name}")
        print(f"tally_slug: {dao.tally_slug}")
        print(f"error: {exc}")
        print()
        return

    print_proposal_stats(
        dao,
        governor_ids=[governor.governor_id for governor in selected_governors],
        entries=proposal_index,
    )


def select_proposal_governors(
    governors: list[GovernorInfo],
    expected_chain_id: int,
) -> list[GovernorInfo]:
    """Select governors to inspect for proposal lists."""
    matching = [
        governor for governor in governors if governor.chain_id == expected_chain_id
    ]
    if matching:
        return matching
    return [select_primary_governor(governors, expected_chain_id)]


def print_proposal_stats(
    dao: DaoConfig,
    governor_ids: list[str],
    entries: list[ProposalIndexEntry],
) -> None:
    """Print aggregate proposal statistics for one DAO."""
    status_counts = Counter(entry.status or "<missing>" for entry in entries)
    missing_created_block = sum(1 for entry in entries if entry.created_block is None)
    created_blocks = [
        entry.created_block for entry in entries if entry.created_block is not None
    ]

    print(f"dao_id: {dao.dao_id}")
    print(f"name: {dao.name}")
    print(f"tally_slug: {dao.tally_slug}")
    print(f"governor_count: {len(governor_ids)}")
    print("governor_ids:")
    for governor_id in governor_ids:
        print(f"  {governor_id}")
    print(f"proposal_total: {len(entries)}")
    print("status_counts:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    print(f"created_block_missing: {missing_created_block}")
    print(f"earliest_created_block: {min(created_blocks) if created_blocks else '<none>'}")
    print(f"latest_created_block: {max(created_blocks) if created_blocks else '<none>'}")
    print()


def print_governor_info(client: TallyClient, dao: DaoConfig) -> None:
    """Print one DAO's selected governor metadata."""
    try:
        governors = fetch_governors(client, dao)
    except TallyClientError as exc:
        print(f"dao_id: {dao.dao_id}")
        print(f"name: {dao.name}")
        print(f"tally_slug: {dao.tally_slug}")
        print(f"error: {exc}")
        print()
        return

    if not governors:
        print(f"dao_id: {dao.dao_id}")
        print(f"name: {dao.name}")
        print(f"tally_slug: {dao.tally_slug}")
        print("governor_id: <not found>")
        print("chain_id: <not found>")
        print("governor_address: <not found>")
        print("governance_system: <not found>")
        print("chain_id_check: MISMATCH")
        print()
        return

    governor = select_primary_governor(governors, dao.expected_chain_id)
    chain_id_check = "OK" if governor.chain_id == dao.expected_chain_id else "MISMATCH"

    print(f"dao_id: {dao.dao_id}")
    print(f"name: {dao.name}")
    print(f"tally_slug: {dao.tally_slug}")
    print(f"governor_id: {governor.governor_id}")
    print(f"chain_id: {governor.chain_id}")
    print(f"governor_address: {governor.address}")
    print(f"governance_system: {governor.governance_system}")
    print(f"chain_id_check: {chain_id_check}")
    print()


def main() -> int:
    """Parse CLI arguments and run the collector."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, ValueError, TallyClientError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
