from __future__ import annotations

import csv
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from agent_core.fixtures import (
    load_expected_case,
    load_policy_rules,
    load_requesters,
    load_sales_rows,
)
from agent_core.models import StructuredRequest
from agent_core.policies.engine import evaluate_policy
from agent_core.report_generation.builder import build_report_plan
from agent_core.workflow import process_request


class PortableCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.requesters = load_requesters()
        cls.policy_rules = load_policy_rules()
        cls.sales_rows = load_sales_rows()

    def test_policy_decisions_match_expected_cases(self) -> None:
        for index in range(1, 9):
            case_id = f"case-{index:03d}"
            with self.subTest(case_id=case_id):
                expected = load_expected_case(case_id)
                request = StructuredRequest.from_dict(expected["structured_request"])
                decision = evaluate_policy(
                    request,
                    self.requesters.get(expected["requester_id"]),
                    self.policy_rules,
                )
                expected_decision = expected["policy_decision"]
                self.assertEqual(decision.decision, expected_decision["decision"])
                self.assertEqual(decision.reason_codes, expected_decision["reason_codes"])
                self.assertEqual(
                    decision.approval_required,
                    expected_decision["approval_required"],
                )
                self.assertEqual(decision.excluded_fields, expected_decision["excluded_fields"])

    def test_report_plan_matches_expected_report_cases(self) -> None:
        for case_id in ["case-001", "case-003", "case-008"]:
            with self.subTest(case_id=case_id):
                expected = load_expected_case(case_id)
                request = StructuredRequest.from_dict(expected["structured_request"])
                plan = build_report_plan(request)
                self.assertEqual(plan.to_dict(), expected["report_plan"])

    def test_process_generates_csv_report_and_audit(self) -> None:
        expected = load_expected_case("case-008")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = process_request(
                request_id="case-008",
                requester_id=expected["requester_id"],
                structured_request=StructuredRequest.from_dict(expected["structured_request"]),
                output_dir=tmp_path / "reports",
                audit_dir=tmp_path / "traces",
                requesters=self.requesters,
                policy_rules=self.policy_rules,
                sales_rows=self.sales_rows,
            )

            self.assertEqual(result.outcome, "generated_report")
            self.assertIsNotNone(result.output_path)
            output_path = Path(result.output_path or "")
            self.assertEqual(output_path.suffix, ".csv")
            self.assertTrue(output_path.exists())

            with output_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 12)
            self.assertEqual(list(rows[0]), ["month", "revenue"])

            audit_path = tmp_path / "traces" / "case-008.json"
            self.assertTrue(audit_path.exists())
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            self.assertEqual(audit["outcome"], "generated_report")

    def test_process_generates_xlsx_with_expected_sheets(self) -> None:
        expected = load_expected_case("case-001")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = process_request(
                request_id="case-001",
                requester_id=expected["requester_id"],
                structured_request=StructuredRequest.from_dict(expected["structured_request"]),
                output_dir=tmp_path / "reports",
                audit_dir=tmp_path / "traces",
                requesters=self.requesters,
                policy_rules=self.policy_rules,
                sales_rows=self.sales_rows,
            )

            self.assertEqual(result.outcome, "generated_report")
            output_path = Path(result.output_path or "")
            self.assertEqual(output_path.suffix, ".xlsx")
            self.assertTrue(output_path.exists())

            with zipfile.ZipFile(output_path) as archive:
                names = set(archive.namelist())
            self.assertIn("xl/worksheets/sheet1.xml", names)
            self.assertIn("xl/worksheets/sheet2.xml", names)
            self.assertIn("xl/worksheets/sheet3.xml", names)

    def test_response_uses_date_bounds_when_label_missing(self) -> None:
        expected = load_expected_case("case-001")
        request_data = dict(expected["structured_request"])
        request_data["date_range"] = {
            key: value
            for key, value in request_data["date_range"].items()
            if key != "label"
        }

        with tempfile.TemporaryDirectory() as tmp:
            result = process_request(
                request_id="case-001",
                requester_id=expected["requester_id"],
                structured_request=StructuredRequest.from_dict(request_data),
                output_dir=Path(tmp) / "reports",
                audit_dir=Path(tmp) / "traces",
                requesters=self.requesters,
                policy_rules=self.policy_rules,
                sales_rows=self.sales_rows,
            )

        self.assertEqual(result.outcome, "generated_report")
        self.assertIn("2025-10-01 to 2025-12-31", result.response_message)
        self.assertNotIn("for None", result.response_message)

    def test_clarification_does_not_generate_report(self) -> None:
        expected = load_expected_case("case-002")
        with tempfile.TemporaryDirectory() as tmp:
            result = process_request(
                request_id="case-002",
                requester_id=expected["requester_id"],
                structured_request=StructuredRequest.from_dict(expected["structured_request"]),
                output_dir=Path(tmp) / "reports",
                audit_dir=Path(tmp) / "traces",
                requesters=self.requesters,
                policy_rules=self.policy_rules,
                sales_rows=self.sales_rows,
            )
            self.assertEqual(result.outcome, "clarification_required")
            self.assertIsNone(result.output_path)
            self.assertIn("reply in this email thread", result.response_message)


if __name__ == "__main__":
    unittest.main()
