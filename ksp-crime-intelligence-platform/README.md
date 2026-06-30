# 🚔 CrimeLens AI
### AI-Powered Crime Intelligence & Investigation Platform

> **Transforming crime records into actionable intelligence using Artificial Intelligence, Machine Learning, and Zoho Catalyst.**

---

## 📌 Problem Statement

Law enforcement agencies manage vast amounts of crime-related information such as FIRs, victim details, suspect records, evidence, financial transactions, and geographical data. These datasets are often scattered across different systems, making investigations slow, manual, and difficult to analyze.

CrimeLens AI provides a centralized intelligence platform that automates crime analysis, uncovers hidden criminal relationships, predicts crime patterns, and assists investigators through conversational AI.

---

# 🚀 Our Solution

CrimeLens AI combines AI, analytics, and cloud technologies to help investigators:

- 📄 Digitize and manage FIR records
- 🤖 Interact with crime data using natural language
- 🔍 Discover criminal relationships
- 📊 Analyze crime trends and hotspots
- 📈 Predict future crime patterns
- 🗺️ Visualize crimes on interactive maps
- 📑 Generate automated investigation reports

---

# 🏗️ System Architecture

```text

                   ┌──────────────────────────┐
                   │ Karnataka Police Data    │
                   │ FIR • Victims • Crime    │
                   │ CDR • Finance • GIS      │
                   └─────────────┬────────────┘
                                 │
                     Data Ingestion Pipeline
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
 Structured DB             Graph Database          Feature Store
(PostgreSQL)                 (Neo4j)                (Redis)
        │                        │                        │
        └──────────────┬─────────┴─────────────┬──────────┘
                       │                       │
              AI Intelligence Engine     Analytics Engine
                       │                       │
         ┌─────────────┼───────────────────────┼─────────────┐
         │             │                       │             │
 Conversational AI  Pattern Mining      ML Prediction   Explainable AI
         │             │                       │             │
         └─────────────┼───────────────────────┼─────────────┘
                       │
          Intelligence API Gateway (FastAPI)
                       │
     ┌─────────────────┼────────────────────┐
     │                 │                    │
 Investigator      Analyst Portal     Admin Portal
 Dashboard          Dashboard          Management
```


