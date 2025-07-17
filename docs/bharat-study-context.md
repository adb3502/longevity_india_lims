# BHARAT Study & Longevity India: Complete Context for LIMS Development

## Organization Overview

**Longevity India** is a research initiative at the Indian Institute of Science (IISc) focused on understanding aging and healthspan in the Indian population. The organization aims to identify biomarkers of healthy aging, resilience, adversity, and transitions through comprehensive multiomics approaches.

## The BHARAT Study

**BHARAT** stands for **Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions**

### Study Design
- **Type**: Cross-sectional population cohort study with longitudinal follow-up planned
- **Target**: 5,000 participants across India
- **Age Groups**: 5 groups (18-29, 30-44, 45-59, 60-74, 75+)
- **Gender Balance**: Equal representation (50% male, 50% female)
- **Geographic Distribution**: Multiple hospital centers across India

### Scientific Objectives
1. **Create an Indian aging reference database** - First comprehensive multiomics dataset for Indian population
2. **Identify aging biomarkers** - Discover markers specific to Indian genetics and lifestyle
3. **Understand resilience factors** - Why some individuals age healthier than others
4. **Track transitions** - Monitor how people move between health states
5. **Enable precision medicine** - Develop India-specific interventions

### Multiomics Approach
The study collects multiple data layers from each participant:

1. **Genomics**
   - SNP array (Illumina) - Genetic variants
   - Methylation array (Illumina) - Epigenetic aging markers

2. **Proteomics**
   - Serum proteomics - Circulating protein profiles
   - Targeted panels for aging-related proteins

3. **Metabolomics**
   - Small molecule profiling
   - Lipid profiles (Lipidomics)
   - Energy metabolism markers

4. **Immunophenotyping**
   - Flow cytometry - Immune cell populations
   - T-cell, B-cell, NK cell distributions
   - Immunosenescence markers

5. **Clinical Data**
   - Comprehensive blood tests (CBC, liver, kidney, lipids, vitamins)
   - Anthropometric measurements
   - Medical history and medications
   - Lifestyle factors

## Current Workflow & Pain Points

### Recruitment & Enrollment
**Current Process**:
1. Volunteers fill interest form on website
2. Sampling manager calls to verify eligibility
3. Schedule appointment at hospital hub
4. Manager opens Excel sheet and assigns codes
5. Manual tracking of appointments

**Pain Points**:
- Excel-based tracking is error-prone
- No real-time visibility of enrollment balance
- Manual code assignment is tedious
- Difficult to track no-shows and reschedules

### Sample Collection
**Current Process**:
1. Participant arrives at hospital
2. Consent forms signed
3. Clinical intern checks vitals and exclusion criteria
4. Doctor confirms eligibility
5. Samples collected:
   - 25mL blood (split into EDTA and SST tubes)
   - Urine sample
   - Hair strands
   - Cheek swab
   - Stool kit provided (optional, using Decode Age kit)
6. Labels prepared previous day
7. Metadata recorded in Epicollect

**Pain Points**:
- Pre-printing labels wastes materials if participant doesn't show
- No real-time tracking of what's collected
- Manual data entry into multiple systems
- Difficult to track which samples yielded adequate volume

### Sample Processing
**Current Process**:
1. Some blood sent to diagnostic labs (1MG, Healthians, Lal Path)
2. Remaining blood processed:
   - Centrifugation for plasma/serum separation
   - Aliquoting (variable volumes)
   - Snap freezing in liquid nitrogen
   - Storage in -80°C freezers
3. Results received as CSV/PDF from labs
4. PDFs sent to participants as reward

**Pain Points**:
- Variable aliquot volumes hard to track
- Manual recording of storage locations
- CSV files need manual processing
- No integration between lab results and sample database

### Data Management
**Current Infrastructure**:
- NAS with 16TB × 8 HDDs for data storage
- Workstation 1: OpenSpecimen installation
- Workstation 2: Analysis workstation
- Freedom EVO liquid handling robot
- Flow cytometer for immunophenotyping

**Pain Points**:
- No unified view of participant data
- Siloed data sources (Epicollect, lab results, flow data)
- Manual data compilation for analysis
- No automated pipelines

## Proposed Architecture & Solutions

### System Design Philosophy
**Participant-Centric Model**: Every piece of data links back to a participant code (e.g., RAM-1A-001)

