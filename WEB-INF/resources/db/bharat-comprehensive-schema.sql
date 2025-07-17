-- ============================================================================
-- BHARAT Study Comprehensive Database Schema
-- Designed for Multi-Omics Data Integration with Participant ID Linking
-- ============================================================================

-- Core participant registry with unique identifier linking
CREATE TABLE IF NOT EXISTS os_bharat_participants (
    participant_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    bharat_code VARCHAR(20) UNIQUE NOT NULL,           -- RAM-1A-001 format
    center_code VARCHAR(10) NOT NULL,                  -- RAM, SSI, BAP, BMC
    age_group INT NOT NULL,                            -- 1-5 age groups
    gender CHAR(1) NOT NULL,                           -- A=Male, B=Female
    sequential_number INT NOT NULL,                    -- 001-999
    epicollect_uuid VARCHAR(100) UNIQUE,               -- Original Epicollect UUID
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    data_privacy_consent BOOLEAN DEFAULT FALSE,
    study_status ENUM('ACTIVE', 'COMPLETED', 'WITHDRAWN', 'SUSPENDED') DEFAULT 'ACTIVE',
    
    -- Composite indexes for performance
    INDEX idx_bharat_code (bharat_code),
    INDEX idx_center_age_gender (center_code, age_group, gender),
    INDEX idx_epicollect_uuid (epicollect_uuid),
    INDEX idx_study_status (study_status)
);

-- ============================================================================
-- DATA INTEGRATION TRACKING
-- ============================================================================

-- Track all data imports and integrations
CREATE TABLE IF NOT EXISTS os_bharat_data_integrations (
    integration_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    source_system VARCHAR(50) NOT NULL,               -- EPICOLLECT, LAB_1MG, HEALTHIANS, etc.
    source_record_id VARCHAR(100),                    -- External system ID
    data_type VARCHAR(50) NOT NULL,                   -- CLINICAL, BLOODWORK, OMICS, etc.
    raw_data JSON,                                    -- Complete original data
    processed_data JSON,                              -- Cleaned and validated data
    import_status ENUM('PENDING', 'SUCCESS', 'FAILED', 'PARTIAL') DEFAULT 'PENDING',
    error_message TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP NULL,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    INDEX idx_participant_source (participant_id, source_system),
    INDEX idx_data_type (data_type),
    INDEX idx_import_status (import_status),
    INDEX idx_imported_at (imported_at)
);

-- ============================================================================
-- CLINICAL METADATA (From Epicollect)
-- ============================================================================

-- Clinical assessments and vitals
CREATE TABLE IF NOT EXISTS os_bharat_clinical_data (
    clinical_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    assessment_date DATE NOT NULL,
    assessment_type VARCHAR(50) NOT NULL,             -- SCREENING, BASELINE, FOLLOW_UP
    
    -- Vital signs
    pulse_rate INT,                                   -- beats per minute
    blood_pressure_systolic INT,                      -- mmHg
    blood_pressure_diastolic INT,                     -- mmHg
    respiratory_rate INT,                             -- breaths per minute
    oxygen_saturation INT,                            -- SpO2 percentage
    temperature_celsius DECIMAL(4,2),                 -- Body temperature
    
    -- Physical measurements
    height_cm DECIMAL(5,2),
    weight_kg DECIMAL(5,2),
    bmi DECIMAL(4,2),
    waist_circumference_cm DECIMAL(5,2),
    hip_circumference_cm DECIMAL(5,2),
    
    -- Clinical assessments
    medical_history JSON,                             -- Structured medical history
    current_medications JSON,                         -- Current medication list
    lifestyle_factors JSON,                           -- Exercise, diet, smoking, etc.
    
    -- Metadata
    recorded_by VARCHAR(100),
    collection_site VARCHAR(100),
    data_completeness DECIMAL(5,2),                   -- Percentage complete
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    INDEX idx_participant_assessment (participant_id, assessment_date),
    INDEX idx_assessment_type (assessment_type),
    INDEX idx_collection_site (collection_site)
);

-- ============================================================================
-- SAMPLE COLLECTION TRACKING
-- ============================================================================

