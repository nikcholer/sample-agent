from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from agent_core.models import ReportOutput, ReportPlan, StructuredRequest
from agent_core.report_generation.xlsx import write_xlsx


def build_report_plan(request: StructuredRequest) -> ReportPlan:
    if request.date_range is None:
        raise ValueError("date_range is required for report planning")

    filters: dict[str, Any] = dict(request.filters)
    filters["order_date"] = {
        "start": request.date_range.start,
        "end": request.date_range.end,
    }
    output_format = request.output_format or "xlsx"
    return ReportPlan(
        source_table="SalesOrders",
        group_by=request.dimensions,
        metrics=request.metrics,
        filters=filters,
        output_format=output_format,
        limit=request.limit,
        sort_by=request.sort_by,
    )


def generate_report(
    *,
    plan: ReportPlan,
    source_rows: list[dict[str, Any]],
    output_dir: Path,
    request_id: str,
    metadata: dict[str, Any],
) -> ReportOutput:
    selected_rows = _filter_rows(source_rows, plan.filters)
    report_rows = _build_rows(selected_rows, plan)

    if plan.output_format == "csv":
        path = output_dir / f"{request_id}.csv"
        _write_csv(path, report_rows)
    elif plan.output_format == "xlsx":
        path = output_dir / f"{request_id}.xlsx"
        _write_workbook(path, report_rows, metadata)
    else:
        raise ValueError(f"Unsupported output format: {plan.output_format}")

    return ReportOutput(
        path=str(path),
        rows=report_rows,
        metadata=metadata,
    )


def _filter_rows(
    rows: list[dict[str, Any]],
    filters: dict[str, Any],
) -> list[dict[str, Any]]:
    date_filter = filters.get("order_date", {})
    start = date_filter.get("start")
    end = date_filter.get("end")
    filtered: list[dict[str, Any]] = []
    for row in rows:
        if start and row["order_date"] < start:
            continue
        if end and row["order_date"] > end:
            continue
        if not _matches_list_filter(row, filters, "country"):
            continue
        if not _matches_list_filter(row, filters, "region"):
            continue
        if not _matches_list_filter(row, filters, "product_category"):
            continue
        if not _matches_list_filter(row, filters, "channel"):
            continue
        if not _matches_list_filter(row, filters, "customer_segment"):
            continue
        filtered.append(row)
    return filtered


def _matches_list_filter(
    row: dict[str, Any],
    filters: dict[str, Any],
    field: str,
) -> bool:
    values = filters.get(field)
    if not values:
        return True
    return row[field] in values


def _build_rows(rows: list[dict[str, Any]], plan: ReportPlan) -> list[dict[str, Any]]:
    if plan.source_table != "SalesOrders":
        raise ValueError(f"Unsupported source table: {plan.source_table}")

    if not plan.group_by:
        return _raw_rows(rows, plan)

    grouped: dict[tuple[Any, ...], dict[str, Any]] = defaultdict(dict)
    for row in rows:
        key = tuple(_dimension_value(row, dimension) for dimension in plan.group_by)
        bucket = grouped[key]
        for index, dimension in enumerate(plan.group_by):
            bucket[dimension] = key[index]
        for metric in plan.metrics:
            bucket[metric] = round(float(bucket.get(metric, 0)) + float(row[metric]), 2)

    report_rows = list(grouped.values())
    sort_field = plan.sort_by or (plan.metrics[0] if plan.metrics else plan.group_by[0])
    if plan.group_by == ["month"]:
        report_rows.sort(key=lambda item: item["month"])
    else:
        report_rows.sort(
            key=lambda item: item.get(sort_field, 0),
            reverse=sort_field in plan.metrics,
        )
    if plan.limit is not None:
        report_rows = report_rows[: plan.limit]
    return report_rows


def _raw_rows(rows: list[dict[str, Any]], plan: ReportPlan) -> list[dict[str, Any]]:
    columns = [
        "order_id",
        "order_date",
        "region",
        "country",
        "product_category",
        "product_name",
        "customer_name",
        "channel",
        *plan.metrics,
    ]
    deduped_columns = list(dict.fromkeys(columns))
    return [
        {column: row[column] for column in deduped_columns}
        for row in rows
    ]


def _dimension_value(row: dict[str, Any], dimension: str) -> Any:
    if dimension == "month":
        return row["order_date"][:7]
    return row[dimension]


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = list(rows[0]) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def _write_workbook(
    path: Path,
    report_rows: list[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    summary = _summary_rows(report_rows)
    metadata_rows = [
        {"field": key, "value": json.dumps(value) if isinstance(value, dict | list) else value}
        for key, value in metadata.items()
    ]
    write_xlsx(
        path,
        {
            "Summary": summary,
            "Data": report_rows,
            "Request Metadata": metadata_rows,
        },
    )


def _summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return [{"measure": "row_count", "value": 0}]
    summary = [{"measure": "row_count", "value": len(rows)}]
    metric_names = [
        key
        for key, value in rows[0].items()
        if isinstance(value, int | float)
    ]
    for metric in metric_names:
        summary.append(
            {
                "measure": f"total_{metric}",
                "value": round(sum(float(row.get(metric, 0)) for row in rows), 2),
            }
        )
    return summary
