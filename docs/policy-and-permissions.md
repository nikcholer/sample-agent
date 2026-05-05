# Policy and Permissions

## Purpose

The workflow must enforce access and sensitivity rules before generating any report. Policy checks are deterministic and should not depend on model judgment.

The model may identify what is being requested. It must not decide whether the requester is allowed to receive it.

## Policy Inputs

Policy checks use:

- requester profile
- structured report request
- requested metrics
- requested dimensions
- requested filters
- requested date range
- requested output format
- stated business purpose

## Requester Profile

Requester profiles are fixtures in v1.

Example shape:

```json
{
  "requester_id": "u-1027",
  "name": "Amira Shah",
  "email": "amira.shah@example.test",
  "department": "Sales",
  "role": "Regional Sales Manager",
  "allowed_regions": ["EMEA"],
  "allowed_countries": ["UK", "Ireland"],
  "can_view_margin": true,
  "can_view_customer_level": false,
  "approval_manager": "u-2001"
}
```

## Core Rules

| Rule | Behavior |
| --- | --- |
| Unknown requester | Reject. |
| Region outside entitlement | Reject or narrow only if the requester explicitly accepts a narrower allowed scope. |
| Country outside entitlement | Reject. |
| Gross margin requested without entitlement | Remove only if explicitly offered and accepted; otherwise clarify/reject. |
| Customer-level data without entitlement | Approval required or reject, depending on request type. |
| Raw extract requested | Approval required unless requester has raw-extract entitlement. |
| Date range over maximum | Ask requester to narrow the range. |
| Unsupported metric or dimension | Reject as unsupported. |
| Missing purpose for sensitive request | Ask for purpose before policy decision completes. |

## Sensitivity Levels

| Level | Examples | Default outcome |
| --- | --- | --- |
| Low | Aggregated revenue by region or product category | Allowed if requester has region/country access. |
| Medium | Gross margin, salesperson-level data, longer date ranges | Allowed only with entitlement or clarification. |
| High | Customer-level detail, raw extracts, broad multi-region pulls | Approval required or rejected. |

## Approval Required

The workflow should mark a request as approval-required when:

- customer-level data is requested without direct entitlement
- a raw extract is requested
- the date range is broad and the data is sensitive
- the requester asks for data outside their usual operational scope but may have a valid business reason
- policy explicitly says manager approval can override the restriction

Approval-required is not the same as allowed. No report should be generated until approval is recorded.

## Rejection

The workflow should reject when:

- the requester is unknown
- the request is unsupported
- the requested scope is clearly outside entitlement
- the request asks for real personal data
- required approval is impossible or not defined
- the request conflicts with a non-overridable rule

Rejections should explain the reason briefly and, where possible, suggest a supported alternative.

## Narrowing

The workflow may suggest a narrower report, but must not silently narrow a request.

Example:

```text
I cannot provide global customer-level data. I can prepare an aggregated UK revenue summary by customer segment if that would meet your need.
```

The narrowed report should only be generated after the requester accepts the narrower scope, unless the original request clearly specified an allowed fallback.

## Report Output Controls

Generated reports should include:

- only permitted fields
- filters used
- date range used
- metrics used
- dimensions used
- a metadata tab or sidecar metadata file

Reports should not include:

- hidden restricted columns
- raw rows when the approved output is aggregate-only
- margin fields when margin is not permitted
- customer names when customer-level detail is not permitted

## Audit Reason Codes

Suggested reason codes:

- `allowed`
- `clarification_required`
- `unknown_requester`
- `unsupported_request_type`
- `region_not_permitted`
- `country_not_permitted`
- `margin_not_permitted`
- `customer_level_approval_required`
- `customer_level_not_permitted`
- `raw_extract_approval_required`
- `raw_extract_not_permitted`
- `date_range_too_broad`
- `missing_business_purpose`
- `invalid_date_range`

These codes should appear in evaluation fixtures and audit events.
