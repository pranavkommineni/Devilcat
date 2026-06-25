# KSP Crime Intelligence Platform - Architecture

## System Overview

The KSP Crime Intelligence Platform is a modular, cloud-native system designed to support law enforcement agencies in managing criminal intelligence data and performing advanced analytics for crime prevention.

### Architecture Layers

#### 1. **Presentation Layer** (Frontend)
Three specialized React applications serve different user roles:

- **Investigator Portal**: Field officers and case investigators
  - FIR (First Information Report) creation and management
  - Suspect/Victim profile lookup
  - Evidence file upload and review
  - AI-assisted investigation recommendations
  
- **Analyst Portal**: Intelligence analysts and supervisors (SCRB-level)
  - Crime analytics dashboards
  - Geographic hotspot mapping
  - Trend and pattern discovery
  - Network link analysis
  - Report generation
  
- **Admin Portal**: System administrators
  - User and role management
  - Permission configuration
  - System settings and feature flags
  - Audit log review
  - Data import/export management

#### 2. **API Gateway Layer**
FastAPI backend serves as the central API gateway providing:
- RESTful endpoints for all operations
- OpenAPI/Swagger documentation
- Request validation and error handling
- Rate limiting and throttling
- Authentication and authorization

#### 3. **Service Layer**
Business logic organized by domain:

**Core Services:**
- **FIR Management**: Record creation, updates, closure
- **Suspect Profiling**: Database creation, MO management, relationship tracking
- **Victim Management**: Data collection and privacy protection
- **Crime Classification**: Offence coding and categorization

**Intelligence Services:**
- **Network Analysis**: Link analysis, suspect-victim-location relationships
- **Predictive Analytics**: Risk scoring, crime forecasting, hotspot prediction
- **Conversational AI**: Natural language investigation assistant (ConvoKraft)
- **Pattern Mining**: MO clustering, association rules, emerging trends

**Support Services:**
- **Evidence Management**: File upload, storage, retrieval (Stratus)
- **Report Generation**: Periodic intelligence reports, ad-hoc exports
- **Audit Logging**: Operation tracking for compliance
- **Notifications**: Real-time alerts and updates (Signals)

#### 4. **Data Access Layer**
Repository pattern implementation providing abstraction over:
- **Catalyst Data Store**: Structured records (FIRs, Suspects, Victims)
- **Catalyst Cache**: High-performance data caching
- **Catalyst Stratus**: Distributed file storage
- **External APIs**: CDR, Finance, GIS data sources

#### 5. **Data Layer**

**Primary Storage:**
- PostgreSQL for relational data persistence
- Neo4j-style graph structures for network relationships
- Redis for session/cache storage

**Catalyst Services Integration:**
- Data Store: Managed structured data
- Cache: Distributed in-memory caching
- Stratus: Scalable file storage
- Search: Full-text search capabilities

#### 6. **Processing Layer**

**AI/ML Pipeline:**
- ConvoKraft: Conversational AI for investigation support
- Zia: Document intelligence and OCR processing
- QuickML: Managed ML model serving
- Custom Models: Risk scoring, anomaly detection, MO clustering

**Analytics Engines:**

*Spatiotemporal Analysis:*
- Crime density mapping
- Hotspot detection and forecasting
- Geographic drill-down capabilities
- Time-series trend analysis

*Network Analysis:*
- Graph centrality measures
- Repeat offender identification
- Association discovery
- Link strength visualization

*Predictive Analytics:*
- Recidivism risk scoring
- Crime likelihood prediction
- Offender profiling
- Trend forecasting

#### 7. **Infrastructure Layer**

**Event-Driven Architecture:**
- Catalyst Signals: Pub/Sub messaging for real-time events
- Catalyst Circuits: Workflow orchestration
- Catalyst Functions: Serverless compute for background jobs

