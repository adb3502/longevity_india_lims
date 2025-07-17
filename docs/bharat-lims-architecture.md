# BHARAT LIMS Architecture & Development Guide

## Overview
Transform OpenSpecimen into a participant-centric LIMS for the BHARAT Study, focusing on multiomics integration and real-time sample tracking.

## Data Model

### 1. Participant Entity (Core)
```
Participant {
  code: "RAM-1A-001" // [CENTER]-[GROUP][GENDER]-[SERIAL]
  demographics: {
    age: 25,
    gender: "M",
    ageGroup: 1,
    enrollmentDate: "2024-07-01",
    center: "RAM"
  }
  consent: {
    status: "completed",
    date: "2024-07-01",
    formId: "BHARAT_CONSENT_v2"
  }
}
```

### 2. Sample Hierarchy
```
Primary Sample
├── Blood (EDTA) - RAM-1A-001-BE
│   ├── Plasma - RAM-1A-001-P1, P2, P3
│   ├── Buffy Coat - RAM-1A-001-BC1
│   └── Whole Blood Aliquot - RAM-1A-001-WB1
├── Blood (SST) - RAM-1A-001-BS
│   └── Serum - RAM-1A-001-S1, S2, S3...
├── Urine - RAM-1A-001-U1
├── Hair - RAM-1A-001-H1
├── Cheek Swab - RAM-1A-001-CS1
└── Stool - RAM-1A-001-ST1 (if provided)
```

### 3. Sample Naming Convention
- Primary samples: `[PARTICIPANT_CODE]-[SAMPLE_TYPE_CODE]`
- Aliquots: `[PARTICIPANT_CODE]-[ALIQUOT_TYPE][SEQUENTIAL_NUMBER]`

Sample Type Codes:
- BE = Blood EDTA
- BS = Blood SST  
- U = Urine
- H = Hair
- CS = Cheek Swab
- ST = Stool

Aliquot Type Codes:
- P = Plasma
- S = Serum
- BC = Buffy Coat
- WB = Whole Blood

## Database Schema Extensions

### Custom Tables Needed

```sql
-- Participant grouping and coding
CREATE TABLE bharat_participants (
  participant_id BIGINT PRIMARY KEY,
  center_code VARCHAR(10),
  age_group INT,
  gender CHAR(1),
  sequential_number INT,
  full_code VARCHAR(20) UNIQUE, -- e.g., RAM-1A-001
  enrollment_status VARCHAR(20),
  FOREIGN KEY (participant_id) REFERENCES catissue_participant(identifier)
);

-- Integration tracking
CREATE TABLE bharat_data_integrations (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  participant_id BIGINT,
  data_type VARCHAR(50), -- 'epicollect', 'blood_results', 'flow_cytometry'
  external_id VARCHAR(100),
  import_date TIMESTAMP,
  data_json TEXT,
  FOREIGN KEY (participant_id) REFERENCES catissue_participant(identifier)
);

-- Multiomics batch tracking
CREATE TABLE bharat_omics_batches (
  batch_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  batch_name VARCHAR(100),
  omics_type VARCHAR(50), -- 'genomics', 'proteomics', 'metabolomics'
  plate_layout JSON,
  created_date TIMESTAMP,
  status VARCHAR(20)
);
```

## API Endpoints to Implement

### 1. Participant Management
```
POST /api/bharat/participants/enroll
GET /api/bharat/participants/{code}
GET /api/bharat/participants/{code}/samples
GET /api/bharat/participants/{code}/timeline
```

### 2. Sample Collection
```
POST /api/bharat/samples/collect
POST /api/bharat/samples/create-aliquots
GET /api/bharat/samples/{barcode}/track
```

### 3. Data Integration
```
POST /api/bharat/import/epicollect
POST /api/bharat/import/lab-results
POST /api/bharat/import/flow-cytometry
```

### 4. Dashboard APIs
```
GET /api/bharat/dashboard/enrollment-stats
GET /api/bharat/dashboard/sample-distribution
GET /api/bharat/dashboard/pending-analyses
```

## UI Components to Build

### 1. Participant Search & View
- Global search by participant code
- Quick filters by age group, gender, center
- Participant detail page with tabs

### 2. Sample Collection Workflow
```javascript
// Workflow steps:
1. Scan/Enter participant code
2. Verify participant details
3. Record sample collection
   - Check off each sample type collected
   - Scan pre-printed barcode labels
   - Note any deviations
4. Generate aliquot labels
5. Confirm storage location
```

### 3. Real-time Dashboards
- Enrollment progress by age/gender matrix
- Sample inventory heatmap
- Pending analyses queue
- Data completeness tracker

## Integration Points

### 1. ODK Collect Integration
- Webhook endpoint to receive form submissions
- Auto-create participant and initial samples
- Map ODK fields to OpenSpecimen custom fields

### 2. Diagnostic Lab APIs
```javascript
// Pseudocode for lab result import
async function importLabResults(participantCode, labName) {
  const results = await fetchFromLabAPI(participantCode, labName);
  const participant = await getParticipantByCode(participantCode);
  
  // Store raw results
  await saveDataIntegration(participant.id, 'blood_results', results);
  
  // Parse and store structured data
  await updateParticipantLabResults(participant.id, parseLabResults(results));
  
  // Trigger notifications if abnormal
  checkAbnormalValues(results);
}
```

### 3. Freedom EVO Integration
- File watcher for CSV exports
- Parse plate layouts and update sample processing status
- Track plate-to-sample mappings for batch effects

## Development Priorities

### Phase 1 (Immediate - Week 1)
1. Implement participant-centric data model
2. Create barcode generation and printing module
3. Build basic participant search and view
4. Set up sample collection workflow

### Phase 2 (Week 2)
1. Integrate ODK Collect webhook
2. Build enrollment dashboard
3. Implement aliquot tracking
4. Create sample location management

### Phase 3 (Week 3-4)
1. Lab API integrations (1MG, Healthians, Lal Path)
2. Data visualization dashboards
3. Batch management for multiomics
4. QC and audit trails

## Configuration Files

### Custom Forms Configuration
```json
{
  "bharat_participant_form": {
    "fields": [
      {"name": "exclusion_criteria", "type": "multiselect"},
      {"name": "medications", "type": "text"},
      {"name": "family_history", "type": "json"}
    ]
  }
}
```

### Workflow Rules
```json
{
  "sample_collection_rules": {
    "required_samples": ["BE", "BS", "U", "H", "CS"],
    "optional_samples": ["ST"],
    "aliquot_rules": {
      "BE": {"plasma": 3, "buffy": 1, "whole_blood": 1},
      "BS": {"serum": "variable"} // Based on volume
    }
  }
}
```

## Security & Compliance
- Role-based access control per center
- Audit trail for all sample events
- PHI encryption at rest
- API rate limiting for external integrations

## Change History

### 2025-07-16 - Initial Architecture Implementation
- Designed participant-centric data model with coding scheme
- Created sample hierarchy and naming conventions
- Defined database schema extensions for BHARAT-specific tables
- Outlined API endpoints for participant, sample, and data management
- Designed UI components for collection workflow
- Established integration points for external systems
- Set development priorities in 3 phases
- Created configuration templates for forms and workflows