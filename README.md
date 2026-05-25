# ESG Ingestion Platform

A prototype ESG ingestion and audit workflow platform built using Django REST Framework and React.

The platform ingests emissions-related data from multiple enterprise source systems, normalizes records into a common structure, flags suspicious entries, and provides an analyst review workflow before audit export.

---

# Supported Data Sources

## 1. SAP Fuel / Procurement Data

- CSV-based SAP export simulation
- Scope 1 categorization
- Unit normalization (KL → L)
- Suspicious quantity detection

## 2. Utility Electricity Data

- Utility portal CSV export simulation
- Scope 2 categorization
- kWh normalization
- High-consumption anomaly detection

## 3. Corporate Travel Data

- Travel platform CSV export simulation
- Scope 3 categorization
- Flight / cab / hotel categorization
- Distance-based emissions calculations

---

# Features

- Multi-source ESG ingestion
- Raw source-of-truth preservation
- Normalized emissions layer
- Scope 1 / 2 / 3 categorization
- Suspicious record detection
- Analyst review queue
- Approve / reject workflow
- Audit export functionality
- Multi-tenant organization structure

---

# Tech Stack

## Backend

- Django
- Django REST Framework
- SQLite
- Pandas

## Frontend

- React
- Vite
- Tailwind CSS
- Axios

---

# Architecture Overview

```
Source Upload  
     ↓  
DataSource  
     ↓  
RawRecord  
     ↓  
EmissionRecord  
     ↓  
Analyst Review  
     ↓  
Audit Export
```

---

# Local Setup

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

The backend runs on `http://127.0.0.1:8000`

## Frontend

```bash
cd frontend

npm install

npm run dev
```

The frontend runs on `http://localhost:5173`

---

# API Endpoints

## Dashboard
- `GET /dashboard/stats/` - Get overview statistics

## Ingestion
- `POST /upload/sap/` - Upload SAP data

## Emissions Review
- `GET /emissions/review-queue/` - Get records pending review
- `PATCH /emissions/{id}/approve/` - Approve an emission record
- `PATCH /emissions/{id}/reject/` - Reject an emission record
- `GET /emissions/export/` - Export approved records for audit

---

# Usage

1. **Start Backend & Frontend** - Run setup commands above
2. **Upload Data** - Navigate to Upload Data page and select a CSV file
3. **Review Records** - Go to Review Queue to approve/reject flagged records
4. **View Dashboard** - Check Dashboard for summary statistics
5. **Export Audit** - Use Export button to download approved records