**Key Workflows:**
- FIR Ingestion Trigger: Processes new FIRs, triggers enrichment
- OCR Document Processing: Extracts text from evidence files
- Anomaly Alert Dispatcher: Detects and broadcasts suspicious patterns
- Scheduled Intelligence Reports: Generates periodic reports
- Circuits Automation: Orchestrates complex multi-step workflows

**Deployment:**
- AppSail: Backend deployment platform
- Catalyst CLI: Frontend and functions deployment
- Infrastructure-as-Code: YAML configurations for reproducibility

## Data Flow

### Typical Investigation Workflow

```
1. Officer Creates FIR
   ↓
2. FIR Ingestion Function Triggered
   - Validates FIR data
   - Extracts suspect/victim info
   - Triggers MO analysis
   ↓
3. AI Enrichment
   - Finds similar MOs
   - Identifies linked suspects
   - Generates risk scores
   ↓
4. Analyst Reviews in Dashboard
   - Views hotspots
   - Analyzes network
   - Generates insights
   ↓
5. Real-time Alerts
   - Signals event published
   - Dispatch notifications
   - Updates dashboards
```

### File Evidence Processing

```
1. Officer Uploads Evidence File → Stratus
   ↓
2. OCR Trigger Function Activated
   ↓
3. Zia AI Processes Document
   ↓
4. Extracted Text Indexed in Search
   ↓
5. Results Available in Investigation Portal
```

## Security Architecture

### Authentication & Authorization

- **Catalyst OAuth 2.0**: Central authentication
- **JWT Tokens**: Session management
- **RBAC Model**:
  - Investigator: Case-level access
  - Analyst: Cross-case pattern access
  - Admin: System-wide configuration

### Data Protection

- **Encryption in Transit**: TLS 1.3
- **Encryption at Rest**: Data Store encryption
- **Access Control**: Catalyst IAM policies
- **Audit Logging**: All operations tracked
- **PII Protection**: Suspect/Victim data masking where applicable

## Scalability Considerations

### Horizontal Scaling

- **Backend**: AppSail auto-scaling based on CPU/memory
- **Functions**: Serverless auto-provisioning
- **Frontend**: CDN distribution for static assets
- **Database**: Read replicas for analytics queries

### Performance Optimization

- **Caching Strategy**: Multi-level caching with Catalyst Cache
- **Database Indexing**: Optimized queries for common patterns
- **Lazy Loading**: Progressive data loading in portals
- **Batch Processing**: Bulk operations for efficiency

## Integration Points

### External Data Sources

- **CDR (Call Detail Records)**: Telecom integration
- **Finance**: Transaction monitoring
- **GIS**: Geographic information systems
- **Third-party APIs**: Additional intelligence sources

### Monitoring & Observability

- Application metrics via AppSail
- Function execution logs
- API performance tracking
- Error rate monitoring
- Custom dashboards for operational metrics

## Deployment Architecture

### Development Environment

```
local/
├── Backend: uvicorn (http://localhost:8000)
├── Investigator Portal: Vite (http://localhost:5173)
├── Analyst Portal: Vite (http://localhost:5174)
├── Admin Portal: Vite (http://localhost:5175)
├── PostgreSQL: Docker container
├── Redis: Docker container
└── Catalyst CLI: Local simulator
```

### Production Environment

```
cloud/
├── Backend: AppSail (auto-scaled)
├── Frontend: Catalyst Hosting + CDN
├── Functions: Catalyst Functions (serverless)
├── Data: Catalyst managed services
├── Monitoring: Catalyst Observability
└── CI/CD: GitHub Actions / GitLab CI
```

## Deployment Pipeline

```
Code Push → Build → Test → Deploy
            ↓       ↓
         Docker  Unit Tests
         Build   Int Tests
                 E2E Tests
                    ↓
         Backend → AppSail
         Frontend → Catalyst Hosting
         Functions → Catalyst Functions
```

---

For detailed API specifications, see [api-spec.md](api-spec.md)
For data model details, see [data-model.md](data-model.md)
For security details, see [security-rbac.md](security-rbac.md)
