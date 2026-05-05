# Clarification Rules

## Purpose

Clarification is required when a request is potentially valid but not specific enough to fulfil safely. The workflow should ask targeted questions rather than asking the requester to start again.

The goal is to turn ambiguous human language into a complete structured request.

## When to Clarify

Clarify when any required field is missing, ambiguous, or unsafe to assume.

Common triggers:

- unclear metric
- missing date range
- relative date that cannot be resolved
- missing geography
- unsupported or vague dimension
- missing output format when it matters
- missing purpose for sensitive data
- sensitive request that may need approval
- ambiguous recipient or audience

## When Not to Clarify

Do not ask a clarification question when:

- the request is clearly unsupported
- the requester is unknown
- policy requires rejection
- the request is complete and permitted
- a safe default exists and can be stated in the response

## Safe Defaults

Safe defaults are allowed only when they do not change the substance of the request.

| Field | Safe default |
| --- | --- |
| Output format | XLSX. |
| File naming | Use report type, date range, and request ID. |
| Aggregation sort | Sort descending by primary metric. |
| Metadata | Always include request metadata. |

## Unsafe Defaults

The workflow should not silently default:

- metric when the requester says only "sales"
- country or region when multiple scopes are possible
- date range when no time period is provided
- gross margin inclusion
- customer-level detail
- raw extract versus aggregate
- approval status

## Clarification Question Style

Clarification questions should be:

- specific
- minimal
- phrased in business language
- explicit about available choices when helpful
- clear about why the answer matters

Poor:

```text
Please provide more details.
```

Better:

```text
I can prepare that. Please confirm the metric you want: revenue, units, gross margin, or all permitted metrics. Also confirm the country or region for the report.
```

## Examples

### Ambiguous Metric

Request:

```text
Can I get sales for Q4 by region?
```

Clarification:

```text
Please confirm whether "sales" means revenue, units, gross margin, or all metrics you are permitted to receive.
```

### Missing Date Range

Request:

```text
Please send UK revenue by product category.
```

Clarification:

```text
Please confirm the date range for the UK revenue by product category report.
```

### Relative Date

Request:

```text
Can I get sales for last quarter?
```

If the reference date is defined, resolve it and state the assumption. If not, clarify.

Clarification:

```text
Please confirm the reporting period you mean by "last quarter" so I use the correct dates.
```

### Missing Purpose for Sensitive Data

Request:

```text
Send me the top 20 customers by gross margin for EMEA.
```

Clarification:

```text
This request includes customer-level and margin data. Please confirm the business purpose so I can check whether approval is required.
```

### Potentially Narrowable Request

Request:

```text
Can I get global sales by customer for the year?
```

Clarification or rejection depends on profile. A useful response may offer an allowed alternative:

```text
I cannot provide global customer-level data under your current access. I can prepare an aggregated EMEA sales summary by customer segment for the same period if that would help.
```

## Clarification Output

A clarification outcome should include:

- original request reference
- structured fields already extracted
- missing fields
- ambiguous fields
- proposed questions
- audit reason code `clarification_required`

## Multi-Turn Rule

The first implementation does not need full conversation memory. It can model clarification as:

1. inbound request
2. clarification response
3. second inbound message containing the missing fields
4. merged structured request

The merge behavior should be deterministic where possible and visible in the audit event.
