# Data Model - KSP Crime Intelligence Platform

## Overview

The data model integrates both relational (SQL) and graph structures to represent criminal intelligence data, relationships, and network patterns.

## Core Entities

### FIR (First Information Report)

```
FIR {
  id: UUID
  fir_number: String (unique)
  date_of_event: DateTime
  date_of_report: DateTime
  reporting_officer: User reference
  
  location: {
    latitude: Float
    longitude: Float
    district: String
    police_station: String
    address: String
  }
  
  crime_data: {
    offense_code: String (IPC)
    offense_description: String
    modus_operandi: String
    severity_level: Enum (High/Medium/Low)
  }
  
  status: Enum (Under Investigation, Closed, Suspended)
  priority: Enum (High, Medium, Low)
  
  linked_suspects: Suspect[] (foreign keys)
  linked_victims: Victim[] (foreign keys)
  evidence_files: File[] (Stratus references)
  
  cdr_records: CDR[]
  financial_records: FinancialTransaction[]
  
  created_at: DateTime
  updated_at: DateTime
  closed_at: DateTime (nullable)
  
  tags: String[]
  notes: Text
}
```

### Suspect

```
Suspect {
  id: UUID
  name: String
  aliases: String[]
  
  personal_info: {
    date_of_birth: Date
    age: Integer
    gender: Enum (M/F/Other)
    religion: String (optional, sensitive)
    caste: String (optional, sensitive)
  }
  
  contact_info: {
    phone_numbers: String[]
    email_addresses: String[]
    addresses: Address[]
  }
  
  criminal_profile: {
    past_arrests: Integer
    past_convictions: Integer
    first_arrest_date: Date
    modus_operandi: String
    specialization: String (e.g., burglary, fraud)
    danger_level: Enum (High/Medium/Low)
    recidivism_risk_score: Float (0-100) [AI-generated]
  }
  
  associated_cases: FIR[]
  known_associates: Suspect[] (graph edges)
  known_victims: Victim[] (graph edges)
  frequent_locations: Location[]
  
  biometric_data: {
    fingerprints: Blob
    photograph: File (Stratus)
    facial_features: JSON
  }
  
  status: Enum (Active, Wanted, Arrested, Released, Deceased)
  last_location: Location
  last_seen_date: DateTime
  
  created_at: DateTime
  updated_at: DateTime
}
```

### Victim

```
Victim {
  id: UUID
  name: String
  aliases: String[]
  
  personal_info: {
    date_of_birth: Date (nullable)
    age: Integer (nullable)
    gender: Enum (M/F/Other)
    occupation: String (optional)
  }
  
  contact_info: {
    phone_numbers: String[]
    email_addresses: String[]
    address: Address
  }
  
  victim_profile: {
    victimization_type: String (robbery, assault, fraud, etc.)
    total_cases_involved: Integer
    repeat_victimization: Boolean
    vulnerability_factors: String[]
    estimated_loss: Float (currency)
  }
  
  associated_cases: FIR[]
  associated_suspects: Suspect[] (graph edges)
  
  status: Enum (Active, Deceased, Relocated, Relocated_Abroad)
  last_known_location: Location
  
  created_at: DateTime
  updated_at: DateTime
}
```

### Crime/Offense

```
Crime {
  id: UUID
  ipc_code: String (e.g., 420, 379)
  statute_reference: String
  description: String
  severity_category: Enum (Heinous, Non-heinous, Misdemeanor)
  
  typical_modus_operandi: String
  common_locations: Location[]
  seasonal_pattern: String (optional)
  
  average_investigation_days: Integer
  closure_rate: Float (0-100)
  
  created_at: DateTime
  updated_at: DateTime
}
```

### Location/Geography

```
Location {
  id: UUID
  type: Enum (Crime Scene, Residence, Business, Public Place)
  
  coordinates: {
    latitude: Float
    longitude: Float
  }
  
  address: {
    street: String
    area: String
    district: String
    state: String
    postal_code: String
  }
  
  administrative: {
    police_station: String
    jurisdiction_id: String
    ward_number: String
  }
  
  risk_profile: {
    crime_density: Integer
    last_incident_date: DateTime
    hotspot_score: Float (0-100)
    trend: Enum (Increasing, Decreasing, Stable)
  }
  
  connected_firs: FIR[]
  connected_suspects: Suspect[]
  
  created_at: DateTime
  updated_at: DateTime
}
```

### CDR (Call Detail Record)

```
CDR {
  id: UUID
  
  call_details: {
    caller_number: String
    receiver_number: String
    timestamp: DateTime
    duration_seconds: Integer
    call_type: Enum (Voice, SMS, Data)
  }
  
  location_data: {
    caller_location: Location (tower-based)
    receiver_location: Location (tower-based)
  }
  
  linked_fir: FIR reference
  linked_suspects: Suspect[]
  linked_victims: Victim[]
  
  flagged_for_review: Boolean
  review_status: Enum (Pending, Reviewed, Cleared, Suspicious)
  
  created_at: DateTime
  indexed_at: DateTime
}
```

### Financial Transaction

```
FinancialTransaction {
  id: UUID
  
  transaction_details: {
    transaction_id: String (external bank ID)
    amount: Decimal
    currency: String (INR, USD, etc.)
    timestamp: DateTime
    type: Enum (Deposit, Withdrawal, Transfer, Card Payment)
  }
  
  parties: {
    sender_account: String (masked)
    receiver_account: String (masked)
    sender_name: String (optional)
    receiver_name: String (optional)
  }
  
  institutions: {
    sender_bank: String
    receiver_bank: String
  }
  
  linked_suspect: Suspect reference
  linked_fir: FIR reference
  
  anomaly_flags: {
    is_suspicious: Boolean
    anomaly_score: Float (0-100)
    flags: String[] (e.g., "large amount", "unusual timing")
  }
  
  created_at: DateTime
}
```

### Evidence/File

```
EvidenceFile {
  id: UUID
  
  file_metadata: {
    filename: String
    file_type: String (image, video, document, audio)
    mime_type: String
    file_size_bytes: Integer
    stratus_reference: String (storage path)
  }
  
  processing: {
    status: Enum (Uploaded, Processing, Processed, Failed)
    ocr_extracted_text: Text (for documents)
    detected_objects: JSON (AI vision results)
    transcription: Text (for audio)
  }
  
  chain_of_custody: {
    uploaded_by: User reference
    upload_timestamp: DateTime
    malware_scan_status: Enum (Passed, Failed, Pending)
    scan_results: JSON
  }
  
  classification: {
    evidence_type: String (photo, video, document, etc.)
    relevance_to_case: Enum (Direct, Indirect, Supporting)
    manual_tags: String[]
    ai_generated_tags: String[]
  }
  
  linked_fir: FIR reference
  linked_suspect: Suspect reference (optional)
  linked_victim: Victim reference (optional)
  
  access_log: AccessLog[] (audit trail)
  
  created_at: DateTime
  updated_at: DateTime
}
```

## Graph Relationships (Neo4j-style)

### Relationship Types

```
SUSPECT_KNOWS_SUSPECT
  - relationship_type: Enum (Friend, Associate, Criminal Partner, Informant)
  - strength: Float (0-100) [based on co-occurrence, frequency]
  - last_interaction: DateTime
  - interaction_locations: Location[]
  - shared_firs: Integer

SUSPECT_VICTIM_OF
  - relationship_type: Enum (Robbed, Assaulted, Defrauded)
  - timestamp: DateTime
  - linked_fir: FIR reference
  - strength: Float

SUSPECT_FREQUENTS_LOCATION
  - visit_frequency: Integer
  - last_visit: DateTime
  - associated_activities: String[]
  - arrest_risk: Float

CRIME_OCCURRED_AT_LOCATION
  - timestamp: DateTime
  - modus_operandi: String

VICTIM_LOCATION
  - location_type: Enum (Residence, Workplace, Frequent)
  - primary: Boolean

CRIME_SIMILAR_MODUS
  - similarity_score: Float (0-100)
  - matching_criteria: String[]
```

## Indexes & Performance

### Primary Indexes
- FIR.fir_number (unique)
- Suspect.name (full-text)
- Location.coordinates (spatial)
- CDR.caller_number (hash)
- CDR.timestamp (range)

### Graph Indexes
- Suspect nodes (for centrality queries)
- Location nodes (for geographic queries)
- SUSPECT_KNOWS_SUSPECT edges (for path finding)

## Data Privacy & Sensitivity

### Personally Identifiable Information (PII)
- Victim information: Encrypted at rest, access logged
- Suspect biometric data: Encrypted, role-based access
- Contact details: Masked in most contexts
- Financial data: Anonymized except for authorized personnel

### Audit Logging
Every access to sensitive data is logged with:
- User ID
- Timestamp
- Data accessed
- Purpose/reason
- IP address

## Data Retention

- Active cases: Indefinite
- Closed cases: 7 years (per law requirements)
- CDR records: 3 years
- Financial records: 5 years
- Audit logs: 2 years
- Archived evidence files: As per case status

---

This model integrates seamlessly with Catalyst services:
- **Data Store**: Relational data storage
- **Search**: Full-text indexing of case notes, victim/suspect info
- **Cache**: Frequently accessed entity caching
- **Analytics**: Time-series and spatial queries
