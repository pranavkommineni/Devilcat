# Security & RBAC - KSP Crime Intelligence Platform

## Overview

Security is a critical component of the crime intelligence platform, protecting sensitive investigative data and ensuring proper access controls. The system implements multiple layers of security controls to comply with law enforcement data protection regulations.

## Authentication

### Catalyst OAuth 2.0 Integration

All users authenticate through Catalyst's OAuth 2.0 implementation:

```
User Login → Catalyst Auth Provider → JWT Token → Session Established
```

**Token Structure:**
- Access Token: 1-hour expiry
- Refresh Token: 7-day expiry
- Token scopes: role-based permissions

### Multi-Factor Authentication (MFA)

Optional MFA support:
- TOTP (Time-based One-Time Password)
- SMS-based verification
- Hardware security key support
- Enforced for admin users

### Session Management

- Session timeout: 30 minutes (configurable)
- Device binding: Optional
- Concurrent session limits: 3 per user
- Force logout on password change
- Session revocation on role change

## Authorization & RBAC

### Role Hierarchy

```
┌─────────────────────────────────────────┐
│ System Admin                             │
│ └─ Manage users, roles, system config  │
│    └─ Create new investigators/analysts │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Analyst (SCRB-level)                   │
│ └─ View cross-case patterns            │
│    └─ Generate reports                  │
│    └─ Access dashboards & analytics    │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Investigator (Case Officer)             │
│ └─ Create/modify assigned cases        │
│    └─ Upload evidence                   │
│    └─ Add suspects/victims             │
│    └─ Access AI investigation tools    │
└─────────────────────────────────────────┘
```

### Role-Based Permissions Matrix

#### Investigator Role

```
FIR Operations:
  ✓ Create FIR (assigned station only)
  ✓ Edit own FIRs
  ✗ Edit others' FIRs
  ✓ View assigned FIRs
  ✗ View other investigations (except linked)
  ✓ Upload evidence to assigned cases
  ✗ Delete FIRs

Suspect/Victim Operations:
  ✓ Create suspect profile
  ✓ Link to case
  ✓ View linked profiles
  ✗ Edit suspect profile (except basic info)
  ✗ Delete records

AI Assistant:
  ✓ Chat with ConvoKraft
  ✓ Get MO recommendations
  ✓ View risk scores
  ✓ Request link analysis

Reports:
  ✓ View case report
  ✗ Generate cross-case reports
  ✓ Export own case data (to file)

Admin:
  ✗ User management
  ✗ System settings
  ✗ Audit logs
```

#### Analyst Role

```
FIR Operations:
  ✓ View all FIRs (filtered by district/type)
  ✗ Edit FIRs
  ✓ Export FIR data (anonymized where needed)

Analytics:
  ✓ Access dashboards
  ✓ View hotspot maps
  ✓ Trend analysis
  ✓ Network link analysis
  ✓ Generate SCRB reports

Reporting:
  ✓ Create ad-hoc reports
  ✓ Schedule periodic reports
  ✓ Export data
  ✓ Share reports with team

Suspect/Victim:
  ✓ View profiles
  ✓ View relationship networks
  ✗ Modify profiles

Admin:
  ✗ User management
  ✗ System settings
  ✗ Audit logs
```

#### Admin Role

```
User Management:
  ✓ Create users
  ✓ Delete users
  ✓ Assign roles
  ✓ Reset passwords
  ✓ Disable accounts
  ✓ View user activity

System Configuration:
  ✓ Modify feature flags
  ✓ Update system parameters
  ✓ Configure data retention
  ✓ Manage integrations
  ✓ Control API rate limits

Security:
  ✓ View audit logs
  ✓ Export audit logs
  ✓ Configure security policies
  ✓ Manage encryption keys
  ✓ Review access violations

All Operations:
  ✓ Full access to all data
  ✓ Override restrictions (with logging)
```

### Dynamic Role-Based Access

**Case-Level Permissions:**

```python
# Example: Investigator viewing FIR
if user.role == "Investigator":
    # Can view if:
    # 1. They created it, OR
    # 2. They're assigned to the case, OR
    # 3. They're linked as a suspect/victim (investigation access)
    accessible_firs = (
        FIRs.created_by(user) OR
        FIRs.assigned_to(user) OR
        FIRs.linked_to_user_investigation(user)
    )
```

**Geographic Permissions:**

```python
# Example: Restrict access by police station
if user.role == "Investigator":
    # Can only see FIRs from their assigned station
    accessible_firs = FIRs.filter(
        police_station = user.assigned_station
    )
```

**Data Classification Access:**

```python
# Sensitive data access tiers
LOW_SENSITIVITY:      # All authenticated users
  - Case status
  - Public offense information
  - Generic location data

MEDIUM_SENSITIVITY:   # Investigator+
  - Suspect names
  - Victim contact info
  - Evidence files

HIGH_SENSITIVITY:     # Admin + Designated Analysts
  - Financial records
  - Biometric data
  - Detailed victim info
  - Investigative notes
```