# Folder Architecture:
ksp-crime-intelligence-platform/
├── catalyst.json                      # Catalyst project manifest (required)
├── .env.example
├── README.md
│
├── client/                            # ⚠️ Catalyst CLI expects this exact name
│   ├── investigator-portal/           # React + TS + Tailwind (case work, MO lookup, AI assistant)
│   ├── analyst-portal/                # SCRB-level dashboards, trend/hotspot maps, link analysis
│   ├── admin-portal/                  # User/role management, audit logs, system config
│   └── shared/
│       ├── components/                # buttons, tables, map widgets, network-graph viewer
│       ├── hooks/                     # useAuth, useCatalystSDK, useWebSocket(Signals)
│       ├── lib/
│       │   ├── api-client/            # typed FastAPI/API Gateway client
│       │   └── catalyst-sdk/          # Catalyst Web SDK init (auth, cache, search)
│       ├── types/                     # shared TS interfaces (FIR, Suspect, GraphNode...)
│       └── styles/                    # tailwind.config.ts, design tokens
│
├── functions/                         # ⚠️ Catalyst Functions (event/serverless logic)
│   ├── fir_ingestion_trigger/         # fires on new FIR record / file upload
│   ├── ocr_document_intel/            # Zia AI OCR on Stratus uploads
│   ├── anomaly_alert_dispatcher/      # Signals-driven real-time alerts
│   ├── scheduled_intel_reports/       # Job Scheduling — daily/weekly SCRB reports
│   └── circuits_workflows/            # Circuits automation step handlers
│
├── backend/                           # FastAPI app, deployed via AppSail
│   ├── appsail.config.json
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── core/                      # config, security, catalyst_client.py
│       ├── auth/                      # Catalyst Authentication + RBAC (Investigator/Analyst/Admin)
│       │
│       ├── api/v1/endpoints/
│       │   ├── fir.py / victims.py / crime.py / cdr.py / finance.py / gis.py
│       │   ├── network_analysis.py    # link analysis, MO matching endpoints
│       │   ├── predictive.py          # risk scoring, hotspot forecasts
│       │   ├── conversational_ai.py   # ConvoKraft investigation assistant
│       │   └── admin.py
│       │
│       ├── ingestion/                 # Data Ingestion Pipeline
│       │   ├── connectors/            # excel_importer, fir_sync, cdr_parser, gis_loader
│       │   ├── validators/
│       │   └── pipeline.py
│       │
│       ├── data_access/               # repository layer over Catalyst services
│       │   ├── datastore_repo.py      # Catalyst Data Store (structured records)
│       │   ├── graph_repo.py          # graph-modeled tables (suspects↔victims↔locations)
│       │   ├── cache_repo.py          # Catalyst Cache (dashboard speed)
│       │   └── stratus_repo.py        # evidence files (images/videos/PDFs)
│       │
│       ├── ai_engine/                 # "AI Intelligence Engine" block
│       │   ├── conversational/        # convokraft_client.py, intent parsing
│       │   ├── pattern_mining/        # MO clustering, association rules
│       │   ├── prediction/            # QuickML + scikit-learn risk models
│       │   └── explainability/        # SHAP / feature-importance for XAI
│       │
│       ├── analytics_engine/          # "Analytics Engine" block
│       │   ├── spatiotemporal/        # hotspot detection, district drill-down
│       │   ├── network_analysis/      # centrality, repeat-offender graphs
│       │   ├── socioeconomic/         # crime vs. urbanization/census overlays
│       │   └── trend_discovery/       # emerging-trend / spike detection
│       │
│       ├── models/                    # Pydantic/data models (FIR, Suspect, GraphNode...)
│       ├── schemas/                    # request/response DTOs
│       ├── services/                   # business logic orchestration
│       ├── utils/
│       └── tests/
│
├── ml/                                 # offline training (feeds QuickML/Zia, not deployed live)
│   ├── notebooks/
│   ├── training/
│   │   ├── risk_scoring/
│   │   ├── anomaly_detection/
│   │   └── mo_clustering/
│   ├── feature_engineering/
│   └── model_registry/                 # exported models pushed to QuickML
│
├── infra/
│   ├── api-gateway/                    # route + policy definitions
│   ├── signals/                        # event topic definitions
│   ├── circuits/                       # workflow definitions
│   └── scripts/                        # deploy.sh, seed_data.sh
│
├── docs/
│   ├── architecture.md
│   ├── data-model.md                   # how Neo4j-style graph maps onto Data Store
│   ├── api-spec.md                     # OpenAPI export
│   └── security-rbac.md
│
└── tests/
    ├── integration/
    └── e2e/

# phase 0 architecture:
ksp-crime-intelligence-platform/
├── catalyst.json
├── .env.example
├── README.md
│
├── docs/
│   └── data-model.md                  # edge-table design doc
│
└── backend/
    ├── requirements.txt
    ├── appsail.config.json
    │
    └── app/
        ├── __init__.py
        ├── main.py                    # FastAPI entrypoint
        │
        ├── core/
        │   ├── __init__.py
        │   ├── config.py              # env settings
        │   ├── catalyst_client.py     # Catalyst SDK init
        │   └── security.py            # JWT + password hashing
        │
        ├── auth/
        │   ├── __init__.py
        │   ├── roles.py                # RBAC role/permission table
        │   └── dependencies.py         # require_permission / require_role
        │
        ├── models/
        │   ├── __init__.py
        │   ├── enums.py                # CaseStatus, CrimeCategory, GraphNodeType, GraphEdgeType
        │   ├── location.py             # Location
        │   ├── person.py               # Suspect, Victim
        │   ├── fir.py                  # FIR, Incident
        │   └── graph.py                # GraphNode, GraphEdge
        │
        ├── schemas/
        │   ├── __init__.py
        │   └── auth.py                 # TokenResponse
        │
        ├── data_access/
        │   ├── __init__.py
        │   ├── datastore_repo.py       # generic CRUD over Catalyst Data Store
        │   ├── graph_repo.py           # edge-table adjacency queries
        │   ├── cache_repo.py           # Catalyst Cache wrapper
        │   └── stratus_repo.py         # evidence file storage wrapper
        │
        └── api/
            ├── __init__.py
            └── v1/
                ├── __init__.py
                ├── router.py            # aggregates all endpoint routers
                └── endpoints/
                    ├── __init__.py
                    ├── health.py        # /health
                    ├── auth.py          # /auth/login
                    └── fir.py           # /fir CRUD
# 🛠️ Tech Stack

### Frontend

- React.js
- Tailwind CSS
- TypeScript

### Backend

- FastAPI
- Python

### Database

- Zoho Catalyst Data Store
- Zoho Catalyst Cache

### Storage

- Zoho Catalyst Stratus

### AI & ML

