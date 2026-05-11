from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent

ORDERED_LEVELS = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
EXCLUDED_LEVELS = {"UNKNOWN", "UNSURE", "SKIP", "N/A", ""}
DIMENSIONS = ("conflict_detection", "depth_analysis", "function_semantic_match")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare GovGap outputs with human labels without claiming full benchmark accuracy."
    )
    parser.add_argument("--labels-dir", type=Path, default=Path("../benchmark/data/human_labels"))
    parser.add_argument("--scores-dir", type=Path, default=Path("outputs/scores"))
    parser.add_argument("--samples-dir", type=Path, default=Path("data/raw_samples"))
    parser.add_argument("--summary-dir", type=Path, default=Path("outputs/label_evaluation"))
    args = parser.parse_args()

    labels_dir = _resolve_path(args.labels_dir)
    scores_dir = _resolve_path(args.scores_dir)
    samples_dir = _resolve_path(args.samples_dir)
    summary_dir = _resolve_path(args.summary_dir, must_exist=False)
    summary_dir.mkdir(parents=True, exist_ok=True)

    labels, label_warnings = _load_labels(labels_dir)
    scores = _load_scores(scores_dir)
    sample_daos = _load_sample_daos(samples_dir)

    rows: list[dict[str, Any]] = []
    warnings = list(label_warnings)
    for benchmark_id, label in sorted(labels.items()):
        score = scores.get(benchmark_id)
        if score is None:
            warnings.append(f"{benchmark_id}: missing score output")
            continue

        tool_overall = _normalize_level(score.get("overall", {}).get("risk_level"))
        human_overall = _normalize_level(label.get("human_overall_risk"))
        row: dict[str, Any] = {
            "benchmark_id": benchmark_id,
            "dao": sample_daos.get(benchmark_id, ""),
            "human_overall_risk": human_overall,
            "tool_overall_risk": tool_overall,
            "overall_included": _is_included(human_overall) and _is_included(tool_overall),
            "overall_match": human_overall == tool_overall
            if _is_included(human_overall) and _is_included(tool_overall)
            else None,
            "overall_distance": _distance(human_overall, tool_overall),
        }

        dimension_labels = label.get("dimension_labels", {})
        dimensions = score.get("dimensions", {})
        if not isinstance(dimension_labels, dict):
            warnings.append(f"{benchmark_id}: dimension_labels is not an object")
            dimension_labels = {}
        if not isinstance(dimensions, dict):
            warnings.append(f"{benchmark_id}: score dimensions is not an object")
            dimensions = {}

        for dimension in DIMENSIONS:
            human_dimension = _normalize_level(dimension_labels.get(dimension))
            tool_dimension = _normalize_level(dimensions.get(dimension, {}).get("severity"))
            row[f"human_{dimension}"] = human_dimension
            row[f"tool_{dimension}"] = tool_dimension
            row[f"{dimension}_included"] = _is_included(human_dimension) and _is_included(tool_dimension)
            row[f"{dimension}_match"] = (
                human_dimension == tool_dimension
                if _is_included(human_dimension) and _is_included(tool_dimension)
                else None
            )
            row[f"{dimension}_distance"] = _distance(human_dimension, tool_dimension)

        rows.append(row)

    summary = _build_summary(rows, warnings)
    _write_json(summary_dir / "label-evaluation-summary.json", {"summary": summary, "rows": rows})
    _write_csv(summary_dir / "label-evaluation-rows.csv", rows)
    (summary_dir / "label-confusion-matrices.md").write_text(
        _build_confusion_markdown(summary),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)


