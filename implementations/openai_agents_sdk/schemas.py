from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class DateRangeInput(BaseModel):
    start: str = Field(description="Inclusive ISO start date, YYYY-MM-DD.")
    end: str = Field(description="Inclusive ISO end date, YYYY-MM-DD.")
    label: str | None = Field(default=None, description="Human label such as Q4 2025.")
    reference_date: str | None = Field(
        default=None,
        description="Reference date used to resolve relative phrases such as last quarter.",
    )


class ReportRequestInput(BaseModel):
    report_type: Literal[
        "sales_summary",
        "product_breakdown",
        "monthly_trend",
        "top_n",
        "filtered_raw_extract",
        "unsupported",
    ]
    metrics: list[str] = Field(default_factory=list)
    dimensions: list[str] = Field(default_factory=list)
    date_range: DateRangeInput | None = None
    filters: dict[str, list[str]] = Field(default_factory=dict)
    output_format: Literal["csv", "xlsx"] | None = None
    purpose: str | None = None
    limit: int | None = None
    sort_by: str | None = None
    ambiguous_terms: dict[str, list[str]] = Field(default_factory=dict)


class ToolResult(BaseModel):
    request_id: str
    outcome: Literal[
        "generated_report",
        "clarification_required",
        "approval_required",
        "rejected",
    ]
    structured_request: dict[str, Any]
    policy_decision: dict[str, Any]
    response_message: str
    report_plan: dict[str, Any] | None = None
    output_path: str | None = None
    audit_event: dict[str, Any]


class AgentFinalOutput(BaseModel):
    request_id: str
    requester_id: str
    outcome: Literal[
        "generated_report",
        "clarification_required",
        "approval_required",
        "rejected",
    ]
    response_message: str
    structured_request: dict[str, Any]
    policy_decision: dict[str, Any]
    report_plan: dict[str, Any] | None = None
    output_path: str | None = None
    audit_event: dict[str, Any] | None = None
    notes: list[str] = Field(default_factory=list)
