# Implementation Notes

## Why Start With Documentation

The project intentionally begins with process documents and contracts. That keeps the agent from becoming the design.

The workflow has policy, approvals, clarification, output formats, and audit obligations. Those concerns need to be explicit before choosing a runtime or model.

## Why The Core Is Portable

The portable core owns:

- validation
- policy decisions
- report planning
- CSV/XLSX generation
- response drafting
- audit events
- evaluation fixtures

This means the same behavior can be surfaced through a CLI, OpenAI Agents SDK, Microsoft 365 Agents SDK, Copilot Studio custom connector, Teams bot, email worker, or a normal web form.

## Why The Agent Is Constrained

The live adapter is intentionally bounded enough that parts of it could look like a form. That is the point.

The business value is not unconstrained autonomy. The value is a natural-language intake layer over many request types that would otherwise require users to understand inconsistent UI patterns, entitlement rules, and data terminology.

The agent does interpretation. Code does controls.

## Clarification As A Terminal Outcome

Clarification does not pause an in-memory agent process. It returns a terminal `clarification_required` outcome with an audit event.

When the requester replies, that reply starts a new run, ideally linked with a parent request ID or email thread metadata. This is easier to audit and less brittle than keeping an agent session alive while waiting for a human.

## Why OpenAI Agents SDK First

The OpenAI Agents SDK gave the project a working code-first agent surface without requiring Microsoft tenant setup. The adapter demonstrates:

- model instructions
- tool calling
- provider/model configuration
- OpenAI-compatible provider support
- strict separation from portable business logic

Together AI support is useful because it proves that open-source SDK code does not automatically mean vendor-independent backend behavior. The backend still has to support the API features the adapter uses.

## Why Not Build Microsoft First

Microsoft is a credible enterprise deployment target for this workflow, but a real Microsoft implementation would involve tenant configuration, Entra app registration, channel publishing, Graph permissions, Teams/Copilot governance, and possibly SharePoint/Power Automate integration.

Without a real tenant-backed deployment, a Microsoft scaffold would not prove much. The mapping document is more honest: it identifies where Microsoft-specific work would live while preserving the portable core boundary.

## Evaluation Philosophy

The evaluation harness is deliberately strict. It compares structured fields, policy decisions, report plans, output files, and audit events against fixture expectations.

For live adapters, this catches extraction drift such as:

- over-resolving ambiguous terms
- mixing up region and country
- adding dimensions that were only filters
- returning placeholders without tool use

Model choice is treated as operational evidence. A smaller model may be cheap per token but expensive per correct, auditable case if it causes retries or manual review.

## Trade-Offs

| Choice | Benefit | Cost |
| --- | --- | --- |
| Python portable core | Fast fixture work, clear data processing, easy CLI tests | A production Microsoft shop might prefer TypeScript or hosted API wrappers |
| Deterministic report builder | Reproducible outputs and policy safety | Not a replacement for a real BI semantic model |
| Exact fixture evaluation | Clear failures and regression protection | May flag harmless wording or summarization drift |
| Thin agent adapter | Low vendor lock-in | Less impressive than a large multi-agent demo |
| Documentation-heavy packaging | Easy to review and interview around | Less visually flashy than a hosted app |

## What This Project Is Not

- not a general natural-language SQL tool
- not an autonomous analyst
- not a production email integration
- not a live Microsoft tenant deployment
- not a complete approval workflow
- not a replacement for governed BI platforms

It is a narrow, deployable pattern for turning messy business requests into controlled, auditable outputs.
