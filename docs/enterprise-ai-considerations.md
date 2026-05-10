# Enterprise AI Considerations

This project is framed as a business-agent pattern rather than a chatbot demo. The main design question is where the LLM is useful and where ordinary software should stay in control.

## LLM Responsibility

The model can help interpret an unstructured request, identify missing information, and draft a human-readable response. Those are language-heavy tasks where probabilistic reasoning is useful.

The model should not own:

- permission decisions;
- report calculations;
- file generation;
- audit records;
- final policy outcomes.

Those responsibilities sit in the portable core so they can be tested, reviewed and reused from different agent surfaces.

## Data Security

The repository uses synthetic data. A real deployment would need clear controls before connecting to mailboxes, Teams messages, CRM systems, finance data or customer records.

Production questions include:

- which data fields may be sent to a model provider;
- whether the provider endpoint is public, private or tenant-approved;
- how request and response payloads are logged;
- how generated files are stored and retained;
- how user permissions are resolved and cached;
- how sensitive prompt content is redacted from diagnostics.

## Prompt Injection and Exfiltration

Inbound messages can contain instructions that attempt to override policy, disclose restricted data, or bypass approval. The workflow treats the email as untrusted input.

The core pattern reduces risk by requiring the agent adapter to call deterministic functions for permissions, report generation and audit. The adapter may extract intent, but the portable core decides what can be produced.

## Operational Governance

The evaluation fixtures are part of the governance story. They let a team compare model/provider behavior against known request cases instead of relying on a single impressive demo run.

Useful production additions would include:

- richer negative test fixtures;
- role and entitlement integration;
- immutable audit storage;
- model/provider version capture;
- human approval queues for high-risk requests;
- monitoring for unusual request patterns or repeated denied access attempts.
