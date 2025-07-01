# BHARAT Study Specimen Labeling System Guide

This guide details the complete hierarchical specimen numbering system implemented for the BHARAT Study in OpenSpecimen.

## Overview

The BHARAT Study uses a comprehensive hierarchical labeling system to ensure unique identification and traceability of all participants and specimens throughout the 24-month longitudinal study.

### Labeling Hierarchy

```
Study Level: BHARAT
├── Participants: BHARAT-AG3-P0234
├── Specimens: BHARAT-AG3-P0234-V2-BLD01
├── Derivatives: BHARAT-AG3-P0234-V2-BLD01-PLA-01
└── Aliquots: BHARAT-AG3-P0234-V2-BLD01-PROT-01
```

## Participant Identification (PPID)

### Format: `BHARAT-AGx-Pxxxx`

**Components:**
- **BHARAT**: Study identifier
- **AGx**: Age cohort (AG1-AG5)
- **Pxxxx**: Participant number (4 digits, zero-padded)

### Age Cohorts

| Cohort | Age Range | Description | Example PPID |
|--------|-----------|-------------|--------------|
| AG1 | 20-30 years | Young Adults | BHARAT-AG1-P0001 |
| AG2 | 31-40 years | Early Adults | BHARAT-AG2-P0156 |
| AG3 | 41-50 years | Middle Adults | BHARAT-AG3-P0234 |
| AG4 | 51-60 years | Late Adults | BHARAT-AG4-P0389 |
| AG5 | 61-70 years | Senior Adults | BHARAT-AG5-P0567 |

### Examples
```
BHARAT-AG1-P0001  # First participant, age 20-30
BHARAT-AG3-P0234  # 234th participant, age 41-50  
BHARAT-AG5-P1000  # 1000th participant, age 61-70
```

## Visit Identification

### Format: `Vx`

| Visit Code | Timepoint | Description | Window |
|------------|-----------|-------------|---------|
| V0 | Day 0 | Baseline Visit | Enrollment |
| V1 | Day 180 | 6 Month Follow-up | ±14 days |
| V2 | Day 365 | 12 Month Follow-up | ±14 days |
| V3 | Day 730 | 24 Month Final Visit | ±14 days |

## Primary Specimen Identification

### Format: `{PPID}-{Visit}-{Type}{Number}`

**Components:**
- **PPID**: Participant identifier
- **Visit**: Visit code (V0-V3)
- **Type**: Specimen type abbreviation
- **Number**: Sequential number (01-99)

### Specimen Type Abbreviations

| Specimen Type | Abbreviation | Examples |
|---------------|--------------|----------|
| Whole Blood | BLD | BLD01, BLD02, BLD03, BLD04 |
| Plasma | PLA | PLA01, PLA02 |
| Serum | SER | SER01, SER02 |
| Buffy Coat | BC | BC01, BC02 |
| Red Blood Cells | RBC | RBC01, RBC02 |
| Saliva | SAL | SAL01 |
| Hair | HAR | HAR01 |
| Buccal Cells | CEL | CEL01, CEL02 |

### Primary Specimen Examples
```
BHARAT-AG3-P0234-V0-BLD01  # First blood tube, baseline visit
BHARAT-AG3-P0234-V0-BLD02  # Second blood tube, baseline visit
BHARAT-AG3-P0234-V0-SAL01  # Saliva sample, baseline visit
BHARAT-AG3-P0234-V1-BLD01  # Blood tube, 6-month follow-up
BHARAT-AG3-P0234-V2-HAR01  # Hair sample, 12-month follow-up
```

## Derivative Specimen Identification

### Format: `{Parent_Label}-{Type}-{Number}`

Derivatives are created from primary specimens through processing (e.g., centrifugation).

### Examples
```
BHARAT-AG3-P0234-V0-BLD01-PLA-01  # Plasma from first blood tube
BHARAT-AG3-P0234-V0-BLD01-BC-01   # Buffy coat from first blood tube
BHARAT-AG3-P0234-V0-BLD01-RBC-01  # RBCs from first blood tube
BHARAT-AG3-P0234-V0-BLD02-PLA-01  # Plasma from second blood tube
```

## Aliquot Identification (Analysis-Specific)

### Format: `{Parent_Label}-{Analysis}-{Number}`

Aliquots are created for specific analyses and include the analysis type code.

### Analysis Type Codes

| Analysis Type | Code | Description |
|---------------|------|-------------|
| Genomics | GEN | Whole genome sequencing, SNP arrays |
| Proteomics | PROT | Protein expression, mass spectrometry |
| Metabolomics | META | Small molecule analysis |
| Epigenomics | EPI | DNA methylation, histone modifications |
| Clinical Chemistry | CLIN | Standard clinical lab tests |
| Flow Cytometry | FLOW | Cell population analysis |
| DNA Extraction | DNA | Extracted DNA for downstream analysis |
| RNA Extraction | RNA | Extracted RNA for downstream analysis |

