# Backlog: Portable Email-to-Report Agent

## Product thesis

This project demonstrates a deployable business-agent pattern: document a messy human-operated request process, define the black-box contract, then implement one portable agentic capability that can be surfaced through OpenAI, Microsoft, email, Teams, forms, or other channels.

The first vertical slice is a sales-data request workflow. Requesters send unstructured requests for report extracts. The system interprets the request, asks for clarification where needed, checks policy, generates a deterministic CSV/XLSX report from synthetic data, drafts a response, and records an audit trail.

## Milestone 0: Repository foundation

Goal: make the project navigable and ready for implementation.

- [x] Move planning artifacts into `docs/`.
- [x] Initialize Git repository.
- [x] Create private GitHub remote.
- [x] Add project `README.md` with thesis, scope, and quickstart placeholder.
- [x] Add `.gitignore` for Python, Node, generated reports, local env files, and temporary traces.
- [x] Decide initial implementation stack.
- [x] Create top-level folders for docs, samples, core logic, implementations, and generated outputs.

## Milestone 1: Process documentation

Goal: document the business workflow before agentifying it.

- [x] Write `docs/process-overview.md`.
- [x] Write `docs/current-human-workflow.md`.
- [x] Write `docs/black-box-contract.md`.
- [x] Write `docs/supported-request-types.md`.
- [x] Write `docs/policy-and-permissions.md`.
- [x] Write `docs/clarification-rules.md`.
- [x] Write `docs/evaluation-plan.md`.
- [x] Update `docs/plan-review.md` as the framing note rather than the active plan.

Acceptance criteria:

- A reader can understand the current manual process without reading code.
- Inputs, outputs, rules, exceptions, and audit requirements are explicit.
- The documentation explains when a web form would be sufficient and when an agentic intake layer is justified.

## Milestone 2: Synthetic business domain

Goal: create a realistic but safe data and policy environment.

- [x] Define `SalesOrders` schema.
- [x] Generate synthetic sales dataset.
- [x] Create requester profiles with roles, regions, and entitlements.
- [x] Define policy fixtures for margin access, regional access, raw extract approval, and customer-level restrictions.
- [x] Add sample inbound requests covering clear, ambiguous, unauthorized, and approval-required cases.
- [x] Add expected structured outputs for each sample request.

Acceptance criteria:

- The dataset is plausible enough for demos but contains no real data.
- Every sample request has a known expected decision.
- Data and permissions are versioned as fixtures.

## Milestone 3: Portable agent core

Goal: build vendor-neutral request processing primitives.

- [x] Define structured request schema.
- [x] Define policy decision schema.
- [x] Define report plan schema.
- [x] Define audit event schema.
- [x] Implement request validation and completeness checks.
- [x] Implement deterministic policy checks.
- [x] Implement deterministic report query/build logic.
- [x] Implement CSV output.
- [x] Implement XLSX output with summary, data, and request metadata tabs.
- [x] Implement response drafting from structured outcomes.
- [x] Implement audit log generation.

Acceptance criteria:

- Core logic can run without any agent SDK.
- Calculations and file generation are deterministic.
- Policy checks are testable without model calls.

## Milestone 4: OpenAI Agents SDK implementation

Goal: show a working code-first agent implementation.

- [x] Create OpenAI implementation folder.
- [x] Define the intake agent instructions.
- [x] Expose core operations as tools.
- [x] Use structured outputs for extracted request intent.
- [x] Implement clarification path.
- [x] Implement approved-report path.
- [x] Implement rejection path.
- [x] Implement approval-required path.
- [x] Capture traces or transcript examples.

Acceptance criteria:

- The agent can process fixture requests end to end.
- The model interprets language, while tools perform policy, data, and file work.
- Outputs include structured request JSON, report file, response text, and audit log.

## Milestone 5: Evaluation harness

Goal: make the demo credible as an engineered workflow, not a prompt trick.

- [x] Define evaluation cases from sample inbound requests.
- [x] Check extraction accuracy against expected structured request fields.
- [x] Check policy decision accuracy.
- [x] Check whether clarification is requested when required.
- [x] Check report files contain expected filters, dimensions, and metrics.
- [x] Check audit events are created.
- [x] Add a simple command to run the evaluation set.
- [x] Record provider and model for each live evaluation run.
- [x] Document when repeated extraction failures should trigger live model comparison.
- [x] Document known limitations and failure cases.

Acceptance criteria:

- Evaluation can be run repeatably.
- Failures are visible and actionable.
- Model choice can be evaluated by observed pass rate and reliability, not preference.
- At least one example exists for success, clarification, rejection, and approval-required outcomes.

## Milestone 6: Microsoft and portability mapping

Goal: demonstrate avoidance of vendor lock-in and practical Microsoft awareness.

- [x] Write `docs/microsoft-copilot-mapping.md`.
- [x] Map portable core concepts to Copilot Studio concepts.
- [x] Map portable core concepts to Microsoft 365 Agents SDK/custom engine agent concepts.
- [x] Identify which components would live in Graph, Power Automate, Dataverse, Fabric, or a custom API.
- [x] Describe edge lock-in explicitly: auth, mailbox, Teams, tenant governance, approvals, publishing, and monitoring.
- [x] Sketch thin-adapter architecture for a Microsoft-facing implementation.
- [x] Decide whether to build a small Microsoft 365 Agents SDK adapter or keep this as documented architecture in v1.

Acceptance criteria:

- The Microsoft story is specific enough for an interview discussion.
- Business logic remains outside Microsoft-specific configuration.
- The repo can explain what would change between OpenAI and Microsoft deployments.

## Milestone 7: Portfolio packaging

Goal: make the project easy to inspect and discuss.

- [ ] Write final `README.md`.
- [ ] Add architecture diagram.
- [ ] Add before/after workflow diagram.
- [ ] Add demo script.
- [ ] Add generated example reports.
- [ ] Add anonymized trace/audit examples.
- [ ] Add short implementation notes explaining design trade-offs.
- [ ] Record short demo video or GIF.
- [ ] Add final limitations and extension ideas.

Acceptance criteria:

- A reviewer can understand the project in five minutes.
- A technical interviewer can inspect the implementation and tests.
- The project clearly avoids claiming to be a general BI replacement.

## Open design decisions

- Which runtime should be used for the portable core: Python, TypeScript, or both?
- Should the first report output be CSV-only, or should XLSX be included from the start?
- Should evaluation use static fixture expectations only, or also model-graded qualitative checks?
- What pass-rate or repeated-failure threshold should trigger trying a stronger model in a real deployment?
- Should the first Microsoft artifact be a mapping document, a Copilot Studio mock-up, or a Microsoft 365 Agents SDK adapter?
- Should inbound email be simulated as plain text, `.eml`, or JSON-wrapped messages?

## Parking lot

- Real mailbox ingestion.
- Graph API outbound replies.
- Teams bot surface.
- Power Automate approval flow.
- Power BI/Fabric semantic model integration.
- Natural-language SQL over arbitrary schemas.
- Multi-agent decomposition.
- Web form comparison UI.
- Hosted demo.
