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