### Aliquot Examples
```
BHARAT-AG3-P0234-V0-BLD01-PROT-01   # Proteomics aliquot #1
BHARAT-AG3-P0234-V0-BLD01-PROT-02   # Proteomics aliquot #2
BHARAT-AG3-P0234-V0-BLD01-DNA-01    # DNA extraction aliquot
BHARAT-AG3-P0234-V1-SAL01-META-01   # Metabolomics from saliva
BHARAT-AG3-P0234-V2-HAR01-GEN-01    # Genomics from hair
```

## Collection Schedule and Samples

### Visit V0 (Baseline) - Complete Assessment
```
BHARAT-AG3-P0234-V0-BLD01  # Blood tube 1 (5ml EDTA)
BHARAT-AG3-P0234-V0-BLD02  # Blood tube 2 (5ml EDTA) 
BHARAT-AG3-P0234-V0-BLD03  # Blood tube 3 (5ml EDTA)
BHARAT-AG3-P0234-V0-BLD04  # Blood tube 4 (5ml EDTA)
BHARAT-AG3-P0234-V0-SAL01  # Saliva (5ml)
BHARAT-AG3-P0234-V0-HAR01  # Hair follicles (50 strands)
BHARAT-AG3-P0234-V0-CEL01  # Buccal swab 1
BHARAT-AG3-P0234-V0-CEL02  # Buccal swab 2
```

### Visit V1 (6 Month) - Brief Follow-up
```
BHARAT-AG3-P0234-V1-BLD01  # Blood tube 1 (5ml EDTA)
BHARAT-AG3-P0234-V1-BLD02  # Blood tube 2 (5ml EDTA)
BHARAT-AG3-P0234-V1-SAL01  # Saliva (5ml)
```

### Visit V2 (12 Month) - Annual Assessment
```
BHARAT-AG3-P0234-V2-BLD01  # Blood tube 1 (5ml EDTA)
BHARAT-AG3-P0234-V2-BLD02  # Blood tube 2 (5ml EDTA)
BHARAT-AG3-P0234-V2-BLD03  # Blood tube 3 (5ml EDTA)
BHARAT-AG3-P0234-V2-BLD04  # Blood tube 4 (5ml EDTA)
BHARAT-AG3-P0234-V2-SAL01  # Saliva (5ml)
BHARAT-AG3-P0234-V2-HAR01  # Hair follicles (50 strands)
BHARAT-AG3-P0234-V2-CEL01  # Buccal swab 1
BHARAT-AG3-P0234-V2-CEL02  # Buccal swab 2
```

### Visit V3 (24 Month) - Final Assessment
```
BHARAT-AG3-P0234-V3-BLD01  # Blood tube 1 (5ml EDTA)
BHARAT-AG3-P0234-V3-BLD02  # Blood tube 2 (5ml EDTA)
BHARAT-AG3-P0234-V3-BLD03  # Blood tube 3 (5ml EDTA)
BHARAT-AG3-P0234-V3-BLD04  # Blood tube 4 (5ml EDTA)
BHARAT-AG3-P0234-V3-SAL01  # Saliva (5ml)
BHARAT-AG3-P0234-V3-HAR01  # Hair follicles (50 strands)
BHARAT-AG3-P0234-V3-CEL01  # Buccal swab 1
BHARAT-AG3-P0234-V3-CEL02  # Buccal swab 2
```

## Storage Container Labeling

### Box Format: `BHARAT-{Site}-{Freezer}-{Rack}-{Box}`

**Components:**
- **BHARAT**: Study identifier
- **Site**: Collection site code
- **Freezer**: Freezer identifier
- **Rack**: Rack identifier within freezer
- **Box**: Box number (3 digits)

### Site Codes
| Site | Code | Institution |
|------|------|-------------|
| Bangalore IISc | BLR | Indian Institute of Science |
| MS Ramaiah | MSR | MS Ramaiah Hospital |
| BMC | BMC | Bangalore Medical College |

### Examples
```
BHARAT-BLR-F01-R03-B045  # Box 45, Rack 3, Freezer 1, IISc Bangalore
BHARAT-MSR-F02-R01-B012  # Box 12, Rack 1, Freezer 2, MS Ramaiah
BHARAT-BMC-F01-R05-B078  # Box 78, Rack 5, Freezer 1, BMC
```

## Implementation Files

### 1. Configuration Files
- **`bharat-study-labeling-config.json`** - Complete labeling configuration
- **`setup-bharat-labeling.py`** - Automated setup script
- **`test-bharat-labeling.py`** - Validation and testing script

### 2. Setup Process
```bash
# 1. Setup collection protocol (if not done)
python setup-bharat-study-protocol.py

# 2. Setup labeling system
python setup-bharat-labeling.py

# 3. Validate implementation
python test-bharat-labeling.py
```

## Validation Rules

