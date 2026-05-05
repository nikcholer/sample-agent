# OpenAI Agent Transcript Example

This is an expected transcript shape for the OpenAI Agents SDK adapter. It is not a captured live OpenAI trace; it documents the interaction pattern that a live trace should show once `openai-agents` and `OPENAI_API_KEY` are configured.

## Case

`case-002`: ambiguous request requiring clarification.

Inbound message:

```text
From: Ben Carter <ben.carter@example.test>
Subject: Sales for last quarter

Hi,

Can I get sales for last quarter by region? Need it for a Monday deck.

Thanks,
Ben
```

## Expected Agent/Tool Flow

```text
User input
  -> Intake agent reads email text
  -> Intake agent extracts requester email: ben.carter@example.test
  -> Intake agent extracts partial structured request
  -> Intake agent calls process_sales_report_request
  -> Tool resolves requester profile: u-1002
  -> Portable core validates request
  -> Portable core returns clarification_required
  -> Intake agent returns structured final output
```

## Expected Tool Input

```json
{
  "request_id": "case-002",
  "requester_email": "ben.carter@example.test",
  "structured_request": {
    "report_type": "sales_summary",
    "metrics": [],
    "ambiguous_terms": {
      "sales": ["revenue", "units", "gross_margin"]
    },
    "dimensions": ["region"],
    "date_range": {
      "start": "2026-01-01",
      "end": "2026-03-31",
      "label": "last quarter",
      "reference_date": "2026-05-05"
    },
    "filters": {},
    "output_format": null,
    "purpose": "Monday deck"
  }
}
```

## Expected Final Output

```json
{
  "request_id": "case-002",
  "requester_id": "u-1002",
  "outcome": "clarification_required",
  "response_message": "I can continue, but need clarification before generating a report. Please reply in this email thread and confirm whether sales means revenue, units, gross margin, or all permitted metrics; and confirm the country or region for the report.",
  "output_path": null
}
```

## What A Live SDK Trace Should Show

The OpenAI Agents SDK trace should show:

- one `Runner` run for the request
- one intake-agent turn
- one function-tool call to `process_sales_report_request`
- no report-generation tool inside the model layer
- final structured output matching the tool result

This confirms the intended boundary: the model interprets; the portable core validates, decides, audits, and generates outputs.
