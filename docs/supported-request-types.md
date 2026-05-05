# Supported Request Types

## Scope

The first version supports a small family of sales-data requests. It is intentionally narrow so the process can be evaluated clearly.

The supported request types are:

- sales summary
- product breakdown
- monthly trend
- top N ranking
- filtered raw extract

Requests outside these shapes should be rejected or deferred with a clear explanation.

## Common Fields

All request types use the same core fields:

| Field | Required | Notes |
| --- | --- | --- |
| `report_type` | Yes | One of the supported request types. |
| `metrics` | Yes | Revenue, gross margin, units, or allowed combinations. |
| `dimensions` | Depends | Required for summaries, breakdowns, and trends. |
| `date_range` | Yes | Explicit dates or a resolvable reporting period. |
| `filters` | Optional | Country, region, product category, channel, segment. |
| `output_format` | Optional | Defaults to XLSX for portfolio demos unless CSV is requested. |
| `purpose` | Usually | Required for sensitive or approval-prone requests. |

## Sales Summary

Aggregated sales metrics by one or more dimensions.

Examples:

```text
Please send Q4 2025 UK revenue and gross margin by region and product category as Excel.
```

```text
Can I have 2025 sales by region for the annual planning pack?
```

Allowed dimensions:

- region
- country
- product category
- channel
- customer segment

Allowed metrics:

- revenue
- gross margin, subject to entitlement
- units

## Product Breakdown

Aggregated sales by product category or product name.

Examples:

```text
I need UK revenue by product category for January to March 2026.
```

```text
Can you break down Q1 sales by product line and channel?
```

Product-name level detail may be allowed, but customer-level detail is more restricted.

## Monthly Trend

Aggregated sales over time, usually month by month.

Examples:

```text
Please send monthly revenue and units for EMEA in 2025.
```

```text
I need a trend of UK sales by month for the last two quarters.
```

The workflow must resolve relative periods such as "last quarter" against a defined reference date before generating the report.

## Top N Ranking

Top products or customers by an allowed metric.

Examples:

```text
Can I get the top 10 UK products by revenue for Q4 2025?
```

```text
Please send our top 20 customers by revenue this year.
```

Top customer reports may require approval or additional entitlement because they expose customer-level information.

## Filtered Raw Extract

A row-level extract for a permitted scope.

Examples:

```text
Please send the raw UK online sales rows for March 2026.
```

```text
I need all EMEA enterprise orders for Q1 so my team can reconcile the account list.
```

Raw extracts are sensitive and may require approval even when the requester has regional access.

## Unsupported Requests

The workflow should reject or defer:

- forecasts
- dashboards
- charts only
- arbitrary SQL
- joins across unknown datasets
- customer profitability analysis outside the synthetic schema
- non-sales datasets
- requests for real personal data
- requests with no clear reporting purpose when sensitive fields are involved

## Defaults

Defaults may be used only when they are safe and explicit in the response.

Suggested defaults:

| Missing field | Default behavior |
| --- | --- |
| Output format | Use XLSX. |
| Metric "sales" | Ask whether the requester means revenue, units, margin, or all allowed metrics. |
| Date range | Ask for clarification unless the phrase maps to a defined reporting period. |
| Country or region | Use requester entitlement only if the request clearly implies their own area; otherwise ask. |
| Purpose | Ask when requesting margin, customer-level detail, broad date ranges, or raw extracts. |

## Example Outcomes

| Request | Outcome |
| --- | --- |
| "Send Q4 2025 UK revenue by region as Excel." | Generate report if requester has UK access. |
| "Can I get sales for last quarter?" | Clarify metric, geography, and output shape. |
| "Send all customer-level revenue globally." | Reject or require approval depending on requester profile. |
| "Top 10 UK products by revenue for Q4." | Generate report if requester has UK access. |
| "Build a dashboard comparing marketing attribution." | Reject as unsupported. |