-- Master sample registry
CREATE TABLE IF NOT EXISTS os_bharat_samples (
    sample_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    sample_code VARCHAR(30) UNIQUE NOT NULL,          -- RAM-1A-001-BL-001
    sample_type VARCHAR(50) NOT NULL,                 -- BLOOD, URINE, STOOL, HAIR, SWAB
    sample_subtype VARCHAR(50),                       -- EDTA, SERUM, PLASMA, etc.
    parent_sample_id BIGINT,                          -- For aliquots
    
    -- Collection details
    collection_date TIMESTAMP NOT NULL,
    collection_site VARCHAR(100),
    collected_by VARCHAR(100),
    collection_protocol VARCHAR(100),
    
    -- Storage details
    storage_location VARCHAR(100),
    storage_temperature VARCHAR(20),                  -- -80C, -20C, RT
    storage_container VARCHAR(50),                    -- CRYOTUBE, EPPENDORF, etc.
    
    -- Quality control
    volume_collected_ml DECIMAL(8,3),
    volume_remaining_ml DECIMAL(8,3),
    quality_score DECIMAL(3,2),                       -- 0-10 quality rating
    contamination_flag BOOLEAN DEFAULT FALSE,
    
    -- Status tracking
    sample_status ENUM('COLLECTED', 'PROCESSED', 'ANALYZED', 'EXHAUSTED', 'DISCARDED') DEFAULT 'COLLECTED',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_sample_id) REFERENCES os_bharat_samples(sample_id) ON DELETE SET NULL,
    INDEX idx_participant_sample (participant_id, sample_type),
    INDEX idx_sample_code (sample_code),
    INDEX idx_collection_date (collection_date),
    INDEX idx_sample_status (sample_status),
    INDEX idx_parent_sample (parent_sample_id)
);

-- ============================================================================
-- LABORATORY BLOODWORK DATA
-- ============================================================================

-- Blood test results from various labs
CREATE TABLE IF NOT EXISTS os_bharat_bloodwork (
    bloodwork_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    sample_id BIGINT,
    lab_provider VARCHAR(50) NOT NULL,                -- 1MG, HEALTHIANS, LAL_PATH, etc.
    test_panel VARCHAR(100) NOT NULL,                 -- COMPREHENSIVE, LIPID, DIABETES, etc.
    test_date DATE NOT NULL,
    report_date DATE,
    
    -- Complete Blood Count (CBC)
    hemoglobin DECIMAL(4,2),
    hematocrit DECIMAL(4,2),
    rbc_count DECIMAL(4,2),
    wbc_count DECIMAL(8,2),
    platelet_count DECIMAL(8,2),
    
    -- Lipid Profile
    total_cholesterol DECIMAL(5,2),
    ldl_cholesterol DECIMAL(5,2),
    hdl_cholesterol DECIMAL(5,2),
    triglycerides DECIMAL(5,2),
    
    -- Diabetes Panel
    fasting_glucose DECIMAL(5,2),
    hba1c DECIMAL(4,2),
    insulin DECIMAL(6,2),
    
    -- Kidney Function
    creatinine DECIMAL(4,2),
    bun DECIMAL(4,2),
    egfr DECIMAL(5,2),
    
    -- Liver Function
    alt DECIMAL(5,2),
    ast DECIMAL(5,2),
    alkaline_phosphatase DECIMAL(5,2),
    total_bilirubin DECIMAL(4,2),
    
    -- Inflammatory Markers
    crp DECIMAL(6,3),
    esr DECIMAL(4,2),
    
    -- Vitamins and Minerals
    vitamin_d DECIMAL(5,2),
    vitamin_b12 DECIMAL(6,2),
    folate DECIMAL(5,2),
    iron DECIMAL(5,2),
    ferritin DECIMAL(6,2),
    
    -- Hormones
    tsh DECIMAL(6,3),
    testosterone DECIMAL(6,2),
    cortisol DECIMAL(6,2),
    
    -- Additional biomarkers (JSON for flexibility)
    additional_markers JSON,
    
    -- Quality and metadata
    lab_reference_ranges JSON,
    abnormal_flags JSON,
    interpretation TEXT,
    raw_report_data JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (sample_id) REFERENCES os_bharat_samples(sample_id) ON DELETE SET NULL,
    INDEX idx_participant_bloodwork (participant_id, test_date),
    INDEX idx_lab_provider (lab_provider),
    INDEX idx_test_panel (test_panel),
    INDEX idx_test_date (test_date)
);

-- ============================================================================
-- FLOW CYTOMETRY DATA
-- ============================================================================

