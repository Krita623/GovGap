from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


BENCHMARK_ROOT = Path(__file__).resolve().parents[1]
RAW_SAMPLES_DIR = BENCHMARK_ROOT / "data" / "mutant_samples"
SEMANTICS_DIR = BENCHMARK_ROOT / "data" / "mutant_semantics"
SUMMARY_DIR = BENCHMARK_ROOT / "data" / "summaries"

TIMELOCK = "0x1000000000000000000000000000000000000001"
GOVERNOR = "0x1000000000000000000000000000000000000002"
PROXY_BASE = "0x20000000000000000000000000000000000000"
TOKEN_BASE = "0x30000000000000000000000000000000000000"
RECIPIENT_BASE = "0x40000000000000000000000000000000000000"
IMPLEMENTATION_BASE = "0x50000000000000000000000000000000000000"
ROLE_BASE = "0x60000000000000000000000000000000000000"


@dataclass(frozen=True)
class MutationCase:
    benchmark_id: str
    group: str
    selector: str
    decoded_function: str
    target: str
    args: list[object]
    claimed_action: str
    claimed_effect: str
    title: str
    description: str


def main() -> None:
    for path in (RAW_SAMPLES_DIR, SEMANTICS_DIR, SUMMARY_DIR):
        path.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for case in _cases():
        sample_path = RAW_SAMPLES_DIR / f"{case.benchmark_id}.json"
        semantics_path = SEMANTICS_DIR / f"{case.benchmark_id}-semantics.json"
        sample_path.write_text(json.dumps(_sample(case), indent=2, ensure_ascii=False), encoding="utf-8")
        semantics_path.write_text(json.dumps(_semantics(case), indent=2, ensure_ascii=False), encoding="utf-8")
        rows.append(
            {
                "benchmark_id": case.benchmark_id,
                "risk_group": case.group,
                "sample": str(sample_path.relative_to(BENCHMARK_ROOT)),
                "semantics": str(semantics_path.relative_to(BENCHMARK_ROOT)),
            }
        )

    summary = _summary(rows)
    (SUMMARY_DIR / "mutant-samples-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    with (SUMMARY_DIR / "mutant-samples-summary.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(summary, indent=2, ensure_ascii=False))


def _cases() -> list[MutationCase]:
    cases: list[MutationCase] = []
    for index in range(1, 9):
        cases.append(
            MutationCase(
                benchmark_id=f"mutant-upgrade-{index:04d}",
                group="upgrade",
                selector="0x3659cfe6",
                decoded_function="upgradeTo(address)",
                target=_addr(PROXY_BASE, index),
                args=[_addr(IMPLEMENTATION_BASE, index)],
                claimed_action="maintenance",
                claimed_effect="Routine parameter maintenance and metadata refresh.",
                title=f"Routine market maintenance batch {index}",
                description="This proposal performs routine maintenance and parameter housekeeping.",
            )
        )

    for index in range(1, 9):
        cases.append(
            MutationCase(
                benchmark_id=f"mutant-permission-{index:04d}",
                group="permission_change",
                selector="0x2f2ff15d",
                decoded_function="grantRole(bytes32,address)",
                target=_addr(ROLE_BASE, index),
                args=["0x" + "0" * 63 + f"{index:x}", _addr(RECIPIENT_BASE, index)],
                claimed_action="parameter_update",
                claimed_effect="Update non-security configuration values.",
                title=f"Configuration update batch {index}",
                description="This proposal updates configuration values without changing privileged operators.",
            )
        )

    for index in range(1, 9):
        cases.append(
            MutationCase(
                benchmark_id=f"mutant-transfer-{index:04d}",
                group="transfer",
                selector="0xa9059cbb",
                decoded_function="transfer(address,uint256)",
                target=_addr(TOKEN_BASE, index),
                args=[_addr(RECIPIENT_BASE, index), 10**18 * (index + 1)],
                claimed_action="maintenance",
                claimed_effect="Refresh accounting records without moving assets.",
                title=f"Accounting maintenance batch {index}",
                description="This proposal refreshes accounting records and does not mention token movement.",
            )
        )
    return cases


def _sample(case: MutationCase) -> dict[str, Any]:
    return {
        "benchmark_id": case.benchmark_id,
        "chain_id": 1,
        "dao": {"name": "mutant", "chain_id": 1, "governor_address": GOVERNOR},
        "proposal": {"proposal_id": case.benchmark_id, "fork_block_number": 19000000},
        "proposal_text": {"title": case.title, "description": case.description},
        "payload": {
            "targets": [case.target],
            "values": [0],
            "signatures": [case.decoded_function],
            "calldatas": [_fake_calldata(case.selector, case.args)],
        },
        "transactions": {},
        "rpc_url_env": "MAINNET_RPC_URL",
        "timelock": TIMELOCK,
        "executor": TIMELOCK,
        "mutation": {
            "constructed": True,
            "risk_group": case.group,
            "expected_risk_action": case.group,
        },
    }


def _semantics(case: MutationCase) -> dict[str, Any]:
    return {
        "proposal_summary": case.description,
        "disclosed_entities": [
            {
                "name": "DAO timelock",
                "address": TIMELOCK,
                "entity_type": "timelock",
                "disclosure_level": "implicit",
                "textual_evidence": "standard DAO execution context",
            }
        ],
        "disclosed_addresses": [],
        "claimed_actions": [
            {
                "raw_action": case.claimed_action,
                "canonical_action": case.claimed_action,
                "object": None,
                "claimed_effect": case.claimed_effect,
                "textual_evidence": case.description,
                "confidence": 0.82,
            }
        ],
        "claimed_complexity": {
            "level": "simple",
            "reason": "The text describes routine single-step maintenance.",
            "textual_evidence": case.description,
        },
        "disclosed_functions": [],
        "limitations": ["Synthetic mutant semantics intentionally omit the risky business action."],
        "llm_status": "success",
        "llm_used_for_scoring": False,
    }


def _fake_calldata(selector: str, args: list[object]) -> str:
    encoded = []
    for arg in args:
        if isinstance(arg, int):
            encoded.append(f"{arg:064x}")
        elif isinstance(arg, str) and arg.startswith("0x") and len(arg) == 42:
            encoded.append(arg[2:].rjust(64, "0"))
        elif isinstance(arg, str) and arg.startswith("0x"):
            encoded.append(arg[2:].rjust(64, "0")[:64])
        else:
            encoded.append("0" * 64)
    return selector + "".join(encoded)


def _addr(prefix: str, index: int) -> str:
    return f"{prefix}{index:02x}"[-42:]


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    risk_groups: dict[str, int] = {}
    for row in rows:
        group = str(row["risk_group"])
        risk_groups[group] = risk_groups.get(group, 0) + 1
    return {
        "total_mutant_samples": len(rows),
        "risk_groups": dict(sorted(risk_groups.items())),
        "rows": rows,
    }


if __name__ == "__main__":
    main()
