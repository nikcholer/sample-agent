# Plan Review: Portable Email-to-Report Agent

## Overall verdict

This is a strong portfolio piece. The proposed "email requesting a custom sales report" workflow is familiar, business-relevant, and agent-shaped without feeling contrived. It demonstrates the right things for deployable business agents: intake from messy human language, clarification, policy checks, deterministic data work, file generation, auditability, and a controlled handoff boundary.

The idea is suitable if it is framed as a bounded request-handling workflow, not as "BI by email" or a general natural-language analytics platform. The best title-level positioning is something like:

> Portable Email-to-Report Agent: upgrading a human-operated sales-data request workflow without locking the business logic into one agent platform.

## Complexity assessment

Complexity rating: medium-high, but portfolio-appropriate.

The concept has enough moving parts to show real architecture, but it can still be delivered from home if the first version is deliberately constrained.

| Area | Complexity | Notes |
| --- | --- | --- |
| Request understanding | Medium | The LLM extracts structured intent from unstructured email. Keep supported report types narrow. |
| Clarification loop | Medium | Valuable for showing agentic behavior. Implement with simple missing-field rules first. |
| Policy checks | Medium | Mock roles, regions, margin entitlement, and customer-level data restrictions. This adds business realism. |
| Data querying | Low-medium | Use deterministic code against a synthetic dataset. Do not let the model invent calculations. |
| File generation | Medium | CSV is easy; XLSX with summary, data, and metadata tabs is more impressive. |
| Evaluation | Medium | A small but explicit test set will greatly improve credibility. |
| OpenAI Agents SDK implementation | Medium | Good fit for a code-first implementation. |
| Microsoft/Copilot implementation | Medium-high | Good for architecture mapping, but real publishing may depend on tenant/licensing/access. |
| Real email integration | High | Avoid in v1. Simulate inbound emails as `.txt`, `.eml`, or JSON fixtures. |
| Real Microsoft 365/Fabric/Power BI integration | High | Avoid in v1. Document the mapping instead. |

The dangerous version is a general agent that can answer arbitrary business intelligence questions over arbitrary schemas. The good version is a request workflow for a small family of sales-data extracts.

## Why the workflow is suitable

This workflow is suitable because it starts from a process that businesses already understand. Someone emails an analyst, the analyst interprets the request, asks follow-up questions, checks access, filters data, exports a spreadsheet, and replies. That is a clean black-box replacement story: the input and output surfaces can remain the same while the internal implementation changes.

It also avoids the common portfolio weakness of "I wrapped a chatbot around some data." The agent is not valuable because it chats; it is valuable because it completes a controlled business process with explicit rules, outputs, and evidence.

The strongest engineering message is:

> LLMs interpret requests and produce structured plans. Deterministic tools perform policy checks, calculations, file generation, and logging.

That distinction makes the project feel deployable rather than demo-only.

## The web-form objection

There is a fair objection: if the MVP is constrained enough, it may look like the request should simply be a web form. That does not invalidate the agent idea, but it does affect how the portfolio should explain it.

The right claim is not that email is always better than a form. For a single narrow request type, a form may be cheaper, more predictable, and easier to govern. The stronger business argument is that large organizations often accumulate dozens of request paths across different BI tools, ticketing systems, SharePoint forms, spreadsheets, email aliases, Teams chats, and department-specific workflows. The agentic layer becomes valuable when it can normalize that messy intake landscape into a common request contract.

So the MVP should be presented as one vertical slice of a broader intake-normalization pattern:

```text
Email / Teams / form / ticket / spreadsheet row
   -> request interpretation
   -> common structured request schema
   -> policy and entitlement checks
   -> deterministic fulfilment tools
   -> auditable response
```

That framing makes the constrained version more credible. The project can openly say:

> For this single report type, a web form would be a valid implementation. The agentic value appears when the same intake process has to support many related request types, ambiguous language, missing context, legacy tools, and inconsistent departmental UX.

This is also a useful anti-hype point. It shows that the project is not pretending every form should become a chatbot. It is demonstrating how an organization can move from scattered human-operated interfaces toward a documented, testable request-processing capability.

## Recommended MVP boundary

Build the first version around a synthetic `SalesOrders` dataset with fields such as:

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

Support only these report shapes:

- Sales summary by region
- Sales summary by product category
- Monthly sales trend
- Top N products or customers
- Filtered raw extract, subject to permission

Support only these controls:

- Requester role
- Region entitlement
- Margin-data entitlement
- Customer-level data restriction
- Maximum date range
- Approval required for sensitive extracts

Support only these interactions:

- Produce report
- Ask for clarification
- Reject with explanation
- Escalate for approval

That is enough to be interesting. Anything beyond this should be treated as a later extension.

## Documentation-first plan

The project should lead with process documentation before implementation. That is the main differentiator.

Recommended repository structure:

```text
/docs
  process-overview.md
  current-human-workflow.md
  black-box-contract.md
  supported-request-types.md
  policy-and-permissions.md
  clarification-rules.md
  evaluation-plan.md
  microsoft-copilot-mapping.md
/samples
  inbound-requests/
  expected-outputs/
  generated-reports/
  traces/
/agent-core
  schemas/
  tools/
  policies/
  report-generation/
/openai-agents-sdk
  implementation/
/microsoft-facing
  copilot-studio-notes/
  m365-agents-sdk-adapter/
```

The most important documents are:

- `black-box-contract.md`: inputs, outputs, allowed actions, unavailable actions, exceptions, and audit requirements.
- `current-human-workflow.md`: what the analyst currently does manually.
- `policy-and-permissions.md`: the rules that constrain the agent.
- `evaluation-plan.md`: test cases, expected decisions, expected files, and pass/fail criteria.
- `microsoft-copilot-mapping.md`: how the same capability would map into Copilot Studio, Microsoft 365 Agents SDK, Power Automate, Graph, Fabric, or a custom API.

