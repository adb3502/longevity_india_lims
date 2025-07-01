# BHARAT Study Collection Protocol Setup Guide

This guide provides step-by-step instructions for setting up the BHARAT Study collection protocol in OpenSpecimen.

## Overview

The BHARAT Study (Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions) is a longitudinal aging research study with the following characteristics:

- **Duration**: 24 months per participant
- **Visits**: 4 visits (V0, V1, V2, V3) at baseline, 6mo, 12mo, 24mo
- **Age Cohorts**: 5 groups (20-30, 31-40, 41-50, 51-60, 61-70 years)
- **Sample Types**: Blood (4x5ml EDTA), Saliva, Hair follicles, Buccal cells
- **Sites**: IISc Bangalore, MS Ramaiah Hospital, BMC

## Files Generated

1. **`bharat-study-collection-protocol.json`** - Complete protocol configuration
2. **`setup-bharat-study-protocol.py`** - Automated setup script
3. **`BHARAT-STUDY-SETUP-GUIDE.md`** - This documentation

## Prerequisites

### System Requirements
- OpenSpecimen Community Edition (latest version) 
- MySQL database configured
- Java 16+ and Tomcat 9+
- Python 3.6+ with `requests` library

### Access Requirements
- Admin access to OpenSpecimen instance
- Network access to OpenSpecimen server
- Proper authentication credentials

## Setup Methods

### Method 1: Automated Setup (Recommended)

Use the Python script for automated configuration:

```bash
# 1. Install Python dependencies
pip install requests

# 2. Make the script executable
chmod +x setup-bharat-study-protocol.py

# 3. Run the setup script
python setup-bharat-study-protocol.py
```