### Participant ID Pattern
```regex
^BHARAT-AG[1-5]-P\d{4}$
```
- Must start with "BHARAT-AG"
- Cohort must be 1-5
- Must have "-P" prefix before 4-digit number

### Specimen Label Pattern
```regex
^BHARAT-AG[1-5]-P\d{4}-V[0-3]-[A-Z]{2,4}\d{2}$
```
- Must include valid participant ID
- Visit must be V0-V3
- Type abbreviation 2-4 uppercase letters
- Two-digit sequential number

### Aliquot Label Pattern
```regex
^BHARAT-AG[1-5]-P\d{4}-V[0-3]-[A-Z]{2,4}\d{2}-[A-Z]{2,5}-\d{2}$
```
- Must include valid specimen label
- Analysis type 2-5 uppercase letters
- Two-digit sequential number

## Database Configuration

### Custom Fields Added

**Participant Level:**
- `cohort` (Dropdown: AG1, AG2, AG3, AG4, AG5)
- `enrollmentSite` (Dropdown: BLR, MSR, BMC)

**Specimen Level:**
- `analysisType` (Dropdown: GEN, PROT, META, EPI, CLIN, FLOW, DNA, RNA)
- `processingBatch` (Text field)
- `freezeThawCycles` (Integer, default: 0)

### Label Format Configuration

**Collection Protocol Settings:**
```json
{
  "ppidFmt": "%CP_CODE%-%CUSTOM_FIELD(cpr,cohort)%-%SYS_UID(4)%",
  "visitNameFmt": "%EVENT_CODE%",
  "specimenLabelFmt": "%PPI%-%VISIT_NAME%-%SP_TYPE_ABBR%%SYS_UID(2)%",
  "derivativeLabelFmt": "%PARENT_SPMN_LABEL%-%SP_TYPE_ABBR%-%SYS_UID(2)%",
  "aliquotLabelFmt": "%PARENT_SPMN_LABEL%-%CUSTOM_FIELD(specimen,analysisType)%-%SYS_UID(2)%"
}
```

## User Workflows

### 1. Participant Registration
1. Select age cohort (AG1-AG5) based on participant age
2. System generates PPID: `BHARAT-AGx-Pxxxx`
3. Complete demographic information
4. Save participant record

### 2. Specimen Collection
1. Select participant and visit
2. Create specimens according to visit schedule
3. System generates labels: `BHARAT-AGx-Pxxxx-Vx-TYPExx`
4. Print barcode labels for tubes
5. Collect specimens according to protocol

### 3. Specimen Processing
1. Scan specimen barcodes
2. Process according to SOPs (centrifugation, aliquoting)
3. Create derivatives with system-generated labels
4. Store in designated freezer locations
5. Update specimen status and location

### 4. Analysis Preparation
1. Select specimens for analysis
2. Create aliquots with analysis type selection
3. System generates labels: `Parent-ANALYSIS-xx`
4. Transfer to analysis laboratory
5. Track analysis progress

## Quality Control

### 1. Label Verification
- Double-check participant age matches cohort
- Verify visit timing according to protocol
- Confirm specimen type matches collection requirements
- Validate label format before printing

### 2. Barcode Scanning
- Scan labels during collection
- Verify scanned data matches expected format
- Flag any label format errors immediately
- Maintain scan logs for audit trail

### 3. System Validation
- Run regular label format validation tests
- Check for duplicate labels
- Verify sequential numbering
- Monitor system performance

## Troubleshooting

### Common Issues

**Incorrect Age Cohort:**
- Issue: Participant age doesn't match selected cohort
- Solution: Verify participant birth date and recalculate age
- Prevention: Implement age validation rules

**Label Format Errors:**
- Issue: Labels don't follow expected format
- Solution: Check custom field configuration and label formats
- Prevention: Regular system validation tests

**Missing Sequential Numbers:**
- Issue: Gaps in specimen numbering sequence
- Solution: Check for deleted specimens or system errors
- Prevention: Monitor sequence generation logs

**Duplicate Labels:**
- Issue: Same label generated for different specimens
- Solution: Check sequence key configuration
- Prevention: Implement uniqueness constraints

### Support Contacts

- **Technical Issues**: openspecimen-support@longevityindia.org
- **Study Coordination**: bharat-study@longevityindia.org
- **Emergency Support**: +91-XXXXXXXXXX (24/7)

## Best Practices

### 1. Label Management
- Always verify labels before printing
- Use high-quality barcode printers
- Store backup copies of label formats
- Regular printer maintenance and calibration

### 2. Data Entry
- Double-check participant demographics
- Verify visit dates and timing
- Use barcode scanning whenever possible
- Implement data validation rules

### 3. Training
- Train all staff on labeling conventions
- Provide quick reference guides
- Conduct regular refresher sessions
- Document all procedures clearly

### 4. System Maintenance
- Regular backups of labeling configuration
- Monitor system performance
- Update label formats as needed
- Test changes in staging environment first

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Author**: Longevity India BHARAT Study Team