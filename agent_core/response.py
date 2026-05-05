from __future__ import annotations

from agent_core.models import PolicyDecision, ReportPlan, StructuredRequest


def draft_response(
    *,
    request: StructuredRequest,
    decision: PolicyDecision,
    output_path: str | None = None,
    missing_fields: list[str] | None = None,
) -> str:
    if decision.decision == "allowed":
        return _approved_response(request, output_path)
    if decision.decision in {"deferred", "clarification_required"}:
        return _clarification_response(request, decision, missing_fields or [])
    if decision.decision == "approval_required":
        approver = decision.approver or "the appropriate approver"
        return (
            "This request requires approval before a report can be generated. "
            f"Reason codes: {', '.join(decision.reason_codes)}. "
            f"The approval request should be routed to {approver}."
        )
    return (
        "I cannot complete this request as submitted. "
        f"Reason codes: {', '.join(decision.reason_codes)}."
    )


def describe_report_plan(plan: ReportPlan) -> str:
    return (
        f"{plan.source_table} grouped by {', '.join(plan.group_by) or 'raw rows'} "
        f"with metrics {', '.join(plan.metrics)}"
    )


def _approved_response(
    request: StructuredRequest,
    output_path: str | None,
) -> str:
    date_label = request.date_range.label if request.date_range else "the requested period"
    filters = ", ".join(
        f"{key}: {', '.join(values)}"
        for key, values in request.filters.items()
    ) or "none"
    return (
        f"Attached is the requested {request.report_type} for {date_label}. "
        f"Included metrics: {', '.join(request.metrics)}. "
        f"Dimensions: {', '.join(request.dimensions) or 'raw rows'}. "
        f"Filters applied: {filters}. "
        "No restricted fields are included. "
        f"Output: {output_path}."
    )


def _clarification_response(
    request: StructuredRequest,
    decision: PolicyDecision,
    missing_fields: list[str],
) -> str:
    questions: list[str] = []
    if "metrics" in missing_fields:
        questions.append(
            "confirm whether sales means revenue, units, gross margin, or all permitted metrics"
        )
    if "geography" in missing_fields:
        questions.append("confirm the country or region for the report")
    if "margin_not_permitted" in decision.reason_codes:
        questions.append(
            "confirm whether a revenue-only version would meet the need"
        )
    if not questions:
        questions.append("confirm the missing details needed to complete the report")

    return (
        "I can continue, but need clarification before generating a report. "
        "Please reply in this email thread and "
        + "; and ".join(questions)
        + "."
    )
