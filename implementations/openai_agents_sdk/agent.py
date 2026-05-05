from __future__ import annotations

from implementations.openai_agents_sdk.instructions import INTAKE_AGENT_INSTRUCTIONS
from implementations.openai_agents_sdk.schemas import AgentFinalOutput
from implementations.openai_agents_sdk.tools import process_sales_report_request


def build_intake_agent(model: str | None = None):
    try:
        from agents import Agent
    except ImportError as exc:
        raise RuntimeError(
            "The OpenAI Agents SDK is not installed. Install it with "
            "`python -m pip install -r requirements-openai.txt` to run this adapter."
        ) from exc

    kwargs = {
        "name": "Sales Data Request Intake Agent",
        "instructions": INTAKE_AGENT_INSTRUCTIONS,
        "tools": [process_sales_report_request],
        "output_type": AgentFinalOutput,
    }
    if model:
        kwargs["model"] = model
    return Agent(**kwargs)
