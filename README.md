# Portable Email-to-Report Agent

This project is a portfolio piece for a deployable business-agent pattern: document a messy human-operated workflow first, define the black-box contract, then build a portable agentic implementation around stable business rules and deterministic tools.

The first vertical slice is a sales-data request workflow. A requester sends an unstructured request for a report or data extract. The system interprets the request, asks for clarification where needed, checks policy, generates a deterministic report from synthetic data, drafts a response, and records an audit trail.

## Scope

This is not intended to be a general BI replacement. The first version is a bounded request-handling workflow for a small family of sales-data extracts.

The central design constraint is portability. The business logic should live in the portable core, while OpenAI, Microsoft, email, Teams, forms, and other surfaces are treated as adapters or deployment channels.

## Initial Implementation Stack

- Portable core: Python.
- Data/report tooling: CSV first, XLSX shortly after.
- Agent implementation: OpenAI Agents SDK as the first working surface.
- Microsoft story: mapping document first, with a thin Microsoft-facing adapter only if it adds portfolio value without derailing the core.
- Evaluation: fixture-driven tests with expected structured outputs and policy decisions.

## Repository Layout

```text
docs/                         Planning, workflow docs, architecture notes
samples/                      Synthetic inbound requests and expected outputs
agent_core/                   Vendor-neutral schemas, tools, policies, reports
implementations/              Runtime-specific adapters and demos
generated/                    Local generated reports and traces, ignored by Git
tests/                        Unit and evaluation tests
```

## Quickstart

Implementation is not started yet. The current milestone is repository foundation and process documentation.

Planned first commands:

```powershell
python -m venv .venv
python -m pip install -r requirements.txt
python -m pytest
```

## Design Notes

- Use the model for interpretation and structured request extraction.
- Use deterministic code for permissions, calculations, file generation, and audit logging.
- Keep vendor-specific agent configuration outside the portable business core.
- Make evaluation cases visible and repeatable.
- Be explicit when a web form would be simpler than an agent.

## Current Planning Documents

- [Backlog](docs/backlog.md)
- [Plan review](docs/plan-review.md)
- [Source chat PDF](docs/agent-demo.pdf)
