# Architecture

## Design Thesis

The project separates the thing that should be portable from the things that are naturally platform-specific.

Portable:

- request contract
- validation rules
- entitlement policy
- report planning and generation
- response outcome taxonomy
- audit schema
- evaluation fixtures

Platform-specific:

- email, Teams, Copilot, or web-channel handling
- provider/model configuration
- identity lookup
- file storage and delivery
- tracing and telemetry integrations
- publishing and tenant governance

## Runtime Architecture

```mermaid
flowchart LR
    U["Requester"] --> E["Email text or channel message"]
    E --> A["Adapter layer"]
    A --> X["Request extraction"]
    X --> S["StructuredRequest"]
    S --> C["Portable core"]
    C --> V["Validation"]
    C --> P["Policy engine"]
    C --> B["Report builder"]
    C --> R["Response drafter"]
    C --> L["Audit logger"]
    B --> F["CSV/XLSX output"]
    R --> M["Reply message"]
    L --> J["Audit JSON"]
```

The adapter can be OpenAI Agents SDK, Microsoft 365 Agents SDK, Copilot Studio calling a custom API, a web form, or a plain CLI runner. The core behavior stays the same.

## Agent Boundary

```mermaid
flowchart TB
    subgraph Adapter["Agent/runtime adapter"]
        I["Inbound natural language"]
        N["Normalize to structured request"]
        T["Call portable core tool"]
    end

    subgraph Core["Portable core"]
        V["Validate completeness"]
        P["Evaluate policy"]
        G["Generate report if allowed"]
        D["Draft governed response"]
        A["Write audit event"]
    end

    I --> N --> T --> V
    V --> P --> G
    P --> D
    G --> D
    D --> A
```

The agent may interpret language and choose structured fields. It must not:

- invent sales data
- calculate metrics
- make entitlement decisions
- skip policy checks
- generate report files directly
- hide clarification or approval requirements

## Before Workflow

```mermaid
flowchart LR
    R["Requester emails vague report ask"] --> T["Analyst reads email"]
    T --> Q{"Enough detail?"}
    Q -- "No" --> C["Clarification email"]
    C --> R
    Q -- "Yes" --> P["Manual permission judgment"]
    P --> B["Find data source and build report"]
    B --> S["Send file or link"]
    S --> L["Ad hoc notes or no audit"]
```

The manual process works, but it depends on analyst memory, inconsistent policy interpretation, and repeated navigation across corporate UI surfaces.

## After Workflow

```mermaid
flowchart LR
    R["Requester sends natural-language request"] --> A["Agent intake"]
    A --> C["Portable core"]
    C --> O{"Outcome"}
    O -- "Generated report" --> F["CSV/XLSX plus reply"]
    O -- "Clarification" --> K["Targeted clarification reply"]
    O -- "Approval" --> P["Approval route"]
    O -- "Rejected" --> X["Reasoned rejection"]
    C --> J["Audit JSON"]
```

The improved workflow keeps the natural-language entry point while making policy, output, and audit deterministic.

## Evaluation Architecture

```mermaid
flowchart LR
    F["Fixture cases"] --> E["Evaluation harness"]
    E --> C["Portable core run"]
    E --> L["Live adapter run"]
    C --> M["Field-level comparison"]
    L --> M
    M --> S["Pass/fail summary"]
    M --> J["JSON result"]
```

The harness compares outcomes, structured request fields, policy decisions, report plans, output files, and audit events. For live model runs, it also records provider and model metadata.

## Main Code Paths

| Path | Role |
| --- | --- |
| `agent_core/models.py` | Portable data contracts. |
| `agent_core/workflow.py` | Main deterministic process orchestration. |
| `agent_core/policies/engine.py` | Permission and approval decisions. |
| `agent_core/report_generation/` | CSV/XLSX planning and output. |
| `agent_core/evaluation.py` | Fixture scoring and summary logic. |
| `implementations/openai_agents_sdk/` | Thin live agent adapter. |
| `tools/evaluate_cases.py` | Repeatable evaluation CLI. |
