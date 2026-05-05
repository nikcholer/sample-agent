from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.evaluation import (
    EVALUATION_CASE_IDS,
    evaluate_result,
    run_core_fixture_case,
    summarize_evaluations,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate fixture cases against the portable core or live agent adapter."
    )
    parser.add_argument(
        "--implementation",
        choices=["core", "openai"],
        default="core",
        help="Implementation to evaluate. Use 'openai' for the OpenAI Agents SDK adapter.",
    )
    parser.add_argument(
        "--cases",
        nargs="*",
        default=list(EVALUATION_CASE_IDS),
        help="Case IDs to evaluate. Defaults to all fixture cases.",
    )
    parser.add_argument("--repeat", type=int, default=1, help="Runs per case.")
    parser.add_argument("--model", default=None, help="Optional live-adapter model override.")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "generated" / "evaluation" / "reports"),
        help="Core implementation report output directory.",
    )
    parser.add_argument(
        "--audit-dir",
        default=str(ROOT / "generated" / "evaluation" / "traces"),
        help="Core implementation audit output directory.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    parser.add_argument("--json-out", default=None, help="Optional path for JSON summary.")
    parser.add_argument(
        "--no-fail",
        action="store_true",
        help="Exit with 0 even when mismatches are found.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    audit_dir = Path(args.audit_dir)
    provider = None
    model = None
    if args.implementation == "openai":
        from implementations.openai_agents_sdk.provider_config import (
            selected_model,
            selected_provider,
        )

        provider = selected_provider()
        model = selected_model(args.model)

    results: list[dict[str, Any]] = []
    for repeat in range(1, args.repeat + 1):
        for case_id in args.cases:
            results.append(
                _evaluate_one(
                    case_id=case_id,
                    implementation=args.implementation,
                    provider=provider,
                    model=model,
                    repeat=repeat,
                    output_dir=output_dir,
                    audit_dir=audit_dir,
                    model_override=args.model,
                )
            )

    payload = {
        "implementation": args.implementation,
        "provider": provider,
        "model": model,
        "repeat": args.repeat,
        "summary": summarize_evaluations(results),
        "results": results,
    }
    if args.json_out:
        json_path = Path(args.json_out)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_text(payload)

    if payload["summary"]["failed"] and not args.no_fail:
        raise SystemExit(1)


def _evaluate_one(
    *,
    case_id: str,
    implementation: str,
    provider: str | None,
    model: str | None,
    repeat: int,
    output_dir: Path,
    audit_dir: Path,
    model_override: str | None,
) -> dict[str, Any]:
    try:
        if implementation == "core":
            actual = run_core_fixture_case(
                case_id,
                output_dir=output_dir,
                audit_dir=audit_dir,
            )
            result_audit_dir = audit_dir
        else:
            actual = _run_openai_fixture_case(case_id=case_id, model=model_override)
            result_audit_dir = None

        return evaluate_result(
            case_id=case_id,
            actual_result=actual,
            implementation=implementation,
            provider=provider,
            model=model,
            repeat=repeat,
            repo_root=ROOT,
            audit_dir=result_audit_dir,
        )
    except Exception as exc:
        return {
            "case_id": case_id,
            "implementation": implementation,
            "provider": provider,
            "model": model,
            "repeat": repeat,
            "passed": False,
            "expected_outcome": None,
            "actual_outcome": None,
            "output_path": None,
            "mismatches": [
                {
                    "field": "run",
                    "expected": "case evaluation completed",
                    "actual": f"{type(exc).__name__}: {exc}",
                }
            ],
        }


def _run_openai_fixture_case(*, case_id: str, model: str | None) -> Any:
    from implementations.openai_agents_sdk.runner import run_fixture_case

    return run_fixture_case(case_id=case_id, model=model)


def _print_text(payload: dict[str, Any]) -> None:
    label = payload["implementation"]
    if payload["provider"]:
        label += f" provider={payload['provider']}"
    if payload["model"]:
        label += f" model={payload['model']}"
    print(f"Evaluation: {label}")

    for result in payload["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status} {result['case_id']} run={result['repeat']}")
        for mismatch in result["mismatches"][:8]:
            print(
                "  - "
                f"{mismatch['field']}: expected {mismatch['expected']!r}, "
                f"actual {mismatch['actual']!r}"
            )
        if len(result["mismatches"]) > 8:
            print(f"  - ... {len(result['mismatches']) - 8} more mismatches")

    summary = payload["summary"]
    print(
        "Summary: "
        f"{summary['passed']} passed, {summary['failed']} failed, "
        f"{summary['total']} total, pass_rate={summary['pass_rate']}"
    )


if __name__ == "__main__":
    main()
