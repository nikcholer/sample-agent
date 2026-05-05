# Evaluation Plan

## Purpose

Evaluation shows that the workflow is engineered rather than merely prompted. The same evaluation cases should be reusable against the portable core, the OpenAI implementation, and any future Microsoft-facing adapter.

## Evaluation Scope

The first evaluation set checks:

- request extraction
- completeness decisions
- policy decisions
- report-plan generation
- report-file contents
- response drafting
- audit-event creation

It does not evaluate production email delivery, real identity systems, or live BI integrations.

## Test Case Categories

### Clear Approved Request

The request is complete and permitted.

Expected outcome:

- structured request extracted correctly
- policy decision `allowed`
- report generated
- response includes filters, metrics, dimensions, and date range
- audit event created

### Clarification Required

The request is potentially valid but missing required information.

Expected outcome:

- known fields extracted
- missing fields identified
- no report generated
- targeted clarification question produced
- audit event created

### Rejected Request

The request is unsupported or not permitted.

Expected outcome:

- no report generated
- rejection reason code recorded
- response explains the reason
- audit event created

### Approval Required

The request may be valid but needs human approval.

Expected outcome:

- no report generated
- approver or approval role identified
- approval reason recorded
- response explains next step
- audit event created

### Safe Default Applied

The request is complete except for a safe default such as output format.

Expected outcome:

- default applied
- default stated in response or metadata
- report generated if policy allows
- audit event created

## Initial Evaluation Cases

| ID | Request summary | Expected outcome |
| --- | --- | --- |
| `case-001` | Q4 2025 UK revenue by region as Excel | Generate report |
| `case-002` | "Sales for last quarter by region" | Clarify metric and date scope if reference period unavailable |
| `case-003` | UK revenue and gross margin by product category from requester with margin access | Generate report |
| `case-004` | Gross margin requested by requester without margin access | Clarify allowed alternative or reject |
| `case-005` | Top 20 customers by revenue | Approval required |
| `case-006` | Global customer-level raw extract from regional requester | Reject or approval required depending on fixture policy |
| `case-007` | Marketing attribution dashboard | Reject unsupported |
| `case-008` | Monthly EMEA revenue trend for 2025 | Generate report if requester has EMEA access |

## Extraction Checks

For each case, compare extracted fields with expected values:

- `report_type`
- `metrics`
- `dimensions`
- `date_range`
- `filters`
- `output_format`
- `purpose`

Extraction should be exact for controlled values and normalized dates.

## Policy Checks

For each case, compare:

- policy outcome
- reason codes
- approval requirement
- allowed fields
- excluded fields
- permitted scope

The policy evaluator should be callable without model involvement.

## Report Checks

Generated reports should be checked for:

- file exists
- expected format
- expected sheet names for XLSX
- expected columns
- no restricted columns
- filters reflected in metadata
- date range reflected in metadata
- row count or aggregate totals match deterministic fixture expectations

## Response Checks

Responses should be checked for:

- outcome clarity
- assumptions stated
- filters stated
- exclusions stated
- next action stated when clarification or approval is needed
- no unsupported claims

Response checks may begin as simple text assertions and later become rubric-based review if useful.

## Audit Checks

Each case must produce an audit event with:

- request ID
- timestamp
- requester ID
- outcome
- reason codes
- structured request
- policy decision
- generated file path, if any

Audit events should be JSON so they can be compared across implementations.

## Pass/Fail Standard

A case passes when:

- the primary outcome matches expectation
- required structured fields match expectation
- policy reason codes match expectation
- no disallowed data appears in outputs
- audit event is present

A case fails when:

- a report is generated before policy is satisfied
- restricted data appears
- an unsupported request is fulfilled
- the clarification question is too vague to move the process forward
- the output cannot be reproduced from fixtures

## Reporting Results

The evaluation runner should eventually produce:

- case ID
- expected outcome
- actual outcome
- pass/fail
- mismatched fields
- generated output paths
- audit event path

The first implementation can output this as terminal text and a JSON summary.