## Data Protection

### Encryption in Transit

- **Protocol**: TLS 1.3
- **Cipher Suites**: AES-256-GCM
- **Certificate Pinning**: Enabled for API clients
- **Enforcement**: All data transfers encrypted

### Encryption at Rest

- **Data Store**: AES-256 encryption
- **Stratus (File Storage)**: AES-256 object encryption
- **Database**: Transparent Data Encryption (TDE)
- **Cache (Redis)**: Optional encryption (configured)

**Encryption Key Management:**
- Catalyst managed keys (default)
- Customer managed keys (BYOK) option
- Key rotation: 90-day policy
- Hardware Security Module (HSM): Supported

### Data Masking & PII Protection

**Automatic Masking:**

```
Suspect Name:      "Rajesh Kumar" → "R**** K****"
Phone Number:      "9876543210" → "98XXXXXX10"
Email:            "raj@email.com" → "r**@email.com"
Financial Amount:  "₹5,00,000" → "₹*,**,***"
```

**Masking Policies by Role:**

| Data Type | Investigator | Analyst | Admin |
|-----------|--------------|---------|-------|
| Suspect Name | Full | Masked | Full |
| Victim Name | Full | Masked | Full |
| Contact Info | Full | Masked | Full |
| Financial Amounts | Actual | Masked | Full |
| Biometric Data | Hash | Denied | Full |

### Database Security

- **SQL Injection**: Parameterized queries, ORM usage
- **Access Control**: Database-level RBAC
- **Monitoring**: Query logging for sensitive operations
- **Backup**: Encrypted daily backups, 7-day retention

## Audit Logging

### Comprehensive Audit Trail

Every operation logs:

```
{
  timestamp: DateTime,
  user_id: UUID,
  user_role: String,
  action: String,
  resource_type: String,
  resource_id: UUID,
  changes: {
    before: JSON,
    after: JSON
  },
  ip_address: String,
  user_agent: String,
  status: Enum (Success, Failed, Denied),
  denial_reason: String (if denied),
  session_id: UUID
}
```

### Sensitive Operations Logged

- FIR creation/modification/deletion
- Suspect profile access/modification
- Victim data access
- Evidence file download
- Report generation
- User role changes
- System configuration changes
- Login/logout
- Failed authentication attempts
- Permission denials

### Audit Log Retention

- Production: 2 years minimum
- Searchable retention: 1 year
- Compliance retention: As required by jurisdiction

### Audit Log Access

- Only Admin role can access audit logs
- Audit log access itself is logged
- Export functionality with digital signatures
- Real-time alerting for suspicious patterns

## Threat Protection

### DDoS Protection

- Catalyst-managed DDoS mitigation
- Rate limiting: 1000 requests/minute per user
- IP-based throttling for suspicious patterns
- Automatic blacklisting of abusive clients

### Malware Scanning

**File Upload Protection:**

```
1. Upload file to Stratus
   ↓
2. Immediate scan (ClamAV + Yara signatures)
   ↓
3. If Clean → Indexed and available
   If Threat → Quarantined, alert admin
   ↓
4. Periodic re-scanning for new signatures
```

### API Security

- **Authentication**: JWT bearer tokens
- **Rate Limiting**: Per-user, per-endpoint
- **Input Validation**: Strict schema validation
- **Output Encoding**: Prevent XSS attacks
- **CORS**: Strict origin validation

### Vulnerability Management

- Regular security audits
- Automated dependency scanning
- Penetration testing: Quarterly
- Bug bounty program
- Security patches: Applied within 24 hours

## Compliance & Legal

### Data Protection Regulations

- **GDPR**: Right to be forgotten implementation
- **India DPDP Act**: Data Protection Policy compliance
- **Law Enforcement Data Regulations**: Jurisdiction-specific policies
- **Confidentiality**: Investigation data confidentiality

### Investigative Privilege

Certain data protected by investigative privilege:
- Source protection
- Ongoing investigation restrictions
- Attorney-client communications
- Privileged work product

### Consent & Transparency

- User data consent forms
- Privacy policy acknowledgment
- Purpose limitation (data only used for criminal justice)
- Access transparency reports

## Incident Response

### Security Incident Procedure

```
1. Detection → Alert admin
2. Isolation → Limit impact
3. Analysis → Determine scope
4. Notification → Inform affected users
5. Remediation → Fix vulnerability
6. Post-mortem → Learn and improve
```

### Breach Notification

- Immediate notification to admin
- User notification within 24 hours (if PII exposed)
- Regulatory notification within timeline
- Forensic investigation report

## Testing & Validation

### Security Testing

- **SAST**: Static code analysis
- **DAST**: Dynamic security scanning
- **Penetration Testing**: Quarterly
- **Dependency Audits**: Weekly
- **Compliance Audits**: Annually

### Authentication Testing

- Multi-factor authentication verification
- Session management validation
- Token expiry enforcement
- Permission boundary testing

---

**Last Updated**: 2024
**Version**: 1.0
**Review Schedule**: Quarterly
