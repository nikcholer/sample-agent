from __future__ import annotations

import json
from pathlib import Path

from agent_core.models import AuditEvent


def write_audit_event(event: AuditEvent, audit_dir: Path) -> Path:
    audit_dir.mkdir(parents=True, exist_ok=True)
    path = audit_dir / f"{event.request_id}.json"
    path.write_text(
        json.dumps(event.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return path
