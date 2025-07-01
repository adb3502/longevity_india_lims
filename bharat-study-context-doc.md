# OpenSpecimen Customization for Longevity India BHARAT Study
## Complete Context Document for Development

---

## Executive Summary

This document provides comprehensive context for customizing OpenSpecimen Community Edition for the Longevity India BHARAT Study (Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions). The customization aims to create a state-of-the-art Laboratory Information Management System (LIMS) specifically tailored for longevity research in the Indian population.

**Document Version**: 1.0  
**Date**: January 2025  
**Project Lead**: Longevity India, IISc Bangalore  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Requirements](#2-system-requirements)
3. [Functional Requirements](#3-functional-requirements)
4. [Technical Specifications](#4-technical-specifications)
5. [Implementation Roadmap](#5-implementation-roadmap)
6. [Usage Guidelines](#6-usage-guidelines)

---

## 1. Project Overview

### 1.1 Current Situation
- **Platform**: OpenSpecimen Community Edition (latest version)
- **Status**: Successfully deployed on Linux workstation
- **User**: Biologist (non-developer) requiring technical assistance
- **Objective**: Transform generic OpenSpecimen into specialized BHARAT Study LIMS

### 1.2 About BHARAT Study

The **BHARAT Study** (Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions) represents a groundbreaking initiative in aging research:

- **Mission**: Investigate aging biomarkers specific to the Indian population through multi-omics analyses
- **Scope**: Comprehensive longitudinal study tracking participants over 2+ years
- **Innovation**: First large-scale study focusing on India-specific aging patterns
- **Impact**: Develop interventions to improve healthspan in Indian population

#### Key Study Parameters

| Parameter | Details |
|-----------|---------|
| **Age Range** | 20-70 years |
| **Cohorts** | 5 age groups (20-30, 31-40, 41-50, 51-60, 61-70) |
| **Sample Types** | Blood, Saliva, Hair follicles, Buccal cells |
| **Study Design** | Longitudinal (Baseline, 6mo, 12mo, 24mo) |
| **Analysis Types** | Genomics, Proteomics, Metabolomics, Epigenomics |
| **Geographic Coverage** | Multi-site across India |

#### Institutional Partners

- **Lead Institution**: Indian Institute of Science (IISc), Bangalore
- **Clinical Partners**: 
  - MS Ramaiah Hospital
  - Bangalore Medical College & Research Institute
- **Technology Partner**: Arca AI (AI/ML analytics platform)
- **Industry Support**: 
  - Beckman Coulter
  - Healthians
  - Valerian Proteomics
  - DecodeAge

### 1.3 About OpenSpecimen

OpenSpecimen is an open-source biobanking informatics platform with the following characteristics:

- **Architecture**: Web-based, multi-tier application
- **APIs**: 100% REST API enabled
- **Customization**: Highly configurable without coding
- **Extensibility**: Plugin architecture for advanced features
- **Technology Stack**: Java backend, Angular frontend, MySQL/Oracle database
- **Key Principle**: "Biospecimens without high quality data are of no value"

---

## 2. System Requirements

### 2.1 Technical Environment

```yaml
Operating System: Linux (Ubuntu/CentOS)
Database: MySQL 5.7+ (already configured)
Application Server: Tomcat 9+
Java Version: JDK 11+
Storage: Minimum 500GB for data and documents
RAM: 16GB minimum (32GB recommended)
Network: Stable internet for integrations
```

### 2.2 Integration Requirements

**Laboratory Instruments**:
- FreedomEvo Liquid Handlers (Tecan)
- Multiple Mass Spectrometers (Thermo, Waters, Agilent)
- Flow Cytometers (BD, Beckman Coulter)
- Plate readers and other analytical instruments

**Software Systems**:
- ODK Collect (field data collection)
- REDCap (clinical data)
- Laboratory instruments software
- Arca AI analytics platform

**Data Formats**:
- CSV, Excel (XLSX)
- JSON for API communications
- HL7 for clinical data (future)
- Vendor-specific instrument formats

---

## 3. Functional Requirements

### 3.1 Custom Branding and User Interface

#### Visual Identity Requirements

**Color Palette**:
- **Primary**: `#FF6B35` (Warm Orange) - Represents vitality and longevity
- **Secondary**: `#004643` (Deep Teal) - Conveys trust and stability
- **Accent**: `#F8DDA4` (Light Gold) - Premium quality indicator
- **Neutral**: `#F5F5F5` (Light Gray) - Background
- **Text**: `#2C3E50` (Dark Blue-Gray) - High contrast

**Typography**:
- **Headers**: Montserrat (Bold/Semi-bold)
- **Body Text**: Open Sans (Regular/Medium)
- **Data Tables**: Roboto Mono (Monospace)

**UI Elements**:
- Border radius: 8px (consistent rounded corners)
- Card shadows: `0 2px 4px rgba(0,0,0,0.1)`
- Transitions: 0.3s ease-in-out
- Hover effects on all interactive elements

**Branding Applications**:
1. Login page with study description
2. Custom header with Longevity India logo
3. Branded email templates
4. Report headers and footers
5. Loading screens and animations

### 3.2 Dashboard Requirements

#### 3.2.1 Sample Collection Metrics
Real-time visualization of collection progress:

```
Widget Layout:
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ Total Samples       │ Today's Progress    │ Pending Processing  │
│ by Age Cohort       │ [Progress Bar]      │ [Counter]           │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ Site Performance    │ Weekly Trends       │ Quality Alerts      │
│ [Map View]          │ [Line Chart]        │ [Alert List]        │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

**Metrics to Display**:
- Total samples by age cohort (pie chart)
- Daily collection targets vs actual (gauge chart)
- Site-wise performance (heat map)
- Processing queue status (real-time counter)
- Visit completion rates (funnel chart)

#### 3.2.2 Multi-omics Analysis Tracking

**Visual Requirements**:
- Sankey diagram showing sample flow through analyses
- Progress bars for each omics type
- Queue status with estimated completion times
- Failed analysis tracking with reasons

#### 3.2.3 Biomarker Analytics Dashboard

**Visualization Components**:
1. **Heatmap**: Biomarker levels across age groups
2. **Correlation Matrix**: Relationships between aging markers
3. **Alert System**: Out-of-range values requiring attention
4. **Trend Analysis**: Longitudinal changes per participant
5. **Population Distribution**: Bell curves for each marker

#### 3.2.4 Inventory Management Dashboard

**Real-time Monitoring**:
```
┌─────────────────────────────────────┐
│ Freezer Capacity Visualization      │
│ [3D Freezer Layout with Color Coding]│
├─────────────────────────────────────┤
│ Kit Inventory    │ Reagent Status   │
│ • Blood: 245/300 │ • DNA Kits: 45d  │
│ • Saliva: 189/250│ • Proteins: 23d  │
│ • Hair: 156/200  │ • Metabol: 67d   │
└─────────────────────────────────────┘
```

### 3.3 Sample Tracking System

#### 3.3.1 Hierarchical Numbering Scheme

**1. Box Identification**
```
Format: BHARAT-[SITE]-[FREEZER]-[RACK]-[BOX]
Example: BHARAT-BLR-F01-R03-B045

Site Codes:
- BLR: Bangalore
- MUM: Mumbai  
- DEL: Delhi
- CHE: Chennai
- KOL: Kolkata
```

**2. Sample Identification**
```
Format: BHARAT-[COHORT]-[PARTICIPANT]-[VISIT]-[TYPE]
Example: BHARAT-AG3-P0234-V2-BLD

Cohort Codes:
- AG1: 20-30 years
- AG2: 31-40 years
- AG3: 41-50 years
- AG4: 51-60 years
- AG5: 61-70 years

Sample Type Codes:
- BLD: Blood
- SAL: Saliva
- HAR: Hair
- CEL: Cells
```

**3. Aliquot Identification**
```
Format: [PARENT_LABEL]-[ANALYSIS]-[SEQUENCE]
Example: BHARAT-AG3-P0234-V2-BLD-PROT-01

Analysis Codes:
- GEN: Genomics
- PROT: Proteomics
- META: Metabolomics
- EPI: Epigenomics
- CLIN: Clinical chemistry
```

#### 3.3.2 Storage Box Configurations

| Box Type | Configuration | Capacity | Sample Type |
|----------|--------------|----------|-------------|
| Standard Blood | 9×9 grid | 81 | Blood derivatives |
| Saliva Box | 10×10 grid | 100 | Saliva aliquots |
| Hair Storage | 12×8 grid | 96 | Hair samples |
| Cell Storage | 8×12 grid | 96 | Cell pellets |
| DNA Plate | 8×12 grid | 96 | DNA aliquots |

### 3.4 Collection Protocols

#### 3.4.1 BHARAT Longitudinal Study Protocol

```
Protocol Structure:
├── Enrollment Phase
│   ├── Eligibility Verification
│   │   ├── Age check (20-70 years)
│   │   ├── Consent capacity assessment
│   │   └── Exclusion criteria check
│   ├── Informed Consent
│   │   ├── Main study consent
│   │   ├── Genetic analysis consent
│   │   ├── Data sharing consent
│   │   └── Future research consent
│   └── Baseline Assessment
│       ├── Demographics
│       ├── Medical history
│       ├── Lifestyle questionnaire
│       └── Physical measurements
├── Visit Schedule
│   ├── V0 (Baseline)
│   │   ├── All sample types
│   │   ├── Comprehensive assessment
│   │   └── 3-hour appointment
│   ├── V1 (6 months ± 2 weeks)
│   │   ├── Blood and saliva only
│   │   ├── Brief assessment
│   │   └── 1-hour appointment
│   ├── V2 (12 months ± 2 weeks)
│   │   ├── All sample types
│   │   ├── Annual assessment
│   │   └── 2-hour appointment
│   └── V3 (24 months ± 2 weeks)
│       ├── All sample types
│       ├── Final assessment
│       └── 3-hour appointment
└── Sample Collection Requirements
    ├── Blood: 4×5ml EDTA tubes
    ├── Saliva: 1×5ml collection tube
    ├── Hair: 50 strands (with follicles)
    └── Cells: 2 buccal swabs
```

#### 3.4.2 Sample Processing Workflows

**Blood Processing SOP** (Critical: Process within 2 hours)
```
1. Receipt and Registration
   - Scan sample barcode
   - Verify participant ID
   - Record collection time
   - Check tube integrity

2. Centrifugation
   - 1500g for 10 minutes at 4°C
   - No brake setting
   
3. Aliquoting
   - Plasma: 10 aliquots × 0.5ml
   - Buffy coat: 5 aliquots × 0.2ml
   - Red cells: 5 aliquots × 0.5ml
   
4. Storage
   - Immediate transfer to -80°C
   - Record freezer location
   - Update inventory system
```

**Saliva Processing SOP**
```
1. Stabilization
   - Room temperature for 30 minutes
   - Gentle mixing
   
2. Aliquoting
   - 10 aliquots × 0.5ml
   - Leave dead volume
   
3. Storage
   - Flash freeze in liquid nitrogen
   - Transfer to -80°C
```

### 3.5 Experimental Data Tracking

#### 3.5.1 DNA Extraction Form

| Field | Type | Validation | Required |
|-------|------|------------|----------|
| Sample ID | Text | Regex pattern match | Yes |
| Extraction Date | DateTime | Not future date | Yes |
| Method | Dropdown | Qiagen/Promega/Other | Yes |
| Kit Lot Number | Text | Alphanumeric | Yes |
| Technician ID | Dropdown | Active users only | Yes |
| Yield (ng/μl) | Number | 0-5000 | Yes |
| Volume (μl) | Number | 0-200 | Yes |
| 260/280 Ratio | Number | 1.6-2.1 | Yes |
| 260/230 Ratio | Number | 1.8-2.4 | Yes |
| QC Status | Radio | Pass/Fail/Repeat | Yes |
| Notes | TextArea | Max 500 chars | No |

#### 3.5.2 Multi-omics Analysis Forms

**Genomics Analysis Form**:
- Sequencing platform (Illumina/PacBio/ONT)
- Library preparation method
- Sequencing depth (coverage)
- Read length
- Quality metrics (Q30%)
- Total reads generated
- File paths (FASTQ/BAM)
- Analysis pipeline version

**Proteomics Analysis Form**:
- MS platform (vendor/model)
- Sample preparation method
- Protein concentration (μg/μl)
- Number of proteins identified
- Unique peptides count
- Search database used
- FDR threshold
- Raw file location

**Metabolomics Analysis Form**:
- Analysis type (targeted/untargeted)
- LC-MS method details
- Number of metabolites detected
- Internal standards used
- Batch information
- QC sample performance
- Peak quality metrics

#### 3.5.3 Biomarker Panel Tracking

**Standard Panels**:

1. **Inflammation Panel**
   - C-Reactive Protein (CRP): 0-10 mg/L
   - Interleukin-6 (IL-6): 0-10 pg/ml
   - Tumor Necrosis Factor-α (TNF-α): 0-20 pg/ml
   - Interleukin-1β (IL-1β): 0-5 pg/ml

2. **Metabolic Health Panel**
   - Fasting Glucose: 70-100 mg/dl
   - HbA1c: 4-6%
   - Insulin: 2-25 μIU/ml
   - Lipid Profile (TC, LDL, HDL, TG)

3. **Aging Biomarkers**
   - Telomere Length: qPCR T/S ratio
   - p16INK4a expression
   - GDF15: 200-1800 pg/ml
   - Epigenetic age (Horvath clock)

4. **Organ Function Markers**
   - Kidney: Cystatin C, eGFR
   - Liver: ALT, AST, Albumin
   - Heart: NT-proBNP, Troponin
   - Thyroid: TSH, Free T4

### 3.6 Inventory Management System

#### 3.6.1 Kit and Consumable Tracking

**Collection Kit Components**:
```
Blood Collection Kit:
├── 4 × 5ml EDTA tubes
├── 1 × 21G butterfly needle
├── 1 × Tourniquet
├── 2 × Alcohol swabs
├── 1 × Bandage
└── 1 × Biohazard bag

Minimum Stock Levels (per site):
- Active sites: 50 kits
- New sites: 100 kits
- Reorder at 30% remaining
```

#### 3.6.2 Reagent Management

**Critical Reagents Tracking**:
- DNA extraction kits (25 reactions/kit)
- Protein assay reagents
- ELISA kits for biomarkers
- Cell culture media
- Cryopreservation solutions

**Expiry Management**:
- 90-day warning (yellow)
- 30-day warning (orange)
- 7-day critical (red)
- Expired (black) - quarantine

#### 3.6.3 Equipment Monitoring

| Equipment | Monitoring Parameters | Alert Thresholds |
|-----------|---------------------|------------------|
| -80°C Freezers | Temperature, Power | >-75°C for 30min |
| LN2 Tanks | Level, Temperature | <30% capacity |
| Centrifuges | Run hours, Balance | 1000hr service |
| Biosafety Cabinets | Flow rate, HEPA | Annual certification |

### 3.7 Data Completeness Matrix

#### Visual Tracking System

```
Participant Data Completeness Matrix:
┌─────────────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│ Participant │Dem │Med │Life│Samp│DNA │Gen │Prot│Meta│Clin│
├─────────────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
│ P0001       │ ✓  │ ✓  │ ✓  │ ✓  │ ✓  │ ⏱  │ ✓  │ ⏱  │ ✓  │
│ P0002       │ ✓  │ ✓  │ ⏱  │ ✓  │ ✓  │ ✗  │ ⏱  │ -  │ ✓  │
│ P0003       │ ✓  │ ✓  │ ✓  │ ⏱  │ -  │ -  │ -  │ -  │ -  │
└─────────────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘

Legend: ✓ Complete | ⏱ In Progress | ✗ Failed | - Not Started
```

### 3.8 Excel Integration Specifications

#### 3.8.1 Import Templates

**Participant Registration Template**:
```
Columns:
A: Study ID (auto-generated if blank)
B: First Name*
C: Last Name*
D: Date of Birth* (DD/MM/YYYY)
E: Gender* (M/F/O)
F: Mobile Number*
G: Email
H: Address Line 1*
I: City*
J: State*
K: PIN Code*
L: Consent Date* (DD/MM/YYYY)
M: Consent Version*
N: Site Code*
O: Enrollment Date*

Validation Rules:
- Age must be 20-70 years
- Mobile: 10 digits
- PIN: 6 digits
- Dates: Not future
- Required fields marked with *
```

#### 3.8.2 Bulk Operations

**Supported Bulk Operations**:
1. Participant registration (up to 500 records)
2. Visit scheduling
3. Sample collection records
4. Biomarker results import
5. Inventory updates
6. Sample disposal records

**Error Handling**:
- Pre-validation before import
- Row-by-row error reporting
- Partial import capability
- Rollback on critical errors
- Detailed error log generation

### 3.9 Instrument Integration Specifications

#### 3.9.1 FreedomEvo Liquid Handler

**Integration Requirements**:
```
Worklist Format:
- CSV format with specific headers
- Well position mapping (A1-H12)
- Source and destination volumes
- Dilution factors
- Sample ID mapping

Data Flow:
1. Export worklist from OpenSpecimen
2. Run on FreedomEvo
3. Import completion file
4. Update sample volumes
5. Create aliquot records
```

#### 3.9.2 Mass Spectrometer Integration

**Supported Platforms**:
- Thermo Scientific (RAW files)
- Waters (WIFF files)
- Agilent (D files)
- Bruker (BAF files)

**Data Capture**:
- Sample queue management
- Acquisition parameters
- Quality metrics
- Peak lists
- Quantitation results

#### 3.9.3 Flow Cytometer Integration

**Panel Definition**:
```yaml
T-Cell Panel:
  - CD3-FITC
  - CD4-PE
  - CD8-APC
  - CD45-PerCP
  
B-Cell Panel:
  - CD19-FITC
  - CD20-PE
  - CD27-APC
  
Compensation: Auto-compensation with controls
File Format: FCS 3.1
Analysis: FlowJo compatible
```

### 3.10 ODK Collect Integration

#### Field Data Collection Scenarios

**Use Cases**:
1. Rural health camps
2. Home visits for elderly participants
3. Community screening events
4. Follow-up visits

**Data Synchronization**:
```
ODK Form Fields → OpenSpecimen Mapping:
- participant_id → Participant.studyId
- collection_date → Visit.visitDate
- gps_location → CustomFields.gpsCoordinates
- sample_photo → Attachments.samplePhoto
- field_notes → Visit.comments
```

### 3.11 Advanced Features

#### 3.11.1 Participant Portal

**Features**:
- Secure login with OTP authentication
- Personalized dashboard with health metrics
- Result interpretation in lay language
- Appointment scheduling
- Document downloads (reports, consent forms)
- Feedback and query submission

#### 3.11.2 AI/ML Analytics Integration

**Predictive Models**:
1. Biological age calculation
2. Disease risk assessment
3. Optimal intervention recommendations
4. Anomaly detection in biomarker patterns

**Integration with Arca AI**:
- Real-time data streaming
- Model training pipelines
- Result visualization
- Clinical decision support

#### 3.11.3 Compliance and Security

**Regulatory Compliance**:
- ICMR Ethical Guidelines
- ICMR National Guidelines for Biomedical Research
- IT Act 2000 compliance
- Future DPDP Act readiness

**Security Measures**:
- Multi-factor authentication
- Role-based access control (RBAC)
- Audit trails for all actions
- Data encryption at rest and in transit
- Regular security assessments

---

## 4. Technical Specifications

### 4.1 System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  Load Balancer  │────▶│   Web Server    │
│  (Angular App)  │     │    (Apache)     │     │   (Tomcat)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Mobile Devices  │────▶│   REST APIs     │────▶│ Business Logic  │
│  (Field App)    │     │  (OpenAPI 3.0)  │     │    (Java)       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Instruments    │────▶│ Integration     │────▶│   Database      │
│  (Direct API)   │     │   Services      │     │   (MySQL)       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 4.2 API Specifications

**Authentication**:
```http
POST /rest/ng/sessions
Content-Type: application/json

{
  "loginName": "user@longevityindia.org",
  "password": "encrypted_password",
  "domainName": "openspecimen"
}
```

**Key API Endpoints**:
- `/rest/ng/collection-protocols` - Protocol management
- `/rest/ng/participants` - Participant operations
- `/rest/ng/specimens` - Sample tracking
- `/rest/ng/forms` - Custom form data
- `/rest/ng/query` - Advanced queries

### 4.3 Database Schema Extensions

**Custom Tables Required**:
```sql
-- Biomarker Results Table
CREATE TABLE os_biomarker_results (
    identifier BIGINT PRIMARY KEY,
    specimen_id BIGINT NOT NULL,
    panel_name VARCHAR(50),
    marker_name VARCHAR(100),
    value DECIMAL(10,4),
    unit VARCHAR(20),
    reference_range VARCHAR(50),
    abnormal_flag CHAR(1),
    test_date TIMESTAMP,
    FOREIGN KEY (specimen_id) REFERENCES catissue_specimen(identifier)
);

-- Multi-omics Tracking
CREATE TABLE os_omics_analysis (
    identifier BIGINT PRIMARY KEY,
    specimen_id BIGINT NOT NULL,
    analysis_type VARCHAR(20),
    platform VARCHAR(100),
    status VARCHAR(20),
    start_date TIMESTAMP,
    completion_date TIMESTAMP,
    data_location VARCHAR(500),
    quality_score DECIMAL(5,2),
    FOREIGN KEY (specimen_id) REFERENCES catissue_specimen(identifier)
);
```

### 4.4 Performance Requirements

| Metric | Requirement |
|--------|-------------|
| Page Load Time | < 2 seconds |
| API Response Time | < 500ms (95th percentile) |
| Concurrent Users | Support 100+ |
| Data Import | 1000 records/minute |
| Report Generation | < 30 seconds |
| Uptime | 99.9% availability |

---

## 5. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Custom branding implementation
- [ ] Basic collection protocol setup
- [ ] Essential custom forms
- [ ] User roles and permissions
- [ ] Basic dashboard configuration

### Phase 2: Core Features (Weeks 3-4)
- [ ] Complete sample tracking system
- [ ] Inventory management setup
- [ ] Excel import/export templates
- [ ] Basic reporting configuration
- [ ] Email notifications

### Phase 3: Integrations (Weeks 5-6)
- [ ] Instrument integration development
- [ ] ODK Collect synchronization
- [ ] API integration testing
- [ ] Advanced dashboard widgets
- [ ] Automated workflows

### Phase 4: Advanced Features (Weeks 7-8)
- [ ] AI/ML model integration
- [ ] Participant portal
- [ ] Advanced analytics
- [ ] Performance optimization
- [ ] Security hardening

### Phase 5: Deployment (Week 9-10)
- [ ] User acceptance testing
- [ ] Training material preparation
- [ ] Data migration
- [ ] Go-live preparation
- [ ] Post-deployment support

---

## 6. Usage Guidelines

### 6.1 For Developers Using Claude Code

#### Initial Setup
```bash
# Navigate to your OpenSpecimen customization directory
cd ~/openspecimen-customization

# Start Claude Code
claude-code

# First message to Claude Code:
"I need help customizing OpenSpecimen for the BHARAT Study. 
Here's the complete context document: [paste this entire document]"
```

#### Effective Prompting Patterns

**Pattern 1: Configuration Generation**
```
"Based on the BHARAT Study requirements in section 3.4, 
create the JSON configuration for the blood processing workflow 
including all validation rules and automated calculations."
```

**Pattern 2: API Integration**
```
"Create a Python script using the OpenSpecimen REST API to:
1. Authenticate using the credentials
2. Create a new collection protocol for BHARAT Study
3. Add the visit schedule as defined in section 3.4.1
4. Include error handling and logging"
```

**Pattern 3: Custom Form Development**
```
"Generate the complete custom form configuration for 
DNA extraction tracking as specified in section 3.5.1, 
including all validation rules and conditional logic."
```

#### Best Practices

1. **Start Small**: Begin with one component and iterate
2. **Test Thoroughly**: Always test in staging environment first
3. **Document Everything**: Request documentation with each component
4. **Version Control**: Use Git for all customizations
5. **Modular Approach**: Build reusable components

#### Common Tasks and Prompts

**Dashboard Creation**:
```
"Create a dashboard widget configuration that shows 
real-time sample collection progress by age cohort 
using the specifications in section 3.2.1"
```

**Report Generation**:
```
"Build a Python script that generates the weekly 
progress report including all metrics from section 3.2"
```

**Data Validation**:
```
"Create validation functions for the participant 
import template that check all rules specified 
in section 3.8.1"
```

### 6.2 For Laboratory Staff

1. **Daily Operations**
   - Check dashboard for pending tasks
   - Process samples within time limits
   - Update sample status promptly
   - Report any system issues

2. **Quality Control**
   - Verify sample IDs before processing
   - Check temperature logs daily
   - Document any deviations
   - Perform weekly inventory counts

3. **Data Entry**
   - Use barcode scanners when possible
   - Double-check manual entries
   - Complete all required fields
   - Add notes for any anomalies

### 6.3 For Study Coordinators

1. **Participant Management**
   - Monitor enrollment progress
   - Schedule follow-up visits
   - Track compliance rates
   - Generate monthly reports

2. **Site Coordination**
   - Distribute collection kits
   - Monitor site performance
   - Coordinate training sessions
   - Manage supply chain

---

## Appendices

### Appendix A: Abbreviations

| Abbreviation | Full Form |
|--------------|-----------|
| BHARAT | Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions |
| LIMS | Laboratory Information Management System |
| SOP | Standard Operating Procedure |
| QC | Quality Control |
| API | Application Programming Interface |
| ICMR | Indian Council of Medical Research |
| IISc | Indian Institute of Science |

### Appendix B: Contact Information

**Technical Support**: openspecimen-support@longevityindia.org  
**Study Coordination**: bharat-study@longevityindia.org  
**Emergency Contact**: +91-XXXXXXXXXX (24/7 Hotline)

### Appendix C: References

1. OpenSpecimen Documentation: https://openspecimen.atlassian.net/
2. ICMR Ethical Guidelines: https://icmr.gov.in/
3. Longevity India Initiative: https://longevity.iisc.ac.in/
4. BHARAT Study Protocol: [Internal Document]

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2025 | BHARAT Study Team | Initial version |

---

*This document is confidential and proprietary to Longevity India Initiative, IISc Bangalore.*