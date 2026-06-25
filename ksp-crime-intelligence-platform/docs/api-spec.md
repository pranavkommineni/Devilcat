# API Specification - KSP Crime Intelligence Platform

## Base URL

```
https://api.crime-intelligence.local/api/v1
```

## Authentication

All endpoints require Bearer token authentication:

```
Authorization: Bearer <access_token>
```

## Response Format

All responses follow a standard format:

```json
{
  "success": true,
  "data": { /* endpoint-specific data */ },
  "message": "Operation successful",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Error Responses

```json
{
  "success": false,
  "error": {
    "code": "ERR_CODE",
    "message": "Human-readable error message",
    "details": { /* additional context */ }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## FIR Endpoints

### Create FIR

```
POST /fir
Content-Type: application/json

{
  "fir_number": "string (auto-generated)",
  "date_of_event": "2024-01-15T10:30:00Z",
  "crime_data": {
    "offense_code": "420",
    "offense_description": "Fraud case",
    "modus_operandi": "Online scam",
    "severity_level": "Medium"
  },
  "location": {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "district": "Bangalore",
    "police_station": "Koramangala PS"
  },
  "suspect_ids": ["uuid1", "uuid2"],
  "victim_ids": ["uuid3"],
  "notes": "Initial investigation notes"
}

Response: 201 Created
{
  "id": "uuid",
  "fir_number": "KA-2024-001234",
  "status": "Under Investigation",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Get FIR by ID

```
GET /fir/{fir_id}

Response: 200 OK
{
  "id": "uuid",
  "fir_number": "KA-2024-001234",
  "date_of_event": "2024-01-15T10:30:00Z",
  "crime_data": { ... },
  "linked_suspects": [...],
  "linked_victims": [...],
  "evidence_files": [...]
}
```

### Update FIR

```
PATCH /fir/{fir_id}
Content-Type: application/json

{
  "status": "Closed",
  "notes": "Updated investigation notes",
  "linked_suspects": ["uuid_new"]
}

Response: 200 OK
```

### List FIRs

```
GET /fir?district=Bangalore&status=Under Investigation&limit=50&offset=0

Query Parameters:
  - district: string (optional)
  - status: string (optional)
  - severity: string (optional)
  - date_from: ISO 8601 (optional)
  - date_to: ISO 8601 (optional)
  - limit: integer (default: 20, max: 100)
  - offset: integer (default: 0)

Response: 200 OK
{
  "items": [...],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

## Suspect Endpoints

### Create Suspect

```
POST /suspects
Content-Type: application/json

{
  "name": "Rajesh Kumar",
  "aliases": ["Raja", "RK"],
  "personal_info": {
    "date_of_birth": "1985-06-15",
    "gender": "M",
    "religion": "Hindu"
  },
  "criminal_profile": {
    "modus_operandi": "Online fraud",
    "specialization": "Financial crimes",
    "danger_level": "High"
  }
}

Response: 201 Created
```

### Search Suspects

```
GET /suspects/search?q=Rajesh&district=Bangalore

Query Parameters:
  - q: string (name/alias search)
  - district: string (optional)
  - modus_operandi: string (optional)
  - danger_level: string (optional)

Response: 200 OK
{
  "items": [...]
}
```

### Get Suspect Network

```
GET /suspects/{suspect_id}/network?depth=2

Query Parameters:
  - depth: integer (1-3, default: 2)
  - relationship_type: string (optional)

Response: 200 OK
{
  "suspect": { ... },
  "connections": [
    {
      "target_suspect": { ... },
      "relationship": "Criminal Partner",
      "strength": 0.85,
      "common_cases": 3
    }
  ]
}
```

## Analytics Endpoints

### Hotspot Analysis

```
GET /analytics/hotspots

Query Parameters:
  - district: string (required)
  - date_from: ISO 8601 (optional)
  - date_to: ISO 8601 (optional)
  - crime_type: string (optional)
  - radius_km: integer (default: 5)

Response: 200 OK
{
  "hotspots": [
    {
      "location": {
        "latitude": 12.9716,
        "longitude": 77.5946
      },
      "intensity": 0.85,
      "crime_count": 12,
      "trend": "Increasing"
    }
  ]
}
```

### Risk Scoring

```
GET /analytics/risk-score/{suspect_id}

Response: 200 OK
{
  "suspect_id": "uuid",
  "recidivism_risk": 0.75,
  "factors": [
    "Previous arrests",
    "Pattern matches",
    "Recent activity"
  ],
  "recommendation": "Monitor closely"
}
```

### Trend Analysis

```
GET /analytics/trends

Query Parameters:
  - district: string (optional)
  - crime_type: string (optional)
  - time_period: "week|month|quarter|year" (default: month)

Response: 200 OK
{
  "trends": [
    {
      "crime_type": "Robbery",
      "prev_period": 23,
      "current_period": 31,
      "change_percent": 34.8,
      "status": "Increasing"
    }
  ]
}
```

## Conversational AI Endpoints

### Start Investigation Chat

```
POST /ai/chat/start
Content-Type: application/json

{
  "case_id": "fir_uuid",
  "context": "Helping investigate online fraud case"
}

Response: 201 Created
{
  "session_id": "uuid",
  "conversation_id": "uuid"
}
```

### Send Message

```
POST /ai/chat/{session_id}/message
Content-Type: application/json

{
  "message": "What are common patterns for this type of crime?",
  "attachments": ["evidence_file_id"] (optional)
}

Response: 200 OK
{
  "response": "Based on the case details...",
  "suggestions": ["Link to known case", "Contact expert"],
  "confidence": 0.92
}
```

### Get MO Recommendations

```
GET /ai/mo-recommendations/{suspect_id}

Response: 200 OK
{
  "similar_cases": [
    {
      "fir_id": "uuid",
      "similarity_score": 0.88,
      "common_elements": ["Method", "Location"],
      "suspects_linked": ["uuid1", "uuid2"]
    }
  ]
}
```

## Report Generation

### Generate SCRB Report

```
POST /reports/scrb-report
Content-Type: application/json

{
  "district": "Bangalore",
  "date_range": {
    "from": "2024-01-01",
    "to": "2024-01-31"
  },
  "include_sections": [
    "Executive Summary",
    "Crime Trends",
    "Hotspot Analysis",
    "Key Suspects"
  ]
}

Response: 202 Accepted
{
  "report_id": "uuid",
  "status": "Generating",
  "estimated_completion": "2024-01-15T11:00:00Z"
}
```

### Get Report

```
GET /reports/{report_id}

Response: 200 OK
{
  "id": "uuid",
  "status": "Completed",
  "generated_at": "2024-01-15T10:45:00Z",
  "download_url": "/reports/{report_id}/download"
}
```

## File Upload/Download

### Upload Evidence

```
POST /evidence/upload
Content-Type: multipart/form-data

Form Data:
  - fir_id: string (required)
  - file: binary (required)
  - evidence_type: string (photo|video|document|audio)
  - description: string (optional)

Response: 201 Created
{
  "file_id": "uuid",
  "status": "Uploaded",
  "processing_status": "Scanning"
}
```

### Download Evidence

```
GET /evidence/{file_id}/download

Response: 200 OK (binary file)
Headers:
  Content-Type: image/jpeg
  Content-Disposition: attachment; filename="evidence.jpg"
```

## Admin Endpoints

### User Management

```
POST /admin/users
{
  "name": "Officer John",
  "email": "john@police.gov.in",
  "role": "Investigator",
  "assigned_station": "Koramangala PS"
}

GET /admin/users
GET /admin/users/{user_id}
PATCH /admin/users/{user_id}
DELETE /admin/users/{user_id}

Response varies based on endpoint
```

### Audit Logs

```
GET /admin/audit-logs
Query Parameters:
  - user_id: string (optional)
  - action: string (optional)
  - date_from: ISO 8601 (optional)
  - date_to: ISO 8601 (optional)
  - limit: integer (default: 100)

Response: 200 OK
{
  "logs": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "user_id": "uuid",
      "action": "FIR_CREATED",
      "resource_id": "fir_uuid",
      "status": "Success"
    }
  ]
}
```

## Rate Limiting

- Default: 1000 requests/minute per user
- Burst: 50 requests/second
- Headers returned:
  - `X-RateLimit-Limit`: 1000
  - `X-RateLimit-Remaining`: 950
  - `X-RateLimit-Reset`: 1705316400

## Pagination

Standard pagination parameters:
- `limit`: Number of results (default: 20, max: 100)
- `offset`: Starting position (default: 0)

Response includes:
- `total`: Total number of items
- `limit`: Items per page
- `offset`: Current offset
- `items`: Array of results

---

For interactive API documentation, visit `/docs` (Swagger UI) or `/redoc` (ReDoc)
