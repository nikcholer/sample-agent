from __future__ import annotations

from typing import Any

from agent_core.models import PolicyDecision, RequesterProfile, StructuredRequest
from agent_core.validation import validate_request


def evaluate_policy(
    request: StructuredRequest,
    requester: RequesterProfile | None,
    policy_rules: dict[str, Any],
) -> PolicyDecision:
    if requester is None:
        return PolicyDecision(
            decision="rejected",
            reason_codes=["unknown_requester"],
        )

    validation = validate_request(request, policy_rules)
    if validation.invalid_fields:
        if "unsupported_request_type" in validation.reason_codes:
            return PolicyDecision(
                decision="rejected",
                reason_codes=["unsupported_request_type"],
            )
        return PolicyDecision(
            decision="clarification_required",
            reason_codes=validation.reason_codes or ["clarification_required"],
        )

    if validation.missing_fields:
        return PolicyDecision(
            decision="deferred",
            reason_codes=["clarification_required"],
        )

    reason_codes: list[str] = []
    excluded_fields: list[str] = []

    region_violation = _region_violation(request, requester)
    country_violation = _country_violation(request, requester)
    if region_violation:
        reason_codes.append("region_not_permitted")
    if country_violation or (region_violation and "*" not in requester.allowed_countries):
        reason_codes.append("country_not_permitted")

    margin_violation = "gross_margin" in request.metrics and not requester.can_view_margin
    if margin_violation:
        reason_codes.append("margin_not_permitted")
        excluded_fields.append("gross_margin")

    customer_level = "customer_name" in request.dimensions
    raw_extract = request.report_type == "filtered_raw_extract"

    if region_violation or country_violation:
        if customer_level and not requester.can_view_customer_level:
            reason_codes.append("customer_level_not_permitted")
            excluded_fields.append("customer_name")
        if raw_extract and not requester.can_view_raw_extract:
            reason_codes.append("raw_extract_not_permitted")
        return PolicyDecision(
            decision="rejected",
            reason_codes=_dedupe(reason_codes),
            approval_required=False,
            excluded_fields=_dedupe(excluded_fields),
        )

    if customer_level and not requester.can_view_customer_level:
        return PolicyDecision(
            decision="approval_required",
            reason_codes=["customer_level_approval_required"],
            approval_required=True,
            approver=requester.approval_manager,
            excluded_fields=[],
        )

    if raw_extract and not requester.can_view_raw_extract:
        return PolicyDecision(
            decision="approval_required",
            reason_codes=["raw_extract_approval_required"],
            approval_required=True,
            approver=requester.approval_manager,
            excluded_fields=[],
        )

    if margin_violation:
        return PolicyDecision(
            decision="clarification_required",
            reason_codes=["margin_not_permitted", "clarification_required"],
            approval_required=False,
            excluded_fields=_dedupe(excluded_fields),
        )

    return PolicyDecision(
        decision="allowed",
        reason_codes=["allowed"],
        approval_required=False,
        excluded_fields=[],
    )


def _region_violation(
    request: StructuredRequest,
    requester: RequesterProfile,
) -> bool:
    requested_regions = request.filters.get("region", [])
    if not requested_regions:
        return False
    if "*" in requester.allowed_regions:
        return False
    return any(region not in requester.allowed_regions for region in requested_regions)


def _country_violation(
    request: StructuredRequest,
    requester: RequesterProfile,
) -> bool:
    requested_countries = request.filters.get("country", [])
    if not requested_countries:
        return False
    if "*" in requester.allowed_countries:
        return False
    return any(country not in requester.allowed_countries for country in requested_countries)


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
