# SOURCES.md

## Overview

This document explains the real-world ESG data source formats researched for the prototype, the ingestion assumptions made, and the limitations of the simplified implementation.

The prototype intentionally models realistic enterprise data inconsistencies while keeping the ingestion system manageable within the assignment scope.

---

# 1. SAP Fuel and Procurement Data

## Research Conducted

I reviewed common SAP integration/export patterns including:
- SAP IDoc
- SAP OData services
- flat-file exports
- procurement transaction exports

I found that many operational sustainability workflows still rely heavily on CSV or Excel exports generated from SAP transaction reports rather than direct API integrations.

---

## Chosen Format

CSV flat-file export.

Example columns:
- material_code
- fuel_type
- quantity
- unit
- posting_date
- plant_code

---

## Realistic Challenges Observed

SAP exports are often inconsistent:
- units vary (L vs KL)
- plant codes require lookup mappings
- procurement naming conventions differ by business unit
- date formats vary
- some deployments expose multilingual headers

---

## What The Prototype Handles

- fuel quantity normalization
- KL → L conversion
- ingestion traceability
- suspicious quantity detection
- Scope 1 categorization

---

## What Would Break in Production

The prototype does not yet handle:
- multilingual field mappings
- SAP authentication
- streaming ingestion
- asynchronous extraction jobs
- procurement classification hierarchies
- duplicate reconciliation logic

---

# 2. Utility Electricity Data

## Research Conducted

I reviewed how facilities and sustainability teams commonly retrieve electricity data.

In many organizations, utility data is exported manually from:
- utility provider portals
- spreadsheet reports
- monthly billing exports

I also evaluated PDF bill ingestion workflows.

---

## Chosen Format

CSV utility export.

Example columns:
- meter_id
- billing_start
- billing_end
- kwh
- cost

---

## Why CSV Was Chosen Over OCR

PDF OCR pipelines introduce:
- layout variability
- extraction accuracy issues
- preprocessing complexity

Since the assignment focused more on ingestion architecture than document extraction, CSV exports were selected as the most practical operational format.

---

## Realistic Challenges Observed

Utility datasets often contain:
- inconsistent billing periods
- overlapping meter readings
- tariff-specific calculations
- missing consumption intervals
- unit inconsistencies

---

## What The Prototype Handles

- kWh normalization
- Scope 2 categorization
- electricity emission calculations
- suspicious usage detection

---

## What Would Break in Production

The prototype does not yet support:
- multi-meter aggregation
- tariff modeling
- demand charges
- utility APIs
- interval-based consumption data
- OCR invoice ingestion

---

# 3. Corporate Travel Data

## Research Conducted

I reviewed how platforms such as:
- Concur
- Navan
- corporate travel exports

typically expose travel activity data.

Common exports contain:
- employee identifiers
- travel mode
- airport/location codes
- trip distances
- booking categories

---

## Chosen Format

CSV travel export.

Example columns:
- employee
- mode
- from_location
- to_location
- distance_km

---

## Realistic Challenges Observed

Travel emissions are difficult because:
- distances are sometimes missing
- airport codes may require geolocation lookup
- travel classes affect emissions
- hotel emissions vary by geography
- ground transport categories are inconsistent

---

## What The Prototype Handles

- flight travel
- cab travel
- hotel stays
- Scope 3 categorization
- distance-based emissions calculation

---

## What Would Break in Production

The prototype does not yet support:
- airline routing logic
- seat-class multipliers
- radiative forcing calculations
- travel booking APIs
- hotel-specific emissions databases
- airport geocoding systems

---

# Summary

The prototype intentionally prioritizes:
- ingestion architecture
- normalization workflows
- audit traceability
- analyst review

over production-grade vendor integrations.

The chosen formats reflect realistic operational ESG workflows while remaining feasible within the assignment timeline.