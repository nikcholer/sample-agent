from __future__ import annotations

import os
from contextlib import nullcontext


TOGETHER_BASE_URL = "https://api.together.xyz/v1"
TOGETHER_DEFAULT_MODEL = "openai/gpt-oss-20b"


def selected_provider() -> str:
    return os.getenv("OPENAI_AGENT_PROVIDER", "openai").strip().lower()


def selected_model(explicit_model: str | None = None) -> str | None:
    if explicit_model:
        return explicit_model
    env_model = os.getenv("OPENAI_AGENT_MODEL")
    if env_model:
        return env_model
    if selected_provider() == "together":
        return TOGETHER_DEFAULT_MODEL
    return None


def build_run_config():
    provider = selected_provider()
    if provider == "openai":
        return None
    if provider == "together":
        return _together_run_config()
    raise RuntimeError(
        "Unsupported OPENAI_AGENT_PROVIDER. Expected 'openai' or 'together'."
    )


def trace_context(*, workflow_name: str, group_id: str):
    if _tracing_disabled_for_provider():
        return nullcontext()

    try:
        from agents import trace
    except ImportError as exc:
        raise RuntimeError(
            "The OpenAI Agents SDK is not installed. Install it with "
            "`python -m pip install -r requirements-openai.txt` to run this adapter."
        ) from exc

    return trace(workflow_name, group_id=group_id)


def _together_run_config():
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise RuntimeError("TOGETHER_API_KEY is required when OPENAI_AGENT_PROVIDER=together.")

    try:
        from agents import RunConfig
        from agents.models.openai_provider import OpenAIProvider
    except ImportError as exc:
        raise RuntimeError(
            "The OpenAI Agents SDK is not installed. Install it with "
            "`python -m pip install -r requirements-openai.txt` to run this adapter."
        ) from exc

    base_url = os.getenv("TOGETHER_BASE_URL", TOGETHER_BASE_URL)
    return RunConfig(
        model_provider=OpenAIProvider(
            api_key=api_key,
            base_url=base_url,
            use_responses=False,
        ),
        tracing_disabled=_tracing_disabled_for_provider(),
    )


def _tracing_disabled_for_provider() -> bool:
    value = os.getenv("OPENAI_AGENTS_ENABLE_TRACING")
    if value is not None:
        return value.strip().lower() not in {"1", "true", "yes", "on"}
    return selected_provider() != "openai"
