from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_core.fixtures import load_expected_case
from implementations.openai_agents_sdk.instructions import INTAKE_AGENT_INSTRUCTIONS
from implementations.openai_agents_sdk.runner import _parse_tool_output
from implementations.openai_agents_sdk.schemas import (
    AgentFinalOutput,
    ReportRequestInput,
)
from implementations.openai_agents_sdk.tools import (
    process_sales_report_request_for_agent,
    process_sales_report_request_raw,
)


class OpenAIAgentsAdapterTests(unittest.TestCase):
    def test_tool_wrapper_processes_all_fixture_outcomes(self) -> None:
        for index in range(1, 9):
            case_id = f"case-{index:03d}"
            with self.subTest(case_id=case_id):
                expected = load_expected_case(case_id)
                with tempfile.TemporaryDirectory() as tmp:
                    tmp_path = Path(tmp)
                    result = process_sales_report_request_raw(
                        request_id=case_id,
                        requester_id=expected["requester_id"],
                        structured_request=ReportRequestInput(
                            **expected["structured_request"]
                        ),
                        output_dir=str(tmp_path / "reports"),
                        audit_dir=str(tmp_path / "traces"),
                    )

                self.assertEqual(result["outcome"], expected["expected_outcome"])
                self.assertEqual(
                    result["policy_decision"]["decision"],
                    expected["policy_decision"]["decision"],
                )
                self.assertEqual(
                    result["policy_decision"]["reason_codes"],
                    expected["policy_decision"]["reason_codes"],
                )

    def test_final_output_schema_accepts_tool_result(self) -> None:
        expected = load_expected_case("case-002")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tool_result = process_sales_report_request_raw(
                request_id="case-002",
                requester_id=expected["requester_id"],
                structured_request=ReportRequestInput(**expected["structured_request"]),
                output_dir=str(tmp_path / "reports"),
                audit_dir=str(tmp_path / "traces"),
            )

        final = AgentFinalOutput(
            **tool_result,
        )
        self.assertEqual(final.outcome, "clarification_required")
        self.assertIn("reply in this email thread", final.response_message)

    def test_agent_tool_output_is_json_text_for_non_openai_providers(self) -> None:
        expected = load_expected_case("case-001")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tool_output = process_sales_report_request_for_agent(
                request_id="case-001",
                requester_email="amira.shah@example.test",
                structured_request=ReportRequestInput(**expected["structured_request"]),
                output_dir=str(tmp_path / "reports"),
                audit_dir=str(tmp_path / "traces"),
            )

        parsed = _parse_tool_output(tool_output)
        final = AgentFinalOutput(**parsed)
        self.assertEqual(final.outcome, "generated_report")
        self.assertEqual(final.requester_id, "u-1001")

    def test_tool_resolves_requester_email(self) -> None:
        expected = load_expected_case("case-001")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = process_sales_report_request_raw(
                request_id="case-001",
                requester_email="amira.shah@example.test",
                structured_request=ReportRequestInput(**expected["structured_request"]),
                output_dir=str(tmp_path / "reports"),
                audit_dir=str(tmp_path / "traces"),
            )

        self.assertEqual(result["audit_event"]["requester_id"], "u-1001")
        self.assertEqual(result["requester_id"], "u-1001")
        self.assertEqual(result["outcome"], "generated_report")

    def test_agent_forces_tool_use_and_stops_on_tool_output(self) -> None:
        try:
            from agents import FunctionTool
        except ImportError:
            self.skipTest("OpenAI Agents SDK is not installed in this Python environment.")

        from implementations.openai_agents_sdk.agent import build_intake_agent

        agent = build_intake_agent("gpt-5-mini")
        self.assertEqual(agent.model_settings.tool_choice, "required")
        self.assertFalse(agent.model_settings.parallel_tool_calls)
        self.assertEqual(agent.tool_use_behavior, "stop_on_first_tool")
        self.assertIsNone(agent.output_type)
        self.assertIsInstance(agent.tools[0], FunctionTool)
        self.assertEqual(agent.tools[0].name, "process_sales_report_request")

    def test_instructions_preserve_portable_core_boundary(self) -> None:
        self.assertIn("call the portable core tool exactly once", INTAKE_AGENT_INSTRUCTIONS)
        self.assertIn("must not calculate", INTAKE_AGENT_INSTRUCTIONS)
        self.assertIn("must not bypass policy", INTAKE_AGENT_INSTRUCTIONS)
        self.assertIn("reply", INTAKE_AGENT_INSTRUCTIONS)
        self.assertIn("same email thread", INTAKE_AGENT_INSTRUCTIONS)


if __name__ == "__main__":
    unittest.main()
