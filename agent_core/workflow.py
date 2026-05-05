from __future__ import annotations

from pathlib import Path
from typing import Any

from agent_core.audit import write_audit_event
from agent_core.fixtures import load_policy_rules, load_requesters, load_sales_rows
from agent_core.models import AuditEvent, ProcessResult, RequesterProfile, StructuredRequest
from agent_core.policies.engine import evaluate_policy
from agent_core.report_generation.builder import build_report_plan, generate_report
from agent_core.response import draft_response
from agent_core.validation import validate_request


def process_request(
    *,
    request_id: str,
    structured_request: StructuredRequest,
    requester_id: str,
    output_dir: Path | None = None,
    audit_dir: Path | None = None,
    parent_request_id: str | None = None,
    requesters: dict[str, RequesterProfile] | None = None,
    policy_rules: dict[str, Any] | None = None,
    sales_rows: list[dict[str, Any]] | None = None,
) -> ProcessResult:
    requesters = requesters or load_requesters()
    policy_rules = policy_rules or load_policy_rules()
    sales_rows = sales_rows or load_sales_rows()
    output_dir = output_dir or Path("generated") / "reports"

    requester = requesters.get(requester_id)
    validation = validate_request(structured_request, policy_rules)
    decision = evaluate_policy(structured_request, requester, policy_rules)

    report_plan = None
    output_path = None
    if decision.decision == "allowed":
        report_plan = build_report_plan(structured_request)
        metadata = {
            "request_id": request_id,
            "requester_id": requester_id,
            "report_type": structured_request.report_type,
            "date_range": structured_request.date_range.to_dict()
            if structured_request.date_range
            else None,
            "filters": structured_request.filters,
            "metrics": structured_request.metrics,
            "dimensions": structured_request.dimensions,
        }
        report = generate_report(
            plan=report_plan,
            source_rows=sales_rows,
            output_dir=output_dir,
            request_id=request_id,
            metadata=metadata,
        )
        output_path = report.path

    response = draft_response(
        request=structured_request,
        decision=decision,
        output_path=output_path,
        missing_fields=validation.missing_fields,
    )

    audit_event = AuditEvent.create(
        request_id=request_id,
        requester_id=requester_id,
        outcome=_outcome_for_decision(decision.decision),
        reason_codes=decision.reason_codes,
        structured_request=structured_request.to_dict(),
        policy_decision=decision.to_dict(),
        report_plan=report_plan.to_dict() if report_plan else None,
        output_path=output_path,
        parent_request_id=parent_request_id,
    )
    if audit_dir is not None:
        write_audit_event(audit_event, audit_dir)

    return ProcessResult(
        request_id=request_id,
        outcome=audit_event.outcome,
        structured_request=structured_request,
        policy_decision=decision,
        response_message=response,
        report_plan=report_plan,
        output_path=output_path,
        audit_event=audit_event,
    )


def _outcome_for_decision(decision: str) -> str:
    return {
        "allowed": "generated_report",
        "deferred": "clarification_required",
        "clarification_required": "clarification_required",
        "approval_required": "approval_required",
        "rejected": "rejected",
    }.get(decision, decision)
