from __future__ import annotations

from datetime import date
from typing import Any

from agent_core.models import StructuredRequest, ValidationResult


def validate_request(
    request: StructuredRequest,
    policy_rules: dict[str, Any],
) -> ValidationResult:
    missing: list[str] = []
    invalid: list[str] = []
    reason_codes: list[str] = []

    if request.report_type not in policy_rules["supported_report_types"]:
        invalid.append("report_type")
        reason_codes.append("unsupported_request_type")
        return ValidationResult(missing, invalid, reason_codes)

    if not request.metrics:
        missing.append("metrics")
    else:
        supported_metrics = set(policy_rules["metrics"])
        invalid.extend(
            f"metrics.{metric}"
            for metric in request.metrics
            if metric not in supported_metrics
        )

    if request.report_type != "filtered_raw_extract" and not request.dimensions:
        missing.append("dimensions")

    supported_dimensions = set(policy_rules["dimensions"])
    invalid.extend(
        f"dimensions.{dimension}"
        for dimension in request.dimensions
        if dimension not in supported_dimensions
    )

    if request.date_range is None:
        missing.append("date_range")
    else:
        try:
            start = date.fromisoformat(request.date_range.start)
            end = date.fromisoformat(request.date_range.end)
            if start > end:
                invalid.append("date_range")
                reason_codes.append("invalid_date_range")
            elif (end - start).days > policy_rules["max_date_range_days"]:
                invalid.append("date_range")
                reason_codes.append("date_range_too_broad")
        except ValueError:
            invalid.append("date_range")
            reason_codes.append("invalid_date_range")

    if request.output_format is not None:
        if request.output_format not in policy_rules["supported_output_formats"]:
            invalid.append("output_format")

    if _requires_geography(request) and not _has_geography(request):
        missing.append("geography")

    if missing and "clarification_required" not in reason_codes:
        reason_codes.append("clarification_required")

    return ValidationResult(missing, invalid, reason_codes)


def _requires_geography(request: StructuredRequest) -> bool:
    return request.report_type in {
        "sales_summary",
        "product_breakdown",
        "monthly_trend",
        "top_n",
        "filtered_raw_extract",
    }


def _has_geography(request: StructuredRequest) -> bool:
    return bool(request.filters.get("country") or request.filters.get("region"))
