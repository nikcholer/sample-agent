# Implementation Stack

## Decision

The initial implementation will use Python for the portable core, with OpenAI Agents SDK as the first working agent surface.

## Rationale

Python is the most direct fit for the first vertical slice:

- Synthetic sales data can be generated and queried simply.
- CSV and XLSX report generation are straightforward.
- Fixture-driven evaluations are easy to express.
- The portable core can be kept independent of any agent runtime.
- The OpenAI implementation can wrap the core tools without owning the business logic.

The project should avoid beginning with Microsoft tenant setup, real email ingestion, or a full web application. Those are deployment concerns. The first milestone that matters is a documented and testable business capability.

## Initial Choices

| Area | Choice |
| --- | --- |
| Core runtime | Python |
| First report output | CSV, then XLSX |
| First agent surface | OpenAI Agents SDK |
| Microsoft artifact | Mapping document first |
| Evaluation style | Static fixtures with expected structured outputs and decisions |
| Inbound request format | Plain text fixtures first |

## Deferred Choices

- Microsoft 365 Agents SDK adapter.
- Copilot Studio mock-up.
- Real mailbox ingestion.
- Graph API replies.
- Teams bot surface.
- Web form comparison UI.

## Portability Rule

The portable core owns schemas, policy checks, report generation, and audit events. Agent runtimes only translate user/channel input into core calls and present the resulting outputs.