This makes the portfolio piece about deployable process design, not just prompt craft.

## Vendor lock-in review

The plan is good on lock-in if the agent capability is kept behind stable contracts.

Recommended boundaries:

- Keep the business capability in `agent-core`, not inside Copilot Studio topics or a vendor-specific agent canvas.
- Define the structured request schema independently of any SDK.
- Treat OpenAI Agents SDK, Copilot Studio, Teams, email, or web chat as adapters/channels.
- Put policy checks, report generation, and audit logging in deterministic services or modules.
- Use test fixtures and evaluation cases that can be run against any implementation.
- Store traces in a platform-neutral shape, even if one implementation also emits vendor-native traces.
- Keep Microsoft-specific objects in a separate mapping or wrapper layer.

A good architecture sentence:

> The workflow is portable because the black-box contract, policy rules, test cases, and report-generation tools are independent of the agent runtime. Vendor-specific agents are deployment surfaces, not the source of the business logic.

There is still unavoidable lock-in at the edges. Authentication, mailboxes, Teams, Graph, Dataverse, Power Automate approvals, Copilot Studio publishing, and Microsoft 365 Copilot availability are all platform-specific. The aim should not be zero lock-in. The aim should be conscious, isolated lock-in.

## Microsoft/Copilot suitability

The Microsoft angle is suitable, but it should be positioned carefully.

For a home portfolio, Copilot Studio is useful for vocabulary, screenshots, and a low-code comparison, but it may not be the best core implementation. Microsoft documentation says trial access can allow users to create and test agents, while publishing can be restricted by trial/licensing conditions. It also notes that personal email addresses or disabled self-service signup can block access.

The Microsoft 365 Agents SDK is a better fit for the portability story. Microsoft describes it as a way to build agents deployable to channels such as Microsoft 365 Copilot, Teams, web, and custom apps while using the AI services and orchestration of your choice. Microsoft also describes custom engine agents as allowing developers to bring their own orchestration, AI services, workflows, models, and integrations.

So the recommended portfolio approach is:

1. Build the portable core first.
2. Implement one working OpenAI Agents SDK version.
3. Add a Microsoft mapping document.
4. Optionally add a thin Microsoft-facing adapter using Microsoft 365 Agents SDK if setup is manageable.
5. Treat Copilot Studio as an optional comparison surface, not the architectural center.

That supports the portfolio claim better than "I built a Copilot Studio bot."

## Suggested implementation sequence

1. Document the current human workflow.
2. Define the black-box contract.
3. Create synthetic sales data and requester profiles.
4. Define structured schemas for report requests, policy outcomes, report plans, and audit events.
5. Build deterministic tools for policy checks, querying, report generation, and reply drafting.
6. Build the OpenAI Agents SDK workflow around those tools.
7. Add fixture-based evaluation cases.
8. Generate example outputs: clarification email, approved report, rejected request, approval-required request, audit log.
9. Write the Microsoft mapping.
10. Add a thin adapter or Copilot Studio mock-up only after the core is demonstrably working.

## What to avoid in v1

Avoid these until the story is already working:

- Real inbox ingestion
- Real outbound email
- Real Power BI integration
- Arbitrary SQL generation over unknown schemas
- A full dashboard interface
- Complex multi-agent choreography
- Real row-level security
- Production Microsoft 365 tenant governance
- Multiple vendors implemented equally deeply

The project should be small enough that the README can honestly say what it does, and the demo can show every important path in a few minutes.

## Portfolio evidence to include

The final portfolio should show:

- A before/after process diagram
- The black-box contract
- A few realistic inbound email examples
- The extracted structured request JSON
- Clarification behavior
- Policy decisions
- Generated CSV/XLSX reports
- Audit logs or traces
- Evaluation cases with pass/fail results
- OpenAI implementation notes
- Microsoft/Copilot mapping notes
- A short demo video or GIF

The evaluation set is especially important. It signals engineering maturity and separates the project from a prompt demo.

## Main risks

The biggest risk is scope creep. The project becomes too complex if it tries to solve general analytics, real enterprise access control, real Microsoft deployment, and polished UX all at once.

The second risk is hiding the real value in implementation details. The portfolio should foreground the process model: current workflow, black-box contract, rules, controls, evaluation, and portability.

The third risk is over-agentifying. A single well-instructed agent with well-defined tools is probably stronger for v1 than a theatrical multi-agent setup. Multi-agent decomposition can be documented as an extension path.

## Final recommendation

Proceed with this portfolio piece. It is the right level of complex if scoped as a narrow, deployable workflow. It will demonstrate business understanding, agent architecture, governance awareness, deterministic tool use, evaluation discipline, and a pragmatic view of Microsoft/OpenAI portability.

The core thesis is excellent:

> Document the process first. Agentify only the well-understood black box. Keep the business logic portable. Let vendor platforms compete to host or surface the capability, rather than becoming the capability.

## References checked

- Microsoft Learn: Copilot Studio access and trial notes, including trial sign-up and possible personal-email/self-service restrictions: https://learn.microsoft.com/en-us/microsoft-copilot-studio/sign-up-individual
- Microsoft Learn: Copilot Studio licensing notes, including trial create/test limitations around publishing: https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing
- Microsoft Learn: Microsoft 365 Agents SDK overview, including channel deployment and choice of AI services/orchestration: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/agents-sdk-overview
- Microsoft Learn: Custom engine agents overview, including bring-your-own orchestration, AI services, workflows, models, and integrations: https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-custom-engine-agent