-- Flow cytometry analysis results
CREATE TABLE IF NOT EXISTS os_bharat_flow_cytometry (
    flow_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    sample_id BIGINT,
    analysis_date DATE NOT NULL,
    instrument VARCHAR(50),                           -- BD FACSCanto, etc.
    protocol VARCHAR(100),                            -- IMMUNOSENESCENCE, T_CELL_PROFILE, etc.
    
    -- Cell populations (percentages)
    cd3_positive DECIMAL(5,2),                        -- Total T cells
    cd4_positive DECIMAL(5,2),                        -- T helper cells
    cd8_positive DECIMAL(5,2),                        -- Cytotoxic T cells
    cd19_positive DECIMAL(5,2),                       -- B cells
    cd56_positive DECIMAL(5,2),                       -- NK cells
    
    -- Activation markers
    cd25_positive DECIMAL(5,2),                       -- Activated T cells
    cd69_positive DECIMAL(5,2),                       -- Early activation
    hla_dr_positive DECIMAL(5,2),                     -- Late activation
    
    -- Senescence markers
    cd57_positive DECIMAL(5,2),                       -- Senescent cells
    cd28_negative DECIMAL(5,2),                       -- Senescent T cells
    
    -- Memory markers
    cd45ra_positive DECIMAL(5,2),                     -- Naive cells
    cd45ro_positive DECIMAL(5,2),                     -- Memory cells
    ccr7_positive DECIMAL(5,2),                       -- Central memory
    
    -- Additional markers (JSON for flexibility)
    additional_markers JSON,
    
    -- Raw data and metadata
    total_events_acquired BIGINT,
    viability_percent DECIMAL(5,2),
    compensation_applied BOOLEAN DEFAULT FALSE,
    gating_strategy TEXT,
    raw_fcs_file_path VARCHAR(500),
    analysis_software VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (sample_id) REFERENCES os_bharat_samples(sample_id) ON DELETE SET NULL,
    INDEX idx_participant_flow (participant_id, analysis_date),
    INDEX idx_protocol (protocol),
    INDEX idx_analysis_date (analysis_date)
);

-- ============================================================================
-- MULTI-OMICS DATA
-- ============================================================================

-- Genomics data
CREATE TABLE IF NOT EXISTS os_bharat_genomics (
    genomics_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    sample_id BIGINT,
    sequencing_date DATE NOT NULL,
    platform VARCHAR(50),                            -- ILLUMINA, NANOPORE, etc.
    sequencing_type VARCHAR(50),                      -- WGS, WES, TARGETED, etc.
    
    -- Quality metrics
    coverage_depth DECIMAL(6,2),
    read_quality_score DECIMAL(4,2),
    contamination_estimate DECIMAL(4,2),
    
    -- Variant calling results
    total_variants BIGINT,
    snv_count BIGINT,
    indel_count BIGINT,
    structural_variants BIGINT,
    
    -- Ancestry and population genetics
    ancestry_components JSON,
    population_structure JSON,
    
    -- Pharmacogenomics
    drug_response_variants JSON,
    
    -- File paths
    raw_fastq_path VARCHAR(500),
    aligned_bam_path VARCHAR(500),
    vcf_file_path VARCHAR(500),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (sample_id) REFERENCES os_bharat_samples(sample_id) ON DELETE SET NULL,
    INDEX idx_participant_genomics (participant_id, sequencing_date),
    INDEX idx_platform (platform),
    INDEX idx_sequencing_type (sequencing_type)
);

-- Epigenetics data
CREATE TABLE IF NOT EXISTS os_bharat_epigenetics (
    epigenetics_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    sample_id BIGINT,
    analysis_date DATE NOT NULL,
    assay_type VARCHAR(50),                          -- METHYLATION, CHIP_SEQ, ATAC_SEQ, etc.
    platform VARCHAR(50),                           -- ILLUMINA_450K, EPIC, etc.
    
    -- Methylation data
    mean_methylation DECIMAL(5,4),
    methylation_age DECIMAL(5,2),                   -- Epigenetic age
    age_acceleration DECIMAL(5,2),                  -- Difference from chronological age
    
    -- Clock estimates
    horvath_age DECIMAL(5,2),
    hannum_age DECIMAL(5,2),
    phenoage DECIMAL(5,2),
    grimage DECIMAL(5,2),
    
    -- Pathway analysis
    pathway_enrichment JSON,
    go_terms JSON,
    
    -- File paths
    raw_data_path VARCHAR(500),
    processed_data_path VARCHAR(500),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (sample_id) REFERENCES os_bharat_samples(sample_id) ON DELETE SET NULL,
    INDEX idx_participant_epigenetics (participant_id, analysis_date),
    INDEX idx_assay_type (assay_type),
    INDEX idx_methylation_age (methylation_age)
);

