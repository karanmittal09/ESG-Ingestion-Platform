# TRADEOFFS.md

## Overview

This prototype intentionally prioritizes ingestion architecture, normalization workflows, and audit traceability over production-scale infrastructure and integrations.

Several features were deliberately excluded due to time constraints and assignment scope.

---

## 1. No Real-Time External Integrations

Not Built:
- live SAP integrations
- Concur/Navan APIs
- utility provider APIs

Why:
The assignment focused more on ingestion architecture and normalization logic than vendor-specific authentication and API integration complexity.

Instead, I modeled realistic enterprise exports using CSV ingestion workflows.

Tradeoff:
The prototype demonstrates ingestion behavior realistically but does not handle real-time synchronization.

---

## 2. No OCR-Based Utility Bill Processing

Not Built:
- PDF parsing
- OCR extraction pipelines

Why:
OCR introduces significant complexity:
- inconsistent utility bill layouts
- extraction accuracy issues
- preprocessing requirements

I intentionally chose CSV-based utility exports because they are operationally common and allowed me to focus on auditability and normalization workflows.

Tradeoff:
The platform currently assumes structured electricity exports rather than scanned invoices.

---

## 3. No Asynchronous Processing Pipeline

Not Built:
- Celery
- Redis queues
- background workers

Why:
The ingestion volumes in the prototype are small enough for synchronous processing.

Adding distributed job infrastructure would increase operational complexity without materially improving the architecture being evaluated.

Tradeoff:
Large enterprise uploads would eventually require asynchronous ingestion and retry mechanisms.

---

## 4. Simplified Emission Factor Logic

Not Built:
- configurable emission factor libraries
- region-specific calculations
- dynamic GHG databases

Why:
The assignment focus appeared to be ingestion and workflow design rather than emissions science accuracy.

The prototype uses simplified static emission factors to demonstrate normalization flow.

Tradeoff:
Production systems would require versioned and region-aware emissions datasets.

---

## 5. Minimal Authentication and Authorization

Not Built:
- RBAC
- SSO
- tenant-level permissions
- analyst/admin roles

Why:
The prototype prioritizes ingestion workflows and review pipelines over enterprise IAM implementation.

Tradeoff:
The current system is not production-secure for multi-user enterprise access.

---

## 6. No Historical Reprocessing Framework

Not Built:
- replay pipelines
- ingestion versioning
- transformation version history

Why:
The RawRecord layer preserves enough source fidelity for future reprocessing, but a complete replay framework was outside the assignment scope.

Tradeoff:
Transformation logic updates would currently require manual migration/reprocessing steps.

---

## 7. SQLite Instead of PostgreSQL

Chosen:
SQLite

Instead of:
PostgreSQL

Why:
SQLite enabled faster local setup and development iteration during the prototype phase.

Tradeoff:
SQLite would not be appropriate for high-concurrency enterprise ingestion workloads.