- Zoho Catalyst Zia AI
- ConvoKraft
- QuickML
- Scikit-learn

### Deployment

- Zoho Catalyst AppSail
- Zoho Catalyst API Gateway

---

# ☁️ Zoho Catalyst Services Used

| Service | Purpose |
|----------|---------|
| Data Store | Crime records database |
| Stratus | Store evidence (images, videos, PDFs) |
| Cache | Faster dashboard and search |
| Authentication | Secure login & role management |
| Functions | Serverless backend logic |
| AppSail | Backend & frontend hosting |
| API Gateway | Secure API access |
| Search | Intelligent crime search |
| Zia AI | OCR & document intelligence |
| ConvoKraft | AI Investigation Assistant |
| QuickML | Crime prediction models |
| Signals | Event-driven processing |
| Circuits | Workflow automation |
| Job Scheduling | Automated reports |

---

# ✨ Key Features

## 📂 Crime Management

- FIR Management
- Victim & Suspect Records
- Evidence Management
- Case Tracking

---

## 🤖 AI Investigation Assistant

Ask questions like:

- Show robbery cases in Bengaluru
- Find repeat offenders
- Search FIR by suspect
- List similar crime cases
- Show crimes near a location

---

## 📊 Crime Analytics

- Crime Trends
- District-wise Statistics
- Case Status
- Crime Distribution
- Interactive Dashboards

---

## 🗺️ Crime Intelligence

- Crime Hotspots
- Interactive Maps
- Timeline Analysis
- Criminal Relationship Network

---

## 🧠 Predictive Analytics

- Crime Hotspot Prediction
- Repeat Offender Prediction
- Case Priority Analysis
- Crime Trend Forecasting

---

## 📄 Smart Document Processing

- OCR for FIR Documents
- Automatic Data Extraction
- Evidence Upload
- PDF Report Generation

---

# 🔄 Workflow

```text
Crime Data
      │
      ▼
Data Ingestion
      │
      ▼
Data Validation & Storage
      │
      ▼
AI Analysis
      │
      ▼
Prediction & Analytics
      │
      ▼
Investigator Dashboard
```

---

# 📁 Project Structure

```
CrimeLens-AI/

├── frontend/
├── backend/
├── datasets/
├── docs/
└── README.md
```

---

# 🔒 Security

- Role-Based Access Control
- Secure Authentication
- Protected APIs
- Audit Logging
- Secure Evidence Storage

---

# 🌟 Future Enhancements

- Facial Recognition
- Vehicle Number Plate Detection
- Real-time CCTV Analytics
- Voice-based AI Assistant
- Mobile Investigator App
- Cross-State Crime Intelligence

---

# 🚀 Development Roadmap

## Phase 0 — Project Setup *(Day 1)*

Get the project skeleton running before writing any application logic.

```
catalyst.json
```

* Define Catalyst project
* Configure Data Store
* Configure Cache
* Configure Stratus
* Configure Authentication

```
catalyst init
```

Generates the base project structure:

```
client/
functions/
```

```
backend/requirements.txt
```

Install project dependencies:

* FastAPI
* Uvicorn
* Pydantic
* python-jose
* scikit-learn
* pandas
* zcatalyst-sdk

```
backend/app/main.py
```

* Bare FastAPI application
* Health Check endpoint only

```
backend/appsail.config.json
```

Configure AppSail deployment.

```
.env.example
```

Contains:

* Catalyst Project ID
* Environment
* Zone
* Required Keys

---

# Phase 1 — Authentication & Data Model *(Week 1)*

Everything in the platform depends on authentication and a well-designed data model.

```
backend/app/auth/
```

* Catalyst Authentication
* JWT Authentication
* Role Middleware
* Investigator
* Analyst
* Administrator

```
backend/app/models/
```

Create Pydantic models:

* FIR
* Victim
* Suspect
* Incident
* Location
* GraphEdge

```
docs/data-model.md
```

Finalize:

* Data Store Tables
* Columns
* Relationships
* Primary Keys
* Indexes

This becomes the most important design document because Catalyst Data Store is not a graph database. The edge-table design determines all downstream analytics.

```
backend/app/data_access/datastore_repo.py
```

CRUD operations against Catalyst Data Store.

```
backend/app/data_access/graph_repo.py
```

Relationship and adjacency queries.

Example:

```
Suspect ↔ Incident ↔ Location
```

---

# Phase 2 — Data Ingestion Pipeline *(Week 2)*

Replace manual Excel workflows with an automated ingestion pipeline.

```
backend/app/ingestion/validators/
```