-- Proteomics data
CREATE TABLE IF NOT EXISTS os_bharat_proteomics (
    proteomics_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    sample_id BIGINT,
    analysis_date DATE NOT NULL,
    platform VARCHAR(50),                           -- MASS_SPEC, LUMINEX, etc.
    protocol VARCHAR(100),                          -- SOMALOGIC, OLINK, etc.
    
    -- Protein quantification
    total_proteins_detected INT,
    protein_concentrations JSON,                    -- Protein ID -> concentration
    
    -- Pathway analysis
    pathway_analysis JSON,
    protein_networks JSON,
    
    -- Inflammatory markers
    inflammatory_score DECIMAL(5,2),
    aging_score DECIMAL(5,2),
    
    -- File paths
    raw_data_path VARCHAR(500),
    processed_data_path VARCHAR(500),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    FOREIGN KEY (sample_id) REFERENCES os_bharat_samples(sample_id) ON DELETE SET NULL,
    INDEX idx_participant_proteomics (participant_id, analysis_date),
    INDEX idx_platform (platform),
    INDEX idx_analysis_date (analysis_date)
);

-- ============================================================================
-- DATA QUALITY AND AUDIT
-- ============================================================================

-- Data quality tracking
CREATE TABLE IF NOT EXISTS os_bharat_data_quality (
    quality_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    data_type VARCHAR(50) NOT NULL,                 -- CLINICAL, BLOODWORK, OMICS, etc.
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NOT NULL,
    
    -- Quality metrics
    completeness_score DECIMAL(5,2),               -- % of required fields populated
    accuracy_score DECIMAL(5,2),                   -- Data validation score
    consistency_score DECIMAL(5,2),                -- Cross-reference consistency
    
    -- Issue tracking
    missing_fields JSON,                           -- List of missing required fields
    validation_errors JSON,                        -- Validation failures
    consistency_issues JSON,                       -- Cross-reference problems
    
    -- Resolution tracking
    quality_status ENUM('GOOD', 'ACCEPTABLE', 'POOR', 'NEEDS_REVIEW') DEFAULT 'GOOD',
    reviewed_by VARCHAR(100),
    reviewed_at TIMESTAMP NULL,
    resolution_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    INDEX idx_participant_quality (participant_id, data_type),
    INDEX idx_quality_status (quality_status),
    INDEX idx_table_record (table_name, record_id)
);

-- Audit trail for all data modifications
CREATE TABLE IF NOT EXISTS os_bharat_audit_trail (
    audit_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    participant_id BIGINT NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NOT NULL,
    action_type ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    
    -- Change details
    field_name VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    
    -- Metadata
    changed_by VARCHAR(100) NOT NULL,
    change_reason TEXT,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (participant_id) REFERENCES os_bharat_participants(participant_id) ON DELETE CASCADE,
    INDEX idx_participant_audit (participant_id, change_timestamp),
    INDEX idx_table_record_audit (table_name, record_id),
    INDEX idx_action_type (action_type),
    INDEX idx_changed_by (changed_by)
);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Comprehensive participant overview
CREATE VIEW v_bharat_participant_summary AS
SELECT 
    p.participant_id,
    p.bharat_code,
    p.center_code,
    p.age_group,
    p.gender,
    p.study_status,
    p.registration_date,
    
    -- Data completeness
    COUNT(DISTINCT cd.clinical_id) as clinical_assessments,
    COUNT(DISTINCT bw.bloodwork_id) as bloodwork_results,
    COUNT(DISTINCT fc.flow_id) as flow_cytometry_analyses,
    COUNT(DISTINCT g.genomics_id) as genomics_datasets,
    COUNT(DISTINCT e.epigenetics_id) as epigenetics_datasets,
    COUNT(DISTINCT pr.proteomics_id) as proteomics_datasets,
    
    -- Sample counts
    COUNT(DISTINCT s.sample_id) as total_samples,
    COUNT(DISTINCT CASE WHEN s.sample_type = 'BLOOD' THEN s.sample_id END) as blood_samples,
    COUNT(DISTINCT CASE WHEN s.sample_type = 'URINE' THEN s.sample_id END) as urine_samples,
    
    -- Latest data timestamps
    MAX(cd.assessment_date) as latest_clinical_assessment,
    MAX(bw.test_date) as latest_bloodwork,
    MAX(fc.analysis_date) as latest_flow_cytometry,
    MAX(g.sequencing_date) as latest_genomics,
    MAX(e.analysis_date) as latest_epigenetics,
    MAX(pr.analysis_date) as latest_proteomics

