# Synthetic Business Domain

## Purpose

Milestone 2 turns the documented process into a safe, versioned business domain. The data is fictional but shaped to feel like a plausible sales-reporting environment.

The fixtures are deliberately small enough to inspect and deterministic enough to evaluate.

## Fixture Files

| File | Purpose |
| --- | --- |
| `agent_core/schemas/sales_orders.schema.json` | Machine-readable schema for sales order rows. |
| `samples/data/sales_orders.csv` | Synthetic sales orders generated from a deterministic script. |
| `samples/data/requesters.json` | Fictional requester profiles and entitlements. |
| `samples/policies/policy_rules.json` | Policy fixtures for supported metrics, dimensions, approvals, and restrictions. |
| `samples/inbound-requests/case-*.txt` | Plain-text inbound request examples. |
| `samples/expected-outputs/case-*.json` | Expected extraction, policy, and outcome for each case. |
| `tools/generate_synthetic_sales_data.py` | Regenerates the synthetic sales dataset. |

## Data Shape

The `SalesOrders` table contains:

- order identity and date
- region and country
- customer segment and customer name
- product category and product name
- salesperson and channel
- revenue, gross margin, and units

The data spans January 2025 through April 2026 across EMEA, Americas, and APAC. All names are fictional.

## Requester Profiles

Requester fixtures model common permission shapes:

- regional manager with UK/Ireland access and margin entitlement
- sales operations analyst with EMEA revenue/units access but no margin entitlement
- global sales director with broad access
- account manager restricted to the USA
- product manager with APAC access but no customer-level entitlement

These profiles are intentionally simple. The point is to make policy behavior explicit before production identity or row-level security is introduced.

## Evaluation Cases

The first case set covers:

- clear approved request
- ambiguous request requiring clarification
- approved margin request
- margin request from a user without margin entitlement
- customer-level request requiring approval
- unauthorized global raw extract
- unsupported dashboard request
- approved monthly trend request

Every inbound request has an expected output file. Future implementation work should treat these as the contract for extraction and policy behavior.

## Regeneration

To regenerate the synthetic dataset:

```powershell
python tools\generate_synthetic_sales_data.py
```

The script uses a fixed random seed. Regenerating should produce the same `samples/data/sales_orders.csv` unless the generator is intentionally changed.