Validate incoming:

* FIR
* CDR
* Financial Records
* GIS Data

```
backend/app/ingestion/connectors/
```

Implement:

* excel_importer.py
* fir_sync.py
* cdr_parser.py
* gis_loader.py

```
backend/app/ingestion/pipeline.py
```

Pipeline Flow

```
Connector
      ↓
Validator
      ↓
Transformation
      ↓
Catalyst Data Store
```

```
functions/fir_ingestion_trigger/
```

Catalyst Function triggered through:

* Signals
* Stratus Upload Events

```
infra/scripts/seed_data.sh
```

Populate sample datasets for development.

---

# Phase 3 — Core CRUD API *(Week 2–3)*

Build the REST layer before introducing AI.

```
backend/app/api/v1/endpoints/
```

Endpoints:

* fir.py
* victims.py
* crime.py
* cdr.py
* finance.py
* gis.py

```
backend/app/schemas/
```

Request / Response DTOs.

```
backend/app/services/
```

Business logic layer.

```
infra/api-gateway/
```

Configure Catalyst API Gateway.

```
docs/api-spec.md
```

Export FastAPI OpenAPI specification.


---

# Phase 4 — Analytics Engine *(Week 3–4)*

Build deterministic analytics before machine learning.

```
backend/app/analytics_engine/spatiotemporal/
```

* Crime Hotspot Detection
* Time × Location Clustering

```
backend/app/analytics_engine/trend_discovery/
```

* Crime Spike Detection
* Historical Trend Analysis

```
backend/app/analytics_engine/network_analysis/
```

* Repeat Offenders
* Criminal Networks
* Centrality Analysis

```
backend/app/analytics_engine/socioeconomic/
```

Overlay demographic or census data with crime statistics.

```
backend/app/api/v1/endpoints/network_analysis.py
```

Expose criminal relationship APIs.


---

# Phase 5 — Frontend: Analyst & Investigator Portals *(Week 4–5)*

Build dashboards using the completed backend APIs.

```
client/shared/lib/catalyst-sdk/
```

Configure:

* Authentication
* API Client

```
client/shared/components/
```

Reusable Components:

* Map Widget
* Crime Table
* Network Graph
* Charts

```
client/analyst-portal/
```

Features:

* District Dashboard
* Heatmaps
* Trend Alerts
* Analytics

```
client/investigator-portal/
```

Features:

* Case Search
* FIR Viewer
* Suspect Profile
* Investigation Timeline


---

# Phase 6 — AI & Machine Learning *(Week 5–7)*

Train and integrate prediction models using real investigation data.

```
ml/feature_engineering/
```

Generate features from ingested datasets.

```
ml/training/
```

Train:

* Risk Scoring
* Crime Prediction
* Anomaly Detection
* Modus Operandi Clustering

```
ml/model_registry/
```

Deploy models using QuickML.

```
backend/app/ai_engine/prediction/
```

Prediction Service.

```
backend/app/ai_engine/explainability/
```

Explainable AI using:

* SHAP
* Feature Importance

```
backend/app/api/v1/endpoints/predictive.py
```

Expose prediction endpoints.

---

# Phase 7 — Conversational AI *(ConvoKraft)* *(Week 7)*

Build an AI-powered investigation assistant.

```
backend/app/ai_engine/conversational/
```

Implement:

```
convokraft_client.py
```

```
backend/app/api/v1/endpoints/conversational_ai.py
```

Route natural language queries to:

* FIR Search
* Criminal Networks
* Predictive Analytics
* Investigation Data

```
functions/ocr_document_intel/
```

Use Zia AI OCR for:

* FIR Documents
* Scanned Reports
* Case Files

Integrate into:

```
client/investigator-portal/
```

As the **AI Investigation Assistant**.


---

# Phase 8 — Admin Portal, Automation & Production Hardening *(Week 8)*

Complete the platform with administration, automation, and testing.

```
client/admin-portal/
```

Features:

* User Management
* Role Management
* Permissions
* Monitoring

```
backend/app/api/v1/endpoints/admin.py
```

Administrative APIs.

```
infra/circuits/
infra/signals/
```

Workflow automation.

```
functions/scheduled_intel_reports/
```

Generate scheduled intelligence reports.

```
functions/anomaly_alert_dispatcher/
```

Automatic crime anomaly alerts.

```
tests/integration/
tests/e2e/
```

Perform:

* Integration Testing
* End-to-End Testing

```
docs/security-rbac.md
```

Finalize RBAC policies and perform security audit.