### Coding Strategy Refinement
**Format**: `[CENTER]-[GROUP][GENDER]-[SERIAL]`
- CENTER: 3-letter code (RAM = Ramaiah Hospital)
- GROUP: Age group (1-5)
- GENDER: A=Male, B=Female
- SERIAL: 3-digit sequential (001-999)

**Visual Coding**:
- Cryocap colors: By age group (1=Blue, 2=Green, 3=Yellow, 4=Orange, 5=Red)
- Label borders: By gender (Male=Blue, Female=Pink)
- 2D barcode: Contains full metadata

### Data Flow Architecture
```
Field Collection → Real-time Integration → Unified Database → Analysis
       ↓                    ↓                    ↓              ↓
  ODK Collect          Lab APIs           OpenSpecimen      Dashboards
                    Epicollect Sync                        Export Tools
```

### Key Innovations
1. **Dynamic Code Assignment**: Codes assigned when participant arrives, not pre-assigned
2. **Real-time Integration**: APIs pull data automatically from all sources
3. **Unified Timeline**: See all events for a participant chronologically
4. **Smart Batching**: System suggests optimal batches for multiomics to minimize batch effects
5. **Quality Tracking**: Automated QC checks at each step

## Technical Requirements

### Functional Requirements
1. **Enrollment Management**
   - Generate participant codes on-demand
   - Track enrollment balance by age/gender/center
   - Manage consent and eligibility

2. **Sample Tracking**
   - Barcode scanning at collection
   - Hierarchical sample relationships (parent → aliquots)
   - Storage location management
   - Chain of custody

3. **Data Integration**
   - Pull from Epicollect API
   - Integrate lab results (1MG, Healthians, Lal Path APIs)
   - Import flow cytometry FCS files
   - Parse Freedom EVO outputs

4. **Analysis Support**
   - Batch samples for multiomics
   - Track processing status
   - Link raw data files to samples
   - Export for statistical analysis

5. **Quality Management**
   - Flag hemolyzed samples
   - Track failed QC
   - Monitor data completeness
   - Alert on deviations

### Non-Functional Requirements
1. **Performance**: Handle 5000+ participants with millions of aliquots
2. **Reliability**: 99.9% uptime for critical sampling operations
3. **Security**: PHI protection, role-based access control
4. **Scalability**: Design for future expansion to 50,000 participants
5. **Usability**: Intuitive for non-technical staff

## User Personas

### Sampling Manager (Primary User)
- Needs to track enrollment balance
- Assigns participants to time slots
- Monitors sample collection metrics
- Generates reports for PIs

### Clinical Intern (Field User)
- Collects samples at hospital
- Records metadata
- Prints labels
- Needs simple, fast interface

### Lab Technician (Processing User)
- Processes samples into aliquots
- Records storage locations
- Manages batch creation
- Tracks QC results

### Data Scientist (Analysis User)
- Queries integrated datasets
- Exports data for analysis
- Creates visualizations
- Needs comprehensive data access

### Principal Investigator (Oversight User)
- Views high-level dashboards
- Monitors study progress
- Reviews quality metrics
- Makes strategic decisions

## Success Metrics
1. **Efficiency**: Reduce enrollment time from 30 min to 10 min per participant
2. **Accuracy**: <0.1% sample mislabeling rate
3. **Completeness**: >95% data completeness within 7 days
4. **Integration**: 100% automated data import from external sources
5. **User Satisfaction**: >90% user satisfaction score

## Future Roadmap
1. **Phase 1** (Current): Basic LIMS for 5,000 participants
2. **Phase 2**: Participant portal for result access
3. **Phase 3**: AI-powered analysis pipelines
4. **Phase 4**: Expand to 50,000 participants
5. **Phase 5**: National biobank network integration

## Development Principles
1. **Start Simple**: Get core workflow running first
2. **Iterate Quickly**: Deploy updates weekly
3. **User-Driven**: Regular feedback from field staff
4. **Data Quality First**: Better to have less data that's accurate
5. **Future-Proof**: Design for 10x scale from day one

This context should help Claude Code understand not just WHAT to build, but WHY each feature matters and HOW it fits into the larger scientific mission of understanding aging in India.

## Change History

### 2025-07-16 - Initial Implementation
- Created comprehensive BHARAT study context documentation
- Defined participant coding system: [CENTER]-[GROUP][GENDER]-[SERIAL]
- Established visual coding scheme for cryocaps and labels
- Outlined multiomics data integration strategy
- Documented current workflow pain points and proposed solutions
- Defined user personas and success metrics
- Created future roadmap for system expansion