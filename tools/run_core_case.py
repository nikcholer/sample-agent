from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_core.fixtures import load_expected_case
from agent_core.models import StructuredRequest
from agent_core.workflow import process_request


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one fixture case through the portable core.")
    parser.add_argument("case_id", help="Case ID, for example case-001")
    parser.add_argument("--output-dir", default=str(ROOT / "generated" / "reports"))
    parser.add_argument("--audit-dir", default=str(ROOT / "generated" / "traces"))
    args = parser.parse_args()

    expected = load_expected_case(args.case_id)
    result = process_request(
        request_id=args.case_id,
        requester_id=expected["requester_id"],
        structured_request=StructuredRequest.from_dict(expected["structured_request"]),
        output_dir=Path(args.output_dir),
        audit_dir=Path(args.audit_dir),
    )
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