The script will prompt for:
- OpenSpecimen admin username (default: admin@openspecimen.org)
- Password (default: Login!@#)

**What the script does:**
1. ✅ Authenticates with OpenSpecimen
2. ✅ Checks for existing BHARAT protocol
3. ✅ Creates required sites (IISc, MSR, BMC)
4. ✅ Creates study users (PI, Coordinator)
5. ✅ Validates specimen types
6. ✅ Creates the complete collection protocol
7. ✅ Sets up age cohort groups
8. ✅ Generates setup report

### Method 2: Manual Setup via Web Interface

1. **Login to OpenSpecimen**
   - Navigate to your OpenSpecimen instance
   - Login with admin credentials

2. **Create Sites**
   - Go to Settings → Sites
   - Create three sites:
     - IISc Bangalore (Code: BLR)
     - MS Ramaiah Hospital (Code: MSR) 
     - Bangalore Medical College (Code: BMC)

3. **Create Users**
   - Go to Settings → Users
   - Create PI and Coordinator accounts

4. **Import Protocol**
   - Go to Collection Protocols
   - Use "Import" feature
   - Upload `bharat-study-collection-protocol.json`

### Method 3: REST API Setup

Use curl commands to setup via REST API:

```bash
# 1. Authenticate
curl -X POST "http://localhost:8080/openspecimen/rest/ng/sessions" \
     -H "Content-Type: application/json" \
     -d '{"loginName":"admin@openspecimen.org","password":"Login!@#","domainName":"openspecimen"}'

# 2. Create collection protocol
curl -X POST "http://localhost:8080/openspecimen/rest/ng/collection-protocols" \
     -H "Content-Type: application/json" \
     -H "X-OS-API-TOKEN: YOUR_TOKEN_HERE" \
     -d @bharat-study-collection-protocol.json
```

## Protocol Configuration Details

### Collection Schedule

| Visit | Timepoint | Samples Collected | Purpose |
|-------|-----------|-------------------|---------|
| V0 (Baseline) | Day 0 | 4×Blood, Saliva, Hair, 2×Buccal | Complete baseline assessment |
| V1 (6 Month) | Day 180±14 | 2×Blood, Saliva | Brief follow-up |
| V2 (12 Month) | Day 365±14 | 4×Blood, Saliva, Hair, 2×Buccal | Annual assessment |
| V3 (24 Month) | Day 730±14 | 4×Blood, Saliva, Hair, 2×Buccal | Final assessment |

### Sample Collection Requirements

**Blood Samples (EDTA tubes):**
- Volume: 5ml per tube
- Processing: Within 2 hours
- Storage: -80°C after processing
- Derivatives: Plasma, buffy coat, RBCs

**Saliva Samples:**
- Volume: 5ml collection tube
- Processing: Room temp 30min, then aliquot
- Storage: Flash freeze → -80°C

**Hair Samples:**
- Count: 50 strands with follicles
- Storage: Room temperature
- Container: Collection envelope

**Buccal Cell Samples:**
- Count: 2 swabs per visit
- Storage: Room temperature
- Processing: Air dry before storage

### Participant Identification Format

**Participant Protocol ID (PPID):**
```
Format: BHARAT-{AG}{cohort}-P{number}
Example: BHARAT-AG3-P0234

Cohort Codes:
- AG1: Ages 20-30
- AG2: Ages 31-40  
- AG3: Ages 41-50
- AG4: Ages 51-60
- AG5: Ages 61-70
```

**Specimen Labels:**
```
Format: {PPID}-{Visit}-{Type}{Number}
Examples:
- BHARAT-AG3-P0234-V0-BLD01
- BHARAT-AG3-P0234-V1-SAL01
- BHARAT-AG3-P0234-V2-HAR01
```

## Post-Setup Configuration

After running the setup, complete these additional configurations:

### 1. Configure Specimen Processing Workflows
- Set up automated aliquoting rules
- Configure derivative creation
- Set up quality control checks

### 2. Setup Multi-Omics Forms
- DNA extraction tracking
- Genomics analysis forms
- Proteomics workflow forms
- Metabolomics data collection

### 3. Configure Dashboards
- Age cohort progress tracking
- Sample collection metrics
- Processing queue status
- Quality control alerts

### 4. Inventory Management
- Kit stock levels and reorder points
- Reagent expiry tracking
- Equipment monitoring

### 5. User Training
- Study coordinator training
- Laboratory staff workflows
- Data entry protocols
- Quality control procedures

## Verification Steps

After setup completion, verify the following:

### ✅ Collection Protocol Checklist
- [ ] BHARAT-STUDY protocol visible in CP list
- [ ] 4 events configured (V0, V1, V2, V3)
- [ ] Correct specimen requirements per visit
- [ ] Proper labeling formats
- [ ] Age cohort groups created

### ✅ Site Configuration Checklist  
- [ ] IISc Bangalore site active
- [ ] MS Ramaiah Hospital site active
- [ ] BMC site active
- [ ] Proper site assignments in protocol

### ✅ User Access Checklist
- [ ] PI account created and functional
- [ ] Coordinator account created
- [ ] Proper role assignments
- [ ] Email notifications configured

## Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify OpenSpecimen URL is correct
- Check username/password credentials
- Ensure admin privileges

**Site Creation Failures:**
- Check for duplicate site names
- Verify institute names exist
- Confirm required fields completed

**Protocol Import Errors:**
- Validate JSON file format
- Check for missing required fields
- Verify specimen types exist

**Missing Specimen Types:**
- Add "Hair" to specimen types if needed
- Add "Buccal Cells" if not present
- Check permissible values configuration

### Support Contacts

- **Technical Support**: openspecimen-support@longevityindia.org
- **Study Coordination**: bharat-study@longevityindia.org  
- **Emergency**: +91-XXXXXXXXXX (24/7 Hotline)

## Next Steps

1. **Review Configuration**: Verify all settings match study requirements
2. **Test Workflows**: Create test participants and specimens
3. **Train Staff**: Conduct training sessions for study team
4. **Go Live**: Begin participant enrollment
5. **Monitor**: Track system performance and data quality

## References

- [OpenSpecimen Documentation](https://openspecimen.atlassian.net/)
- [BHARAT Study Protocol](bharat-study-context-doc.md)
- [Longevity India Initiative](https://longevity.iisc.ac.in/)

---

**Document Version**: 1.0  
**Last Updated**: January 2025  
**Author**: Longevity India BHARAT Study Team