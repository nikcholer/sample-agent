# OpenAI Agents SDK Adapter

## Purpose

This folder demonstrates the first vendor-specific surface over the portable core.

The OpenAI adapter is intentionally thin:

```text
Inbound email text
  -> OpenAI intake agent
  -> structured report request
  -> requester email resolution inside the tool
  -> portable core tool
  -> structured final output
```

The portable core still owns policy, report generation, response drafting, and audit events.

## Current SDK Notes

The current OpenAI Agents SDK documentation describes the main primitives used here:

- `Agent` for model instructions, tools, and structured outputs.
- `Runner.run_sync()` / `Runner.run()` for executing the agent loop.
- `@function_tool` for exposing Python functions as tools.
- `output_type` for structured final outputs.
- built-in tracing around `Runner` runs and function tool calls.

References:

- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/running_agents/
- https://openai.github.io/openai-agents-python/tools/
- https://openai.github.io/openai-agents-python/agents/
- https://openai.github.io/openai-agents-python/tracing/

## Files

| File | Purpose |
| --- | --- |
| `instructions.py` | Intake-agent instructions and boundaries. |
| `schemas.py` | Pydantic input/output models used by the adapter. |
| `tools.py` | Function-tool wrapper around the portable core, including requester email resolution. |
| `agent.py` | `Agent` construction. |
| `runner.py` | Fixture and raw-email runner helpers. |

The function tool is registered with `strict_mode=False`, and the final output type is wrapped with `AgentOutputSchema(..., strict_json_schema=False)`. The portable request contract includes dictionary-shaped fields such as `filters`, `ambiguous_terms`, `structured_request`, and `audit_event`; in `openai-agents==0.15.1`, strict schemas reject those `additionalProperties` shapes. The core still validates the structured request after the tool is called.

## Running

The local environment used while creating this project did not include `openai-agents`,
so the adapter is import-safe and the tool boundary is tested without a live API call.

To run the actual OpenAI Agents SDK path:

```powershell
python -m pip install -r requirements-openai.txt
$env:OPENAI_API_KEY = "sk-..."
python tools\run_openai_agent_case.py case-001
```

Optionally set a model:

```powershell
$env:OPENAI_AGENT_MODEL = "your-preferred-model"
python tools\run_openai_agent_case.py case-001
```

## Together AI / OpenAI-Compatible Providers

The OpenAI Agents SDK is open source, but that does not automatically guarantee every model backend works. The backend must support the API features this adapter uses: Chat Completions, function/tool calling, and structured JSON output.

Together AI exposes an OpenAI-compatible API at `https://api.together.xyz/v1`. To run the same adapter against Together:

```powershell
$env:OPENAI_AGENT_PROVIDER = "together"
$env:TOGETHER_API_KEY = "your-together-key"
$env:OPENAI_AGENT_MODEL = "openai/gpt-oss-20b"
python tools\run_openai_agent_case.py case-001
```

If `OPENAI_AGENT_MODEL` is unset and `OPENAI_AGENT_PROVIDER=together`, the adapter defaults to `openai/gpt-oss-20b` because Together documents it as supporting both function calling and structured outputs.

Together runs through the SDK's OpenAI-compatible provider path with `use_responses=False`, because Together's compatibility examples use Chat Completions. OpenAI tracing is disabled by default for Together runs; set `OPENAI_AGENTS_ENABLE_TRACING=true` if you deliberately want OpenAI-hosted traces as well.

## Design Boundary

The agent may interpret text and choose structured fields. It must call the portable core tool for every request. It must not:

- invent data
- calculate metrics directly
- make permission decisions itself
- skip policy checks
- generate files directly
- silently narrow a request

This keeps the OpenAI implementation useful as a code-first agent demonstration while preserving the vendor-neutral business logic.
