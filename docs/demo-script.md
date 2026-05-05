# Demo Script

## Goal

Show the project as a complete business-agent slice in 5 to 8 minutes:

- process first
- portable core second
- agent adapter third
- evaluation and platform mapping last

## Setup

```powershell
git pull
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

Optional live adapter setup:

```powershell
python -m pip install -r requirements-openai.txt
$env:OPENAI_AGENT_PROVIDER = "together"
$env:TOGETHER_API_KEY = "your-together-key"
$env:OPENAI_AGENT_MODEL = "openai/gpt-oss-20b"
```

## Walkthrough

### 1. Open With The Business Problem

Show:

- [process-overview.md](process-overview.md)
- [current-human-workflow.md](current-human-workflow.md)

Talk track:

> This starts as a common corporate problem: users ask for reports through email because the actual data is spread across tools, permissions, and conventions. The first move was to document the process, not build an agent.

### 2. Show The Contract

Show:

- [black-box-contract.md](black-box-contract.md)
- [policy-and-permissions.md](policy-and-permissions.md)

Talk track:

> The agent is not allowed to be a fuzzy BI system. It has a narrow contract: extract intent, run deterministic policy, generate controlled outputs, and audit every outcome.

### 3. Run The Portable Core

Command:

```powershell
python tools\run_core_case.py case-001
```

Point out:

- `outcome`
- `policy_decision`
- `report_plan`
- `output_path`
- `audit_event`

Then show committed examples:

- `samples/example-outputs/reports/case-001.xlsx`
- `samples/example-outputs/traces/case-001.json`

Talk track:

> This run does not use any agent SDK. The core can stand alone, which is the main anti-lock-in design choice.

### 4. Show Clarification And Approval Paths

Commands:

```powershell
python tools\run_core_case.py case-002
python tools\run_core_case.py case-005
```

Point out:

- case 002 does not pause a process; it terminates with `clarification_required`
- the user's clarified reply would start a new linked run
- case 005 routes to approval rather than generating customer-level output

### 5. Run The Evaluation Harness

Command:

```powershell
python tools\evaluate_cases.py --implementation core
```

Expected:

```text
Summary: 8 passed, 0 failed, 8 total, pass_rate=1.0
```

Talk track:

> This is what turns the project from a prompt demo into an engineered workflow. The fixture set can score the portable core and live adapters against the same expected outputs.

### 6. Show The Agent Adapter

Show:

- [openai-agents-sdk.md](openai-agents-sdk.md)
- `implementations/openai_agents_sdk/instructions.py`
- `implementations/openai_agents_sdk/tools.py`

Optional live command:

```powershell
python tools\run_openai_agent_case.py case-001
```

Talk track:

> The OpenAI adapter is deliberately thin. It extracts a structured request and must call the portable core. Provider/model choice can change without changing the business logic.

### 7. Show Microsoft Mapping

Show:

- [microsoft-copilot-mapping.md](microsoft-copilot-mapping.md)

Talk track:

> This avoids committing to Copilot Studio or Microsoft 365 Agents SDK too early. The document identifies what would be platform-specific and keeps policy/report/audit logic portable.

### 8. Close With Trade-Offs

Show:

- [implementation-notes.md](implementation-notes.md)
- [limitations-and-extensions.md](limitations-and-extensions.md)

Talk track:

> The point is not that every process needs an agent. A web form may be enough if request types are simple. The agent earns its keep when a single natural-language entry point can handle many request patterns while still enforcing deterministic controls.

## Recording Notes

For a short demo video or GIF, record:

1. README opening and architecture diagram.
2. `python tools\evaluate_cases.py --implementation core`.
3. A generated report and audit JSON.
4. OpenAI adapter docs or a live adapter run, if credentials are available.

Avoid showing real API keys, terminal environment variables containing keys, or live provider dashboards.