FROM os_bharat_participants p
LEFT JOIN os_bharat_clinical_data cd ON p.participant_id = cd.participant_id
LEFT JOIN os_bharat_bloodwork bw ON p.participant_id = bw.participant_id
LEFT JOIN os_bharat_flow_cytometry fc ON p.participant_id = fc.participant_id
LEFT JOIN os_bharat_genomics g ON p.participant_id = g.participant_id
LEFT JOIN os_bharat_epigenetics e ON p.participant_id = e.participant_id
LEFT JOIN os_bharat_proteomics pr ON p.participant_id = pr.participant_id
LEFT JOIN os_bharat_samples s ON p.participant_id = s.participant_id

GROUP BY p.participant_id;

-- ============================================================================
-- TRIGGERS FOR DATA INTEGRITY
-- ============================================================================

-- Ensure participant codes follow the correct format
DELIMITER //
CREATE TRIGGER tr_validate_bharat_code 
BEFORE INSERT ON os_bharat_participants
FOR EACH ROW
BEGIN
    IF NEW.bharat_code NOT REGEXP '^[A-Z]{3}-[1-5][AB]-[0-9]{3}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid BHARAT code format. Must be XXX-#X-### where XXX=center, #=age group, X=gender, ###=sequential';
    END IF;
END//
DELIMITER ;

-- Automatically update data quality scores when data is inserted/updated
DELIMITER //
CREATE TRIGGER tr_update_data_quality_clinical
AFTER INSERT ON os_bharat_clinical_data
FOR EACH ROW
BEGIN
    INSERT INTO os_bharat_data_quality (participant_id, data_type, table_name, record_id, completeness_score)
    VALUES (NEW.participant_id, 'CLINICAL', 'os_bharat_clinical_data', NEW.clinical_id, 
            (CASE WHEN NEW.pulse_rate IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.blood_pressure_systolic IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.blood_pressure_diastolic IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.respiratory_rate IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.oxygen_saturation IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.temperature_celsius IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.height_cm IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.weight_kg IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.medical_history IS NOT NULL THEN 10 ELSE 0 END +
             CASE WHEN NEW.lifestyle_factors IS NOT NULL THEN 10 ELSE 0 END) / 10.0);
END//
DELIMITER ;

-- ============================================================================
-- INITIAL DATA SETUP
-- ============================================================================

-- Insert initial center codes
INSERT IGNORE INTO os_bharat_participants (participant_id, bharat_code, center_code, age_group, gender, sequential_number) 
VALUES 
(0, 'SYSTEM', 'SYS', 0, 'X', 0)
ON DUPLICATE KEY UPDATE participant_id = participant_id;

-- ============================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Additional composite indexes for common query patterns
CREATE INDEX idx_participant_data_type ON os_bharat_data_integrations (participant_id, data_type, imported_at);
CREATE INDEX idx_clinical_assessment_date ON os_bharat_clinical_data (participant_id, assessment_date DESC);
CREATE INDEX idx_bloodwork_test_date ON os_bharat_bloodwork (participant_id, test_date DESC);
CREATE INDEX idx_omics_analysis_date ON os_bharat_genomics (participant_id, sequencing_date DESC);
CREATE INDEX idx_sample_collection_date ON os_bharat_samples (participant_id, collection_date DESC);

-- Full-text search indexes for research queries
CREATE FULLTEXT INDEX idx_clinical_history ON os_bharat_clinical_data (medical_history);
CREATE FULLTEXT INDEX idx_audit_reason ON os_bharat_audit_trail (change_reason);

-- ============================================================================
-- COMMENTS AND DOCUMENTATION
-- ============================================================================

-- Table comments for documentation
ALTER TABLE os_bharat_participants COMMENT = 'Master participant registry with unique BHARAT study identifiers';
ALTER TABLE os_bharat_data_integrations COMMENT = 'Tracks all external data imports with full audit trail';
ALTER TABLE os_bharat_clinical_data COMMENT = 'Clinical metadata and assessments from Epicollect and other sources';
ALTER TABLE os_bharat_bloodwork COMMENT = 'Laboratory blood test results from multiple providers';
ALTER TABLE os_bharat_flow_cytometry COMMENT = 'Flow cytometry analysis results for immune profiling';
ALTER TABLE os_bharat_genomics COMMENT = 'Genomic sequencing data and variant calling results';
ALTER TABLE os_bharat_epigenetics COMMENT = 'Epigenetic analysis including methylation and aging clocks';
ALTER TABLE os_bharat_proteomics COMMENT = 'Protein expression and quantification data';
ALTER TABLE os_bharat_samples COMMENT = 'Sample collection and tracking with full chain of custody';
ALTER TABLE os_bharat_data_quality COMMENT = 'Data quality metrics and validation results';
ALTER TABLE os_bharat_audit_trail COMMENT = 'Complete audit trail of all data modifications';

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================