# Portable Core

## Purpose

The portable core is the vendor-neutral implementation of the sales request workflow. It can run without OpenAI, Microsoft, email integration, or any agent SDK.

It assumes that a structured request already exists. In later milestones, an agent runtime can produce that structured request from natural-language email. The core then performs the deterministic work:

- validate completeness
- check policy and permissions
- build a report plan
- generate CSV/XLSX outputs
- draft a response
- write an audit event

## Main Entry Point

The main function is:

```python
from agent_core.models import StructuredRequest
from agent_core.workflow import process_request

result = process_request(
    request_id="case-001",
    requester_id="u-1001",
    structured_request=StructuredRequest.from_dict(data),
)
```

The result includes:

- outcome
- policy decision
- response message
- optional report plan
- optional output path
- audit event

## CLI

Run one fixture case through the portable core:

```powershell
python tools\run_core_case.py case-001
```

Generated reports and audit traces are written under `generated/`, which is ignored by Git.

## Tests

Run the core tests:

```powershell
python -m unittest discover -s tests
```

The tests check that:

- fixture policy decisions match expected outputs
- report plans match expected report cases
- CSV report generation works
- XLSX report generation creates the expected workbook structure
- clarification does not generate a report

## Design Boundary

The portable core does not parse unstructured email. That is intentional. Natural-language interpretation belongs to the adapter/agent layer. The core owns the contract once a structured request exists.

This keeps the business logic portable across OpenAI Agents SDK, Microsoft 365 Agents SDK, Copilot Studio, web forms, ticket workflows, and other future surfaces.
