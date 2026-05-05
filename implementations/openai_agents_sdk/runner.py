from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from implementations.openai_agents_sdk.agent import build_intake_agent
from implementations.openai_agents_sdk.schemas import AgentFinalOutput


def run_email_request(
    *,
    email_text: str,
    request_id: str,
    model: str | None = None,
    trace_group_id: str | None = None,
) -> AgentFinalOutput:
    try:
        from agents import Runner, trace
    except ImportError as exc:
        raise RuntimeError(
            "The OpenAI Agents SDK is not installed. Install it with "
            "`python -m pip install -r requirements-openai.txt` to run this adapter."
        ) from exc

    agent = build_intake_agent(model=model or os.getenv("OPENAI_AGENT_MODEL"))
    prompt = _build_prompt(email_text=email_text, request_id=request_id)
    with trace("portable-email-to-report", group_id=trace_group_id or request_id):
        result = Runner.run_sync(agent, prompt, max_turns=6)
    final_output = result.final_output
    if isinstance(final_output, AgentFinalOutput):
        return final_output
    if isinstance(final_output, dict):
        return AgentFinalOutput(**final_output)
    raise TypeError(f"Unexpected final output type: {type(final_output)!r}")


def run_fixture_case(
    *,
    case_id: str,
    model: str | None = None,
    samples_dir: Path | None = None,
) -> AgentFinalOutput:
    samples_dir = samples_dir or Path(__file__).resolve().parents[2] / "samples"
    email_text = (samples_dir / "inbound-requests" / f"{case_id}.txt").read_text(
        encoding="utf-8"
    )
    return run_email_request(
        email_text=email_text,
        request_id=case_id,
        model=model,
        trace_group_id=case_id,
    )


def _build_prompt(*, email_text: str, request_id: str) -> str:
    return f"""Request ID: {request_id}

Inbound message:
{email_text}

Process this request. Extract the requester from the From line, identify the matching
requester email address, create the structured report request, call the portable core
tool, and return the structured final output.
"""