def _resolve_path(path: Path, *, must_exist: bool = True) -> Path:
    if path.is_absolute():
        return path
    candidates = [Path.cwd() / path, PROJECT_ROOT / path, REPO_ROOT / path]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if must_exist else candidates[0]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _load_labels(labels_dir: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    labels: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    for path in sorted(labels_dir.glob("*.json")):
        try:
            payload = _load_json(path)
        except Exception as exc:
            warnings.append(f"{path.name}: cannot parse label JSON: {type(exc).__name__}: {exc}")
            continue
        benchmark_id = str(payload.get("benchmark_id") or _benchmark_id_from_label_filename(path))
        if benchmark_id in labels:
            warnings.append(f"{benchmark_id}: duplicate label, keeping last file {path.name}")
        labels[benchmark_id] = payload
    return labels, warnings


def _benchmark_id_from_label_filename(path: Path) -> str:
    stem = path.stem
    if stem.startswith("label-"):
        return f"real-{stem.removeprefix('label-')}"
    return stem


def _load_scores(scores_dir: Path) -> dict[str, dict[str, Any]]:
    scores: dict[str, dict[str, Any]] = {}
    for path in sorted(scores_dir.glob("*-score.json")):
        benchmark_id = path.name.removesuffix("-score.json")
        scores[benchmark_id] = _load_json(path)
    return scores


def _load_sample_daos(samples_dir: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(samples_dir.glob("*.json")):
        try:
            payload = _load_json(path)
        except Exception:
            continue
        benchmark_id = str(payload.get("benchmark_id") or path.stem)
        dao = payload.get("dao")
        if isinstance(dao, dict):
            result[benchmark_id] = str(dao.get("name", ""))
    return result


def _normalize_level(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip().upper()
    if text in {"NONE", "NO_RISK"}:
        return "LOW"
    return text


def _is_included(level: str) -> bool:
    return level in ORDERED_LEVELS


def _distance(left: str, right: str) -> int | None:
    if not _is_included(left) or not _is_included(right):
        return None
    return abs(ORDERED_LEVELS.index(left) - ORDERED_LEVELS.index(right))


def _build_summary(rows: list[dict[str, Any]], warnings: list[str]) -> dict[str, Any]:
    overall_rows = [row for row in rows if row["overall_included"]]
    summary: dict[str, Any] = {
        "labels_seen": len(rows),
        "overall_evaluated": len(overall_rows),
        "overall_exact_match_count": sum(1 for row in overall_rows if row["overall_match"]),
        "overall_within_one_level_count": sum(
            1 for row in overall_rows if int(row["overall_distance"] or 0) <= 1
        ),
        "human_overall_distribution": _counter(rows, "human_overall_risk"),
        "tool_overall_distribution": _counter(rows, "tool_overall_risk"),
        "overall_confusion_matrix": _confusion_matrix(
            rows,
            human_key="human_overall_risk",
            tool_key="tool_overall_risk",
        ),
        "dimension_results": {},
        "warnings": warnings,
    }
    summary["overall_exact_match_rate"] = _rate(
        summary["overall_exact_match_count"],
        summary["overall_evaluated"],
    )
    summary["overall_within_one_level_rate"] = _rate(
        summary["overall_within_one_level_count"],
        summary["overall_evaluated"],
    )
    if len([level for level, count in summary["human_overall_distribution"].items() if count > 0]) <= 1:
        summary["warnings"].append(
            "Human overall labels contain one included class only; do not report this as a mature accuracy estimate."
        )

    for dimension in DIMENSIONS:
        included_key = f"{dimension}_included"
        match_key = f"{dimension}_match"
        distance_key = f"{dimension}_distance"
        human_key = f"human_{dimension}"
        tool_key = f"tool_{dimension}"
        dimension_rows = [row for row in rows if row[included_key]]
        result = {
            "evaluated": len(dimension_rows),
            "exact_match_count": sum(1 for row in dimension_rows if row[match_key]),
            "within_one_level_count": sum(
                1 for row in dimension_rows if int(row[distance_key] or 0) <= 1
            ),
            "human_distribution": _counter(rows, human_key),
            "tool_distribution": _counter(rows, tool_key),
            "confusion_matrix": _confusion_matrix(rows, human_key=human_key, tool_key=tool_key),
        }
        result["exact_match_rate"] = _rate(result["exact_match_count"], result["evaluated"])
        result["within_one_level_rate"] = _rate(result["within_one_level_count"], result["evaluated"])
        summary["dimension_results"][dimension] = result

    return summary


def _counter(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in rows if _is_included(str(row[key]))).items()))


def _confusion_matrix(rows: list[dict[str, Any]], *, human_key: str, tool_key: str) -> dict[str, dict[str, int]]:
    matrix = {human: {tool: 0 for tool in ORDERED_LEVELS} for human in ORDERED_LEVELS}
    for row in rows:
        human = str(row[human_key])
        tool = str(row[tool_key])
        if _is_included(human) and _is_included(tool):
            matrix[human][tool] += 1
    return matrix


def _rate(count: int, total: int) -> float | None:
    return round(count / total, 4) if total else None


def _build_confusion_markdown(summary: dict[str, Any]) -> str:
    lines = ["# Human Label Evaluation", ""]
    lines.append("## Overall")
    lines.extend(_matrix_to_markdown(summary["overall_confusion_matrix"]))
    for dimension, result in summary["dimension_results"].items():
        lines.extend(["", f"## {dimension}"])
        lines.extend(_matrix_to_markdown(result["confusion_matrix"]))
    if summary["warnings"]:
        lines.extend(["", "## Warnings", ""])
        for warning in summary["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def _matrix_to_markdown(matrix: dict[str, dict[str, int]]) -> list[str]:
    lines = ["", "| Human \\ Tool | LOW | MEDIUM | HIGH | CRITICAL |", "| --- | ---: | ---: | ---: | ---: |"]
    for human in ORDERED_LEVELS:
        row = matrix[human]
        lines.append(
            f"| {human} | {row['LOW']} | {row['MEDIUM']} | {row['HIGH']} | {row['CRITICAL']} |"
        )
    return lines


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
