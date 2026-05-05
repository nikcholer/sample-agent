from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path
from typing import Any

from agent_core.fixtures import load_expected_case
from agent_core.models import StructuredRequest
from agent_core.workflow import process_request


EVALUATION_CASE_IDS = tuple(f"case-{index:03d}" for index in range(1, 9))
MISSING = "<missing>"


def run_core_fixture_case(
    case_id: str,
    *,
    output_dir: Path,
    audit_dir: Path,
) -> dict[str, Any]:
    expected = load_expected_case(case_id)
    result = process_request(
        request_id=case_id,
        requester_id=expected["requester_id"],
        structured_request=StructuredRequest.from_dict(expected["structured_request"]),
        output_dir=output_dir,
        audit_dir=audit_dir,
    )
    return result.to_dict()


def evaluate_result(
    *,
    case_id: str,
    actual_result: Any,
    implementation: str,
    provider: str | None = None,
    model: str | None = None,
    repeat: int = 1,
    repo_root: Path | None = None,
    audit_dir: Path | None = None,
) -> dict[str, Any]:
    expected = load_expected_case(case_id)
    actual = _result_to_dict(actual_result)
    repo_root = repo_root or Path.cwd()
    mismatches: list[dict[str, Any]] = []

    _compare("outcome", expected["expected_outcome"], actual.get("outcome"), mismatches)
    _compare("requester_id", expected["requester_id"], _requester_id(actual), mismatches)
    _compare(
        "structured_request",
        expected["structured_request"],
        actual.get("structured_request"),
        mismatches,
    )
    _compare(
        "policy_decision",
        expected["policy_decision"],
        actual.get("policy_decision"),
        mismatches,
    )
    _compare(
        "report_plan",
        expected.get("report_plan"),
        actual.get("report_plan"),
        mismatches,
    )
    _check_output_file(
        expected=expected,
        actual=actual,
        repo_root=repo_root,
        mismatches=mismatches,
    )
    _check_audit_event(
        case_id=case_id,
        expected=expected,
        actual=actual,
        audit_dir=audit_dir,
        mismatches=mismatches,
    )

    return {
        "case_id": case_id,
        "implementation": implementation,
        "provider": provider,
        "model": model,
        "repeat": repeat,
        "passed": not mismatches,
        "expected_outcome": expected["expected_outcome"],
        "actual_outcome": actual.get("outcome"),
        "output_path": actual.get("output_path"),
        "mismatches": mismatches,
    }


def summarize_evaluations(results: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(1 for result in results if result["passed"])
    failed = len(results) - passed
    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / len(results), 3) if results else 0,
    }


def _result_to_dict(result: Any) -> dict[str, Any]:
    if isinstance(result, dict):
        return result
    if hasattr(result, "to_dict"):
        return result.to_dict()
    if hasattr(result, "model_dump"):
        return result.model_dump(mode="json")
    raise TypeError(f"Unsupported result type: {type(result)!r}")


def _requester_id(actual: dict[str, Any]) -> Any:
    return actual.get("requester_id") or actual.get("audit_event", {}).get("requester_id")


def _compare(
    path: str,
    expected: Any,
    actual: Any,
    mismatches: list[dict[str, Any]],
) -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            _add_mismatch(path, expected, actual, mismatches)
            return
        for key in sorted(set(expected) | set(actual)):
            child_path = f"{path}.{key}"
            if key not in expected:
                _add_mismatch(child_path, MISSING, actual[key], mismatches)
            elif key not in actual:
                _add_mismatch(child_path, expected[key], MISSING, mismatches)
            else:
                _compare(child_path, expected[key], actual[key], mismatches)
        return

    if expected != actual:
        _add_mismatch(path, expected, actual, mismatches)


def _add_mismatch(
    field: str,
    expected: Any,
    actual: Any,
    mismatches: list[dict[str, Any]],
) -> None:
    mismatches.append(
        {
            "field": field,
            "expected": expected,
            "actual": actual,
        }
    )


def _check_output_file(
    *,
    expected: dict[str, Any],
    actual: dict[str, Any],
    repo_root: Path,
    mismatches: list[dict[str, Any]],
) -> None:
    output_path = actual.get("output_path")
    if expected["expected_outcome"] != "generated_report":
        if output_path is not None:
            _add_mismatch("output_path", None, output_path, mismatches)
        return

    if not output_path:
        _add_mismatch("output_path", "report file path", output_path, mismatches)
        return

    path = _resolve_path(output_path, repo_root)
    if not path.exists():
        _add_mismatch("output_path.exists", True, False, mismatches)
        return

    expected_plan = expected.get("report_plan") or {}
    expected_format = expected_plan.get("output_format")
    if expected_format and path.suffix != f".{expected_format}":
        _add_mismatch("output_path.suffix", f".{expected_format}", path.suffix, mismatches)

    if expected_format == "csv":
        _check_csv_headers(path, expected_plan, mismatches)
    elif expected_format == "xlsx":
        _check_xlsx_sheets(path, mismatches)


def _resolve_path(path: str, repo_root: Path) -> Path:
    resolved = Path(path)
    if resolved.is_absolute():
        return resolved
    return repo_root / resolved


def _check_csv_headers(
    path: Path,
    expected_plan: dict[str, Any],
    mismatches: list[dict[str, Any]],
) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        headers = next(reader, [])
    expected_headers = [
        *expected_plan.get("group_by", []),
        *expected_plan.get("metrics", []),
    ]
    if headers != expected_headers:
        _add_mismatch("report_file.headers", expected_headers, headers, mismatches)


def _check_xlsx_sheets(path: Path, mismatches: list[dict[str, Any]]) -> None:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    expected_names = {
        "xl/worksheets/sheet1.xml",
        "xl/worksheets/sheet2.xml",
        "xl/worksheets/sheet3.xml",
    }
    missing = sorted(expected_names - names)
    if missing:
        _add_mismatch("report_file.xlsx_sheets", sorted(expected_names), sorted(names), mismatches)


def _check_audit_event(
    *,
    case_id: str,
    expected: dict[str, Any],
    actual: dict[str, Any],
    audit_dir: Path | None,
    mismatches: list[dict[str, Any]],
) -> None:
    audit_event = actual.get("audit_event")
    if not isinstance(audit_event, dict):
        _add_mismatch("audit_event", "audit event", audit_event, mismatches)
        return

    _compare("audit_event.request_id", case_id, audit_event.get("request_id"), mismatches)
    _compare(
        "audit_event.requester_id",
        expected["requester_id"],
        audit_event.get("requester_id"),
        mismatches,
    )
    _compare(
        "audit_event.outcome",
        expected["expected_outcome"],
        audit_event.get("outcome"),
        mismatches,
    )
    _compare(
        "audit_event.policy_decision",
        expected["policy_decision"],
        audit_event.get("policy_decision"),
        mismatches,
    )

    if audit_dir is not None:
        audit_path = audit_dir / f"{case_id}.json"
        if not audit_path.exists():
            _add_mismatch("audit_file.exists", True, False, mismatches)
        else:
            json.loads(audit_path.read_text(encoding="utf-8"))
