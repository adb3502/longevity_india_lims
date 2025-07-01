-- BHARAT Study Dashboard Queries
-- Generated on 2025-06-24 17:16:05

-- ENROLLMENT_SUMMARY

                SELECT 
                    CASE 
                        WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 20 AND 30 THEN 'AG1'
                        WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 31 AND 40 THEN 'AG2'
                        WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 41 AND 50 THEN 'AG3'
                        WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 51 AND 60 THEN 'AG4'
                        WHEN EXTRACT(YEAR FROM AGE(birth_date)) BETWEEN 61 AND 70 THEN 'AG5'
                    END as age_group,
                    COUNT(*) as enrolled_count,
                    126 as target_count,
                    ROUND((COUNT(*) * 100.0 / 126), 1) as completion_percentage
                FROM catissue_participant p
                JOIN catissue_coll_prot_reg cpr ON p.identifier = cpr.participant_id
                JOIN catissue_collection_protocol cp ON cpr.collection_protocol_id = cp.identifier
                WHERE cp.short_title = 'BHARAT-STUDY'
                AND p.activity_status = 'Active'
                GROUP BY age_group
                ORDER BY age_group
            

-- VISIT_COMPLETION_STATUS

                SELECT 
                    cpe.clinical_diagnosis as visit_name,
                    COUNT(DISTINCT cpr.identifier) as completed_participants,
                    (SELECT COUNT(*) FROM catissue_coll_prot_reg WHERE collection_protocol_id = cp.identifier) as total_participants,
                    ROUND((COUNT(DISTINCT cpr.identifier) * 100.0 / 
                           (SELECT COUNT(*) FROM catissue_coll_prot_reg WHERE collection_protocol_id = cp.identifier)), 1) as completion_rate
                FROM catissue_collection_protocol cp
                JOIN catissue_coll_prot_event cpe ON cp.identifier = cpe.collection_protocol_id
                JOIN catissue_specimen_coll_group scg ON cpe.identifier = scg.collection_protocol_event_id
                JOIN catissue_coll_prot_reg cpr ON scg.collection_protocol_reg_id = cpr.identifier
                WHERE cp.short_title = 'BHARAT-STUDY'
                AND scg.activity_status = 'Active'
                GROUP BY cpe.clinical_diagnosis, cp.identifier
                ORDER BY 
                    CASE cpe.clinical_diagnosis 
                        WHEN 'V0' THEN 1 
                        WHEN 'V1' THEN 2 
                        WHEN 'V2' THEN 3 
                        WHEN 'V3' THEN 4 
                    END
            

-- SAMPLE_COLLECTION_METRICS

                SELECT 
                    DATE(s.created_on) as collection_date,
                    s.specimen_type,
                    COUNT(*) as samples_collected,
                    SUM(CASE WHEN s.available_quantity > 0 THEN 1 ELSE 0 END) as samples_available,
                    AVG(s.available_quantity) as avg_quantity
                FROM catissue_specimen s
                JOIN catissue_specimen_coll_group scg ON s.specimen_collection_group_id = scg.identifier
                JOIN catissue_coll_prot_reg cpr ON scg.collection_protocol_reg_id = cpr.identifier
                JOIN catissue_collection_protocol cp ON cpr.collection_protocol_id = cp.identifier
                WHERE cp.short_title = 'BHARAT-STUDY'
                AND s.activity_status = 'Active'
                AND s.created_on >= CURRENT_DATE - INTERVAL '90 days'
                GROUP BY DATE(s.created_on), s.specimen_type
                ORDER BY collection_date DESC, s.specimen_type
            

-- BIOMARKER_SUMMARY

                SELECT 
                    fer.attribute_name as biomarker_name,
                    COUNT(*) as measurement_count,
                    AVG(CAST(fer.attribute_value AS DECIMAL)) as mean_value,
                    STDDEV(CAST(fer.attribute_value AS DECIMAL)) as std_value,
                    MIN(CAST(fer.attribute_value AS DECIMAL)) as min_value,
                    MAX(CAST(fer.attribute_value AS DECIMAL)) as max_value
                FROM catissue_form_record_entry fre
                JOIN catissue_form_context fc ON fre.form_ctxt_id = fc.identifier
                JOIN catissue_form_field_entry fer ON fre.record_id = fer.record_id
                JOIN catissue_collection_protocol cp ON fc.collection_protocol_id = cp.identifier
                WHERE cp.short_title = 'BHARAT-STUDY'
                AND fc.entity_type = 'SpecimenExtension'
                AND fer.attribute_name IN ('epigenetic_age', 'telomere_length', 'crp_level', 'il6_level', 'glucose_level')
                AND fer.attribute_value ~ '^[0-9]+\.?[0-9]*$'
                GROUP BY fer.attribute_name
                ORDER BY fer.attribute_name
            

-- QUALITY_CONTROL_METRICS

                SELECT 
                    DATE(fre.update_time) as analysis_date,
                    COUNT(*) as total_analyses,
                    SUM(CASE WHEN fer_qc.attribute_value = 'Pass' THEN 1 ELSE 0 END) as qc_pass,
                    SUM(CASE WHEN fer_qc.attribute_value = 'Fail' THEN 1 ELSE 0 END) as qc_fail,
                    AVG(CASE WHEN fer_conc.attribute_name = 'dna_yield' 
                             THEN CAST(fer_conc.attribute_value AS DECIMAL) END) as avg_dna_concentration,
                    AVG(CASE WHEN fer_purity.attribute_name = 'ratio260280' 
                             THEN CAST(fer_purity.attribute_value AS DECIMAL) END) as avg_260_280_ratio
                FROM catissue_form_record_entry fre
                JOIN catissue_form_context fc ON fre.form_ctxt_id = fc.identifier
                JOIN catissue_form_field_entry fer_qc ON fre.record_id = fer_qc.record_id AND fer_qc.attribute_name = 'qc_status'
                LEFT JOIN catissue_form_field_entry fer_conc ON fre.record_id = fer_conc.record_id AND fer_conc.attribute_name = 'dna_yield'
                LEFT JOIN catissue_form_field_entry fer_purity ON fre.record_id = fer_purity.record_id AND fer_purity.attribute_name = 'ratio260280'
                JOIN catissue_collection_protocol cp ON fc.collection_protocol_id = cp.identifier
                WHERE cp.short_title = 'BHARAT-STUDY'
                AND fc.entity_type = 'SpecimenExtension'
                AND fre.update_time >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(fre.update_time)
                ORDER BY analysis_date DESC
            

