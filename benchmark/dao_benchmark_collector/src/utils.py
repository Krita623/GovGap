"""Shared utility helpers for the collector.

Utilities here should stay generic: JSONL writing, path setup, warning logs,
and stable serialization helpers.
"""

from __future__ import annotations

import json
from pathlib import Path


def ensure_output_dirs(base_output_dir: Path) -> None:
    """Create expected output directories if they do not exist."""
    base_output_dir.mkdir(parents=True, exist_ok=True)
    (base_output_dir / "raw_samples").mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: dict | list) -> None:
    """Write JSON with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")


def append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON record to a JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        json.dump(record, file, sort_keys=True)
        file.write("\n")
