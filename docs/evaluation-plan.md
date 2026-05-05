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
- clarification response asks the requester to reply in the same thread or include the request reference
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
| `case-002` | "Sales for last quarter by region" | Clarify metric and geography; resolve last quarter against the fixture reference date |
| `case-003` | UK revenue and gross margin by product category from requester with margin access | Generate report |
| `case-004` | Gross margin requested by requester without margin access | Clarify allowed alternative or reject |
| `case-005` | Top 20 customers by revenue | Approval required |
| `case-006` | Global customer-level raw extract from regional requester | Reject as outside entitlement and not approvable in the requested scope |
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
- thread or request-reference instruction when clarification is needed
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
- a clarification response gives no way to correlate the reply with the original request
- the output cannot be reproduced from fixtures

## Model Selection Standard

Model choice is part of the evaluation, not a one-time configuration decision. The default model for a provider should be treated as a cost-conscious starting point, not a guarantee that it is capable enough for the workflow.

Repeated live-adapter failures should trigger a model comparison rather than indefinite prompt tuning. Examples of repeated failures include:

- the same extraction field fails in multiple runs after instructions are clear
- a geography filter is repeatedly misclassified as a dimension
- ambiguous terms are repeatedly over-resolved instead of sent for clarification
- the model omits the required tool call or returns placeholders
- provider errors indicate incomplete support for required tool-calling behavior

A stronger or different model is justified when it materially improves:

- fixture pass rate
- stability across repeated runs
- correct tool-call argument construction
- adherence to clarification boundaries
- cost per successful case, not just cost per token

The portfolio story should be explicit about this trade-off: a small model may be cheaper per call but more expensive operationally if it causes retries, manual review, or incorrect reports. The exact threshold for trying a stronger model is a deployment decision rather than something this synthetic example needs to settle.

## Reporting Results

The evaluation runner produces:

- case ID
- expected outcome
- actual outcome
- pass/fail
- mismatched fields
- model and provider used
- repeat number or run ID
- generated output paths
- audit event path

Run the deterministic portable-core baseline:

```powershell
python tools\evaluate_cases.py --implementation core
```

Run the live OpenAI Agents SDK adapter when API credentials are configured:

```powershell
python tools\evaluate_cases.py --implementation openai
```

Compare a specific model:

```powershell
python tools\evaluate_cases.py --implementation openai --model "provider/model-name"
```

Write a JSON summary for later comparison:

```powershell
python tools\evaluate_cases.py --implementation core --json-out generated\evaluation\core-summary.json
```

The first implementation outputs terminal text by default and can also emit JSON with `--json`.
