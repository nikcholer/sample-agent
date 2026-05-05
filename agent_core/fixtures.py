from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from agent_core.models import RequesterProfile, StructuredRequest


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_requesters(path: Path | None = None) -> dict[str, RequesterProfile]:
    data = load_json(path or ROOT / "samples" / "data" / "requesters.json")
    return {
        item["requester_id"]: RequesterProfile.from_dict(item)
        for item in data
    }


def load_policy_rules(path: Path | None = None) -> dict[str, Any]:
    return load_json(path or ROOT / "samples" / "policies" / "policy_rules.json")


def load_sales_rows(path: Path | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with (path or ROOT / "samples" / "data" / "sales_orders.csv").open(
        newline="",
        encoding="utf-8",
    ) as handle:
        for row in csv.DictReader(handle):
            converted = dict(row)
            converted["revenue"] = float(row["revenue"])
            converted["gross_margin"] = float(row["gross_margin"])
            converted["units"] = int(row["units"])
            rows.append(converted)
    return rows


def load_expected_case(case_id: str) -> dict[str, Any]:
    return load_json(ROOT / "samples" / "expected-outputs" / f"{case_id}.json")


def load_structured_request_from_case(case_id: str) -> StructuredRequest:
    return StructuredRequest.from_dict(load_expected_case(case_id)["structured_request"])
