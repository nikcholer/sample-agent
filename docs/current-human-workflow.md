# Current Human Workflow

## Summary

The current workflow is already an implementation. It is implemented through people, habits, shared knowledge, email, spreadsheets, BI tools, and browser tabs.

A requester sends a sales-data question to an analyst or shared mailbox. The analyst interprets the request, clarifies missing details, checks access, produces a report, and replies with the result. Much of the real process lives in the analyst's judgment rather than in a documented system.

## Actors

| Actor | Role |
| --- | --- |
| Requester | Employee who needs a sales report or data extract. |
| Analyst | Human operator who interprets and fulfils requests. |
| Manager / Approver | Person who can approve sensitive or unusually broad requests. |
| Data Owner | Business owner of sales data and access rules. |
| Recipient | Person or group receiving the output, often the same as the requester. |

## Typical Request

Example:

```text
Hi, could you send me UK sales for Q4 by product category and region?
I need it for next week's trading review. Excel would be ideal.
```

This request is clear enough to proceed if the requester has permission to see UK sales, product category breakdowns, and any requested metrics.

## Ambiguous Request

Example:

```text
Can I get sales for last quarter by region for a board deck?
```

The analyst may need to clarify:

- whether "sales" means revenue, units, gross margin, or all three
- which country or business unit is in scope
- what "last quarter" means relative to the reporting calendar
- whether Excel or CSV is required
- whether board-deck use permits aggregated data only

## Manual Process Steps

1. Request arrives by email, chat, ticket, or direct message.
2. Analyst reads the request and infers the intended report.
3. Analyst checks whether the request is clear enough to fulfil.
4. If details are missing, analyst sends a clarification question.
5. Analyst identifies the requester and likely permissions.
6. Analyst checks sensitive fields, date range, geography, and data granularity.
7. Analyst decides whether the request can proceed, must be narrowed, needs approval, or should be rejected.
8. Analyst opens the relevant BI tool, spreadsheet, database extract, or saved report.
9. Analyst applies filters, dimensions, and metrics.
10. Analyst checks the result for obvious mistakes.
11. Analyst exports CSV/XLSX.
12. Analyst writes a reply explaining what is attached and any assumptions made.
13. Analyst saves or leaves behind an informal audit trail in email, file names, or notes.

## Current Pain Points

- Requesters do not know which tool or form to use.
- Different departments have different unofficial request paths.
- Analysts spend time translating vague requests into structured report specifications.
- Permission checks are partly manual and inconsistent.
- Important assumptions may only appear in email prose.
- Repeated report requests are not always captured as reusable patterns.
- Audit trails are scattered across email threads, local files, tickets, and spreadsheets.
- Report quality depends heavily on the analyst who handles the request.

## Current Controls

Controls exist, but many are informal:

- analysts know which users usually receive which reports
- sensitive requests are escalated to managers
- customer-level exports are treated more carefully than aggregated summaries
- broad extracts are challenged or narrowed
- email threads create a partial audit trail
- report outputs may include filters or notes in worksheet names or filenames

The agentic workflow should make these controls explicit and testable.

## Manual Workflow as Black Box

The current manual process can be described as a black box:

| Element | Current form |
| --- | --- |
| Input | Email, chat message, ticket, or informal request. |
| Interpretation | Analyst reads and infers intent. |
| Rules | Analyst applies documented and undocumented policy knowledge. |
| Tools | BI tools, spreadsheets, saved reports, exports. |
| Output | Report file, clarification, rejection, or escalation. |
| Evidence | Email thread, exported file, analyst notes, ticket history. |

The agentic implementation should replace the internal mechanism without changing the externally understandable contract.

## What Good Looks Like

A better process should:

- make request interpretation visible as structured data
- ask for missing information consistently
- enforce policy before generating outputs
- generate reports deterministically
- explain assumptions and exclusions
- leave an audit event for every decision
- allow the same business capability to be surfaced through multiple channels
