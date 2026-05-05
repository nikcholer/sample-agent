from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from implementations.openai_agents_sdk.runner import run_fixture_case


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run one inbound fixture through the OpenAI Agents SDK adapter."
    )
    parser.add_argument("case_id", help="Case ID, for example case-001")
    parser.add_argument("--model", default=None, help="Optional model override.")
    args = parser.parse_args()

    try:
        result = run_fixture_case(case_id=args.case_id, model=args.model)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from None
    print(json.dumps(result.model_dump(mode="json"), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
