# Process Overview

## Purpose

This project models a common business workflow: employees need sales reports for presentations, planning, performance reviews, or customer conversations, but the data lives behind several tools and conventions that are hard for occasional users to navigate.

Today, those requests are often handled by a human analyst. The analyst reads an email or message, interprets what the requester probably means, asks follow-up questions, checks whether the requester is allowed to see the requested data, uses reporting tools to produce an extract, and sends the result back.

The proposed agentic workflow keeps the same business shape, but makes the process explicit:

```text
Unstructured request
  -> structured report request
  -> completeness check
  -> policy and entitlement check
  -> deterministic report generation
  -> response and audit trail
```

The aim is not to replace all business intelligence tooling. The aim is to demonstrate how a documented, bounded request process can be made portable across agent platforms and business channels.

## Business Scenario

The fictional organization has a sales dataset used for management reporting. Different departments need recurring but slightly varied extracts:

- sales by region for a quarterly review
- revenue and gross margin by product category
- monthly trend for a board presentation
- top customers or products for a sales meeting
- raw filtered rows for operational follow-up

Several user-facing BI tools have been introduced over time, but each department still relies on a small number of people who know where the right data lives and how to produce the right extract. The organization creates a new intake channel for sales-data requests, initially represented as email fixtures in this portfolio project.

## Process Boundary

The process starts when a request arrives through an intake channel. In v1, this is simulated as a plain-text inbound request.

The process ends when one of these outcomes is produced:

- a completed report file and response
- a clarification request
- a rejection with explanation
- an approval-required response

Clarification is a final outcome for a single processing run. That may feel slightly unintuitive because the business conversation is not over. The reason is that the system has done all it safely can with the information available. When the requester replies with the missing details, that reply becomes a new inbound event. If the reply keeps the original email thread intact, the system can correlate it with the earlier request, merge the new information, and run the process again. If the clarification is adequate, the second run takes the report-generation path instead of the clarification path.

The process does not include real mailbox integration, real outbound email, production identity management, or live BI-platform access. Those are deployment concerns and are intentionally outside the first slice.

## Web Form Versus Agent

For a single narrow request type, a web form may be the better implementation. It is cheaper to validate, simpler to govern, and easier to support.

The agentic pattern becomes useful when the organization has many related request types spread across inconsistent channels and tools. Employees may not know whether their request belongs in a BI tool, a spreadsheet, an email alias, a SharePoint form, a ticket queue, or a Teams message. The agentic intake layer can normalize those requests into a common contract.

This project therefore treats the sales-report workflow as one vertical slice of a broader pattern:

```text
Email / Teams / form / ticket / spreadsheet row
  -> request interpretation
  -> common structured request schema
  -> policy and entitlement checks
  -> deterministic fulfilment tools
  -> auditable response
```

The portfolio point is not "chat is better than forms." The point is that a documented request-processing capability can survive changes in channel, vendor, and user interface.

## Agentic Responsibilities

The agentic layer is responsible for:

- interpreting natural-language requests
- extracting a structured report request
- identifying missing or ambiguous information
- choosing the appropriate process outcome
- calling deterministic tools for policy checks and report generation
- drafting a response that explains assumptions, filters, exclusions, and next steps

The agentic layer is not responsible for:

- inventing data
- calculating metrics directly in natural language
- bypassing policy
- deciding access from vibes
- creating arbitrary SQL over unknown schemas
- silently changing the requested scope

## Deterministic Responsibilities

Deterministic code is responsible for:

- validating structured request fields
- checking permissions and policy rules
- filtering and aggregating sales data
- generating CSV/XLSX files
- producing audit events
- comparing outputs against evaluation fixtures

This division is central to the design. The model handles interpretation. Code handles calculation, permissions, and evidence.

## Target Outcomes

A successful implementation should demonstrate:

- a clear manual baseline
- explicit inputs and outputs
- visible policy controls
- clarification behavior
- repeatable report generation
- portable business logic
- evaluation cases that can be reused across vendor-specific implementations

## Non-Goals

The first version will not attempt to build:

- a general BI assistant
- a dashboarding platform
- a natural-language SQL engine
- a production email processor
- real enterprise row-level security
- real Microsoft 365 tenant deployment
- complex multi-agent choreography
