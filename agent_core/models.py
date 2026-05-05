from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class DateRange:
    start: str
    end: str
    label: str | None = None
    reference_date: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "DateRange | None":
        if data is None:
            return None
        return cls(
            start=data["start"],
            end=data["end"],
            label=data.get("label"),
            reference_date=data.get("reference_date"),
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"start": self.start, "end": self.end}
        if self.label is not None:
            data["label"] = self.label
        if self.reference_date is not None:
            data["reference_date"] = self.reference_date
        return data


@dataclass(frozen=True)
class StructuredRequest:
    report_type: str
    metrics: list[str]
    dimensions: list[str]
    date_range: DateRange | None
    filters: dict[str, list[str]]
    output_format: str | None
    purpose: str | None = None
    limit: int | None = None
    sort_by: str | None = None
    ambiguous_terms: dict[str, list[str]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StructuredRequest":
        filters: dict[str, list[str]] = {}
        for key, value in data.get("filters", {}).items():
            filters[key] = value if isinstance(value, list) else [value]

        return cls(
            report_type=data["report_type"],
            metrics=list(data.get("metrics", [])),
            dimensions=list(data.get("dimensions", [])),
            date_range=DateRange.from_dict(data.get("date_range")),
            filters=filters,
            output_format=data.get("output_format"),
            purpose=data.get("purpose"),
            limit=data.get("limit"),
            sort_by=data.get("sort_by"),
            ambiguous_terms=dict(data.get("ambiguous_terms", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "report_type": self.report_type,
            "metrics": self.metrics,
            "dimensions": self.dimensions,
            "date_range": self.date_range.to_dict() if self.date_range else None,
            "filters": self.filters,
            "output_format": self.output_format,
            "purpose": self.purpose,
        }
        if self.limit is not None:
            data["limit"] = self.limit
        if self.sort_by is not None:
            data["sort_by"] = self.sort_by
        if self.ambiguous_terms:
            data["ambiguous_terms"] = self.ambiguous_terms
        return data


@dataclass(frozen=True)
class RequesterProfile:
    requester_id: str
    name: str
    email: str
    department: str
    role: str
    allowed_regions: list[str]
    allowed_countries: list[str]
    can_view_margin: bool
    can_view_customer_level: bool
    can_view_raw_extract: bool
    approval_manager: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RequesterProfile":
        return cls(
            requester_id=data["requester_id"],
            name=data["name"],
            email=data["email"],
            department=data["department"],
            role=data["role"],
            allowed_regions=list(data.get("allowed_regions", [])),
            allowed_countries=list(data.get("allowed_countries", [])),
            can_view_margin=bool(data.get("can_view_margin", False)),
            can_view_customer_level=bool(data.get("can_view_customer_level", False)),
            can_view_raw_extract=bool(data.get("can_view_raw_extract", False)),
            approval_manager=data.get("approval_manager"),
        )


@dataclass(frozen=True)
class ValidationResult:
    missing_fields: list[str] = field(default_factory=list)
    invalid_fields: list[str] = field(default_factory=list)
    reason_codes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.missing_fields and not self.invalid_fields


@dataclass(frozen=True)
class PolicyDecision:
    decision: str
    reason_codes: list[str]
    approval_required: bool = False
    approver: str | None = None
    excluded_fields: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "decision": self.decision,
            "reason_codes": self.reason_codes,
            "approval_required": self.approval_required,
            "excluded_fields": self.excluded_fields,
        }
        if self.approver is not None:
            data["approver"] = self.approver
        return data


@dataclass(frozen=True)
class ReportPlan:
    source_table: str
    group_by: list[str]
    metrics: list[str]
    filters: dict[str, Any]
    output_format: str
    limit: int | None = None
    sort_by: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "source_table": self.source_table,
            "group_by": self.group_by,
            "metrics": self.metrics,
            "filters": self.filters,
            "output_format": self.output_format,
        }
        if self.limit is not None:
            data["limit"] = self.limit
        if self.sort_by is not None:
            data["sort_by"] = self.sort_by
        return data


@dataclass(frozen=True)
class ReportOutput:
    path: str
    rows: list[dict[str, Any]]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class AuditEvent:
    request_id: str
    timestamp: str
    requester_id: str
    outcome: str
    reason_codes: list[str]
    structured_request: dict[str, Any]
    policy_decision: dict[str, Any]
    report_plan: dict[str, Any] | None = None
    output_path: str | None = None
    parent_request_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        request_id: str,
        requester_id: str,
        outcome: str,
        reason_codes: list[str],
        structured_request: dict[str, Any],
        policy_decision: dict[str, Any],
        report_plan: dict[str, Any] | None = None,
        output_path: str | None = None,
        parent_request_id: str | None = None,
    ) -> "AuditEvent":
        return cls(
            request_id=request_id,
            timestamp=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            requester_id=requester_id,
            outcome=outcome,
            reason_codes=reason_codes,
            structured_request=structured_request,
            policy_decision=policy_decision,
            report_plan=report_plan,
            output_path=output_path,
            parent_request_id=parent_request_id,
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "requester_id": self.requester_id,
            "outcome": self.outcome,
            "reason_codes": self.reason_codes,
            "structured_request": self.structured_request,
            "policy_decision": self.policy_decision,
        }
        if self.report_plan is not None:
            data["report_plan"] = self.report_plan
        if self.output_path is not None:
            data["output_path"] = self.output_path
        if self.parent_request_id is not None:
            data["parent_request_id"] = self.parent_request_id
        return data


@dataclass(frozen=True)
class ProcessResult:
    request_id: str
    outcome: str
    structured_request: StructuredRequest
    policy_decision: PolicyDecision
    response_message: str
    report_plan: ReportPlan | None
    output_path: str | None
    audit_event: AuditEvent

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "outcome": self.outcome,
            "structured_request": self.structured_request.to_dict(),
            "policy_decision": self.policy_decision.to_dict(),
            "response_message": self.response_message,
            "report_plan": self.report_plan.to_dict() if self.report_plan else None,
            "output_path": self.output_path,
            "audit_event": self.audit_event.to_dict(),
        }
