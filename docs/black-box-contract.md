# Black-Box Contract

## Purpose

The black-box contract defines the business capability independently of implementation. If this contract is stable, the workflow can be implemented with OpenAI Agents SDK, Microsoft 365 Agents SDK, Copilot Studio, a web form, a ticket workflow, or another platform without redefining the business process.

## Capability

Accept a sales-data report request, determine whether it is complete and permitted, and produce one controlled outcome:

- generate a report
- request clarification
- reject the request
- request approval

## Inputs

### Request Message

The inbound request is plain text in v1.

Required fields that may be explicit or inferred:

- requester identity
- requested report type
- requested metrics
- requested dimensions
- date range
- filters
- output format
- business purpose

### Requester Profile

The requester profile is a fixture in v1.

Fields:

- requester ID
- name
- email
- department
- role
- allowed regions
- allowed countries
- margin-data entitlement
- customer-level-data entitlement
- approval manager

### Sales Data

The sales dataset is synthetic in v1.

Expected table:

- `SalesOrders`

Expected fields:

- `order_id`
- `order_date`
- `region`
- `country`
- `customer_segment`
- `product_category`
- `product_name`
- `customer_name`
- `salesperson`
- `channel`
- `revenue`
- `gross_margin`
- `units`

### Policy Rules

Policy rules are local fixtures in v1.

They cover:

- region and country entitlement
- margin visibility
- customer-level data visibility
- maximum date range
- approval thresholds
- purpose-based restrictions

## Outputs

Exactly one primary outcome must be produced for each request.

### Generated Report

Produced when the request is complete and permitted.

Required outputs:

- report file path
- response message
- structured request
- policy decision
- report plan
- audit event

### Clarification Request

Produced when the request is potentially valid but incomplete or ambiguous.

Required outputs:

- response message with specific questions
- missing or ambiguous fields
- structured request with known fields
- audit event

### Rejection

Produced when the request is not allowed or outside supported scope.

Required outputs:

- response message explaining the reason
- policy decision or scope decision
- audit event

### Approval Required

Produced when the request may be allowed but requires human approval.

Required outputs:

- response message explaining approval requirement
- approver identity or role
- requested approval reason
- structured request
- audit event

## Supported Report Request Schema

The implementation should converge inbound language into a structure like:

```json
{
  "report_type": "sales_summary",
  "metrics": ["revenue", "gross_margin", "units"],
  "dimensions": ["region", "product_category"],
  "date_range": {
    "start": "2025-10-01",
    "end": "2025-12-31"
  },
  "filters": {
    "country": "UK"
  },
  "output_format": "xlsx",
  "purpose": "quarterly trading review"
}
```

## Allowed Actions

The workflow may:

- parse natural-language requests
- ask clarification questions
- check requester permissions
- narrow requests when policy requires it and the narrowing is explicit
- generate CSV or XLSX files from synthetic data
- include assumptions in the response
- reject unsupported requests
- mark requests as approval-required
- write audit events

## Disallowed Actions

The workflow must not:

- invent sales data
- fabricate permission decisions
- generate reports before policy checks
- include restricted fields in outputs
- silently change date ranges, metrics, dimensions, or filters
- produce arbitrary SQL over unknown schemas
- send real emails in v1
- process real customer or employee data

## Exceptions

The workflow should return a controlled exception outcome when:

- the request type is unsupported
- the requester is unknown
- the requested date range is invalid
- the requested date range is too broad
- required fields remain missing
- requested data is outside entitlement
- customer-level data requires approval
- margin data is requested by a user without margin entitlement
- the output format is unsupported

## Audit Requirements

Every request must produce an audit event containing:

- request ID
- timestamp
- requester ID
- original request text reference
- extracted structured request
- clarification fields, if any
- policy decision
- report plan, if generated
- output file path, if generated
- final outcome
- reason codes

The audit event should be platform-neutral so it can be compared across implementations.
