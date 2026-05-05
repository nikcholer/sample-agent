from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_core.evaluation import (
    EVALUATION_CASE_IDS,
    evaluate_result,
    run_core_fixture_case,
    summarize_evaluations,
)
from agent_core.fixtures import load_expected_case


class EvaluationTests(unittest.TestCase):
    def test_core_evaluation_passes_all_fixture_cases(self) -> None:
        results = []
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for case_id in EVALUATION_CASE_IDS:
                actual = run_core_fixture_case(
                    case_id,
                    output_dir=tmp_path / "reports",
                    audit_dir=tmp_path / "traces",
                )
                results.append(
                    evaluate_result(
                        case_id=case_id,
                        actual_result=actual,
                        implementation="core",
                        repo_root=tmp_path,
                        audit_dir=tmp_path / "traces",
                    )
                )

        summary = summarize_evaluations(results)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["passed"], len(EVALUATION_CASE_IDS))

    def test_evaluation_reports_structured_request_mismatches(self) -> None:
        actual = {
            "request_id": "case-003",
            "requester_id": "u-1001",
            "outcome": "rejected",
            "structured_request": dict(load_expected_case("case-003")["structured_request"]),
            "policy_decision": {
                "decision": "rejected",
                "reason_codes": ["region_not_permitted"],
                "approval_required": False,
                "excluded_fields": [],
            },
            "report_plan": None,
            "output_path": None,
            "audit_event": {
                "request_id": "case-003",
                "requester_id": "u-1001",
                "outcome": "rejected",
                "policy_decision": {
                    "decision": "rejected",
                    "reason_codes": ["region_not_permitted"],
                    "approval_required": False,
                    "excluded_fields": [],
                },
            },
        }
        actual["structured_request"]["filters"] = {"region": ["UK"]}

        result = evaluate_result(
            case_id="case-003",
            actual_result=actual,
            implementation="openai",
        )

        fields = {mismatch["field"] for mismatch in result["mismatches"]}
        self.assertFalse(result["passed"])
        self.assertIn("structured_request.filters.country", fields)
        self.assertIn("structured_request.filters.region", fields)
        self.assertIn("outcome", fields)


if __name__ == "__main__":
    unittest.main()
