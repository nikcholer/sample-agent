# Limitations And Extensions

## Current Limitations

- The business domain is synthetic.
- Inbound email is represented as plain text fixtures.
- The core uses fixture data rather than a production warehouse or BI semantic model.
- Report generation is intentionally simple and deterministic.
- Clarification replies are modeled as new runs, but a full thread-correlation implementation is not built.
- The OpenAI Agents SDK adapter has been tested live, but live behavior still depends on the chosen provider and model.
- Microsoft 365 deployment is documented as architecture, not implemented against a tenant.
- Approval-required outcomes stop at routing guidance; they do not yet trigger Power Automate, ServiceNow, Jira, or another approval system.
- Cost tracking is not automated.
- The evaluation harness checks workbook structure, but not every cell of every XLSX output.

## Extension Ideas

### Production Email Worker

- Parse `.eml` or Graph message payloads.
- Preserve thread IDs and request IDs.
- Send replies through Graph or an SMTP relay.
- Attach or link generated reports.

### Hosted Portable Core API

- Wrap the core as an HTTP API.
- Add authentication and tenant-aware requester resolution.
- Keep schemas stable so OpenAI, Microsoft, and web adapters can call the same service.

### Microsoft 365 Adapter

- Use Microsoft 365 Agents SDK/custom engine as the preferred implementation path.
- Resolve user identity through Entra ID or Graph.
- Store generated reports in SharePoint or OneDrive.
- Route approvals through Power Automate.
- Keep Copilot Studio as a possible business-facing surface, not the owner of business logic.

### Richer Evaluation

- Add repeated live-model runs and variance reporting.
- Add cost-per-correct-case tracking.
- Add deeper CSV/XLSX content checks.
- Add response-quality rubrics for user-facing wording.
- Compare OpenAI and OpenAI-compatible providers across the same fixture set.

### Broader Request Types

- Inventory status requests.
- Finance variance reports.
- Customer account summaries.
- HR policy lookup plus governed action routing.
- Procurement spend extracts.

### Form Comparison

Build a small form-based intake surface to show the trade-off directly:

- forms are excellent for narrow, stable request patterns
- agent intake is more useful when request types and terminology vary
- both can call the same portable core

## Production Readiness Gap

Before production, the project would need:

- real identity and access control
- data-source integration
- secrets management
- observability and alerting
- privacy review
- compliance retention rules
- approval workflow implementation
- load and failure-mode testing
- human support path for ambiguous or disputed results
