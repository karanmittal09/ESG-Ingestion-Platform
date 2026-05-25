# MODEL.md

## Overview

The system is designed to ingest ESG-related emissions data from multiple enterprise data sources, normalize the data into a consistent structure, and provide an analyst review workflow before audit approval.

The architecture separates raw ingestion data from normalized emissions data to preserve source fidelity and support audit traceability.

---

## High-Level Data Flow

Source File/API
↓
DataSource
↓
RawRecord
↓
EmissionRecord
↓
Analyst Review Queue
↓
Approved Audit Export

---

## Multi-Tenancy

The Organization model represents a client company onboarded onto the platform.

All ingestion records, raw records, and emission records are tied to an organization to ensure tenant isolation.

This allows multiple enterprise clients to use the platform independently.

---

## DataSource Model

Purpose:
Tracks metadata about each ingestion event.

Fields:
- source_type (SAP / UTILITY / TRAVEL)
- ingestion_method (CSV)
- uploaded_by
- file_name
- uploaded_at

Why:
This provides ingestion traceability and audit visibility into where records originated.

---

## RawRecord Model

Purpose:
Stores the original unmodified payload received from source systems.

Fields:
- datasource reference
- raw_payload (JSON)
- row_number
- ingestion status

Why:
Raw enterprise exports are often inconsistent and may require reprocessing.

Keeping immutable raw records allows:
- debugging failed transformations
- replaying normalization logic
- auditor traceability
- preservation of source-of-truth data

This separation mirrors common enterprise ETL architecture patterns.

---

## EmissionRecord Model

Purpose:
Stores normalized ESG emission records used by analysts and dashboards.

Fields:
- organization
- scope classification
- activity_type
- normalized quantity
- normalized unit
- emission factor
- calculated CO2e
- suspicious flag
- review status

Why:
Source systems expose heterogeneous schemas and units.

The normalized emissions layer provides a consistent structure for:
- analytics
- dashboards
- review workflows
- audit exports

---

## Scope Categorization

The platform supports:
- Scope 1 → Fuel combustion (SAP fuel data)
- Scope 2 → Purchased electricity (Utility data)
- Scope 3 → Business travel emissions

This classification allows analysts to review emissions according to GHG Protocol reporting categories.

---

## Unit Normalization

Different sources expose inconsistent units.

Examples:
- SAP fuel exports may contain KL instead of liters
- Utility data uses kWh
- Travel data uses kilometers

Normalization converts data into consistent internal units before emissions calculations.

---

## Suspicious Record Detection

The ingestion pipeline flags suspicious records during normalization.

Examples:
- Negative fuel quantities
- Extremely high electricity consumption
- Unusually long travel distances

These records appear in the analyst review queue for manual verification.

---

## Analyst Workflow

1. Analyst uploads source data
2. Data is ingested into raw records
3. Records are normalized into emission records
4. Suspicious rows are highlighted
5. Analyst approves or rejects records
6. Approved records can be exported for audit review

---

## Auditability

The architecture was designed around audit traceability.

Every normalized emission record can be traced back to:
- source file
- upload event
- original raw payload
- upload timestamp

This supports downstream audit and compliance workflows.