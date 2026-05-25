# DECISIONS.md

## Overview

This document explains the key architectural and product decisions made while building the ESG ingestion prototype, including assumptions, simplifications, and tradeoffs made under the assignment time constraints.

---

## Why CSV-Based Ingestion?

I chose CSV uploads as the primary ingestion mechanism for all three source types.

Reasons:
- Enterprise exports are frequently shared operationally as CSV or Excel files
- CSV ingestion allows rapid prototyping of heterogeneous schemas
- CSVs are easier for analysts to manually inspect and debug
- Building stable API integrations for SAP or travel vendors would add integration complexity without improving the ingestion architecture being evaluated

---

## SAP Ingestion Decision

Research Considered:
- SAP IDoc
- OData services
- Flat-file exports
- BAPI integrations

Chosen Approach:
CSV-based flat-file export simulation.

Why:
In many organizations, sustainability teams do not directly integrate with SAP APIs. Instead, procurement or finance teams often export transactional reports into CSV or Excel files for downstream processing.

The prototype focuses on handling:
- inconsistent units
- normalization
- ingestion traceability
- audit review workflow

rather than enterprise SAP connectivity.

Handled:
- fuel quantity normalization
- unit conversion
- suspicious quantity detection

Ignored:
- multilingual headers
- plant code mappings
- asynchronous SAP extraction jobs
- SAP authentication flows

---

## Utility Data Decision

Chosen Approach:
CSV export ingestion.

Why:
Many facilities teams retrieve electricity usage data from utility portals manually as CSV or spreadsheet exports.

This was selected over PDF OCR because:
- OCR pipelines significantly increase implementation complexity
- OCR quality and bill variability require extensive preprocessing
- the assignment emphasis appeared to be ingestion modeling rather than document extraction

Handled:
- billing periods
- kWh normalization
- electricity emissions calculations

Ignored:
- tariff structures
- demand charges
- multi-meter aggregation
- utility-specific APIs

---

## Travel Data Decision

Chosen Approach:
CSV ingestion simulating exports from travel platforms such as Concur or Navan.

Why:
Corporate travel systems often expose exports containing:
- employee
- travel mode
- airport/location codes
- trip distances

The prototype focuses on:
- travel categorization
- emission factor assignment
- Scope 3 normalization

Handled:
- flights
- cab travel
- hotel stays

Ignored:
- real airline routing
- seat-class adjustments
- radiative forcing calculations
- travel booking APIs

---

## Why Separate Raw and Normalized Layers?

I intentionally separated:
- RawRecord
- EmissionRecord

Reasons:
- preserve source-of-truth data
- support future reprocessing
- improve audit traceability
- isolate ingestion from normalization logic

This pattern is commonly used in ETL and data warehouse pipelines.

---

## Why Suspicious Detection Happens During Ingestion

Suspicious records are flagged during normalization rather than after approval.

Reasons:
- analysts should review anomalous records early
- ingestion is the point where unit inconsistencies and unrealistic values are most visible
- improves analyst workflow efficiency

Examples:
- negative fuel quantities
- very high electricity consumption
- unusually long travel distances

---

## Why SQLite Was Used

SQLite was chosen for the prototype because:
- setup simplicity
- fast local iteration
- low operational overhead

For production scale, PostgreSQL would be more appropriate.

---

## Why Authentication Was Kept Minimal

The prototype focuses on:
- ingestion architecture
- normalization workflow
- analyst review process

A production system would require:
- RBAC
- SSO
- audit permissions
- organization-level access control

These were intentionally deprioritized due to assignment scope and time constraints.

---

## Questions I Would Ask the PM

If this were a real production onboarding, I would clarify:

- expected ingestion volumes
- whether uploads are batch or streaming
- expected SLA for ingestion processing
- audit retention requirements
- source system ownership
- whether analysts can edit normalized records
- whether emission factors are configurable per client
- whether historical reprocessing is required