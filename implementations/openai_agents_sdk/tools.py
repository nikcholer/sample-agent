from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, TypeVar

from agent_core.fixtures import load_requesters
from agent_core.models import StructuredRequest
from agent_core.workflow import process_request
from implementations.openai_agents_sdk.schemas import ReportRequestInput, ToolResult


F = TypeVar("F", bound=Callable[..., Any])


def _optional_function_tool(func: F) -> F | Any:
    try:
        from agents import function_tool
    except ImportError:
        return func
    return function_tool(
        func,
        name_override="process_sales_report_request",
        strict_mode=False,
    )


def process_sales_report_request_raw(
    *,
    request_id: str,
    requester_id: str | None = None,
    requester_email: str | None = None,
    structured_request: ReportRequestInput,
    output_dir: str = "generated/reports",
    audit_dir: str = "generated/traces",
    parent_request_id: str | None = None,
) -> dict[str, Any]:
    """Run the vendor-neutral portable core for one structured report request."""

    core_request = StructuredRequest.from_dict(
        structured_request.model_dump(exclude_none=False)
    )
    resolved_requester_id = requester_id or _resolve_requester_id(requester_email)
    result = process_request(
        request_id=request_id,
        requester_id=resolved_requester_id,
        structured_request=core_request,
        output_dir=Path(output_dir),
        audit_dir=Path(audit_dir),
        parent_request_id=parent_request_id,
    )
    payload = result.to_dict()
    payload["requester_id"] = result.audit_event.requester_id
    return ToolResult(**payload).model_dump(mode="json")


def process_sales_report_request_for_agent(
    *,
    request_id: str,
    requester_id: str | None = None,
    requester_email: str | None = None,
    structured_request: ReportRequestInput,
    output_dir: str = "generated/reports",
    audit_dir: str = "generated/traces",
    parent_request_id: str | None = None,
) -> str:
    """Run the portable core and return JSON text for the SDK final output."""

    result = process_sales_report_request_raw(
        request_id=request_id,
        requester_id=requester_id,
        requester_email=requester_email,
        structured_request=structured_request,
        output_dir=output_dir,
        audit_dir=audit_dir,
        parent_request_id=parent_request_id,
    )
    return json.dumps(result, sort_keys=True)


def _resolve_requester_id(requester_email: str | None) -> str:
    if requester_email is None:
        return "unknown"
    normalized = requester_email.strip().lower()
    for requester_id, profile in load_requesters().items():
        if profile.email.lower() == normalized:
            return requester_id
    return normalized


process_sales_report_request = _optional_function_tool(process_sales_report_request_for_agent)
