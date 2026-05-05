# Evaluation Results

## Current Deterministic Baseline

The portable core evaluation currently passes all fixture cases:

```powershell
python tools\evaluate_cases.py --implementation core
```

Expected result:

```text
Summary: 8 passed, 0 failed, 8 total, pass_rate=1.0
```

This baseline proves the policy, report generation, response drafting, and audit path are deterministic when the structured request is known.

## Live Adapter Observations

The OpenAI Agents SDK adapter can be evaluated against the same fixtures:

```powershell
python tools\evaluate_cases.py --implementation openai
```

For Together AI:

```powershell
$env:OPENAI_AGENT_PROVIDER = "together"
$env:TOGETHER_API_KEY = "your-together-key"
$env:OPENAI_AGENT_MODEL = "openai/gpt-oss-20b"
python tools\evaluate_cases.py --implementation openai
```

Known live smoke-test observations with `openai/gpt-oss-20b`:

- tool calling worked after removing the model-facing final response schema
- report generation and audit events worked for approved cases
- `generated/` output is ignored by Git and safe for local demo files
- early runs showed extraction drift on ambiguous metrics and geography normalization

Examples of extraction drift seen before prompt hardening:

- bare "sales" was over-resolved to `revenue` instead of treated as ambiguous
- `UK` was misclassified as a region instead of a country filter
- `EMEA` was used as both a filter and a grouping dimension

These are useful failures, not just bugs. They show why the portfolio needs a repeatable evaluation harness and why model choice should be justified by pass rate and stability.

## Current Limitations

- The first harness uses exact fixture comparisons for structured fields. It is intentionally strict and may flag harmless wording or purpose-summary drift.
- Response quality checks are still mostly indirect through outcome, policy, and audit checks.
- Live model comparison is manual: choose models with `OPENAI_AGENT_MODEL` or `--model`, then compare pass rates.
- Cost tracking is not automated yet, so "cost per correct case" must be calculated outside the harness for now.
- The harness does not yet inspect every cell in generated XLSX reports; it checks file existence and expected workbook structure.
