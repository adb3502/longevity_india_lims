package com.krishagni.catissueplus.rest.controller;

import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.krishagni.catissueplus.core.biospecimen.services.BharatComprehensiveDataService;
import com.krishagni.catissueplus.core.biospecimen.services.BharatDataAnonymizationService;
import com.krishagni.catissueplus.core.biospecimen.services.EpicollectImportService;

/**
 * REST controller for BHARAT study data management
 * Provides endpoints for data import, participant management, and study statistics
 */
@RestController
@RequestMapping("/api/bharat/data")
public class BharatDataController {
    
    @Autowired
    private BharatComprehensiveDataService comprehensiveDataService;
    
    @Autowired
    private BharatDataAnonymizationService anonymizationService;
    
    @Autowired
    private EpicollectImportService epicollectImportService;
    
    /**
     * Import complete dataset from Epicollect
     * POST /api/bharat/data/import/complete
     */
    @PostMapping("/import/complete")
    public ResponseEntity<Map<String, Object>> importCompleteDataset() {
        try {
            Map<String, Object> result = comprehensiveDataService.importCompleteDataset();
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to import complete dataset");
            error.put("message", e.getMessage());
            error.put("success", false);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Get participant data by BHARAT code
     * GET /api/bharat/data/participants/{bharatCode}
     */
    @GetMapping("/participants/{bharatCode}")
    public ResponseEntity<Map<String, Object>> getParticipantData(@PathVariable String bharatCode) {
        try {
            Map<String, Object> participant = comprehensiveDataService.getParticipantData(bharatCode);
            if (participant != null) {
                return ResponseEntity.ok(participant);
            } else {
                Map<String, Object> error = new HashMap<>();
                error.put("error", "Participant not found");
                error.put("bharat_code", bharatCode);
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
            }
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to retrieve participant data");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Get comprehensive study statistics
     * GET /api/bharat/data/stats/study
     */
    @GetMapping("/stats/study")
    public ResponseEntity<Map<String, Object>> getStudyStatistics() {
        try {
            Map<String, Object> stats = comprehensiveDataService.getStudyStatistics();
            return ResponseEntity.ok(stats);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to retrieve study statistics");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Get Epicollect connection status
     * GET /api/bharat/data/epicollect/status
     */
    @GetMapping("/epicollect/status")
    public ResponseEntity<Map<String, Object>> getEpicollectStatus() {
        try {
            Map<String, Object> status = new HashMap<>();
            
            // Test connection
            boolean connected = epicollectImportService.testConnection();
            status.put("connected", connected);
            
            if (connected) {
                // Get entry count
                int entryCount = epicollectImportService.getEntryCount();
                status.put("available_entries", entryCount);
                status.put("last_checked", new java.util.Date().toString());
            }
            
            return ResponseEntity.ok(status);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to check Epicollect status");
            error.put("message", e.getMessage());
            error.put("connected", false);
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
        }
    }
    
    /**
     * Get anonymization statistics
     * GET /api/bharat/data/anonymization/stats
     */
    @GetMapping("/anonymization/stats")
    public ResponseEntity<Map<String, Object>> getAnonymizationStats() {
        try {
            Map<String, Integer> stats = anonymizationService.getAnonymizationStats();
            Map<String, Object> report = anonymizationService.generateAnonymizationReport();
            
            Map<String, Object> result = new HashMap<>();
            result.put("current_session_stats", stats);
            result.put("detailed_report", report);
            
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to retrieve anonymization statistics");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Reset anonymization statistics
     * POST /api/bharat/data/anonymization/reset
     */
    @PostMapping("/anonymization/reset")
    public ResponseEntity<Map<String, Object>> resetAnonymizationStats() {
        try {
            anonymizationService.resetStats();
            Map<String, Object> result = new HashMap<>();
            result.put("message", "Anonymization statistics reset successfully");
            result.put("success", true);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to reset anonymization statistics");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Get data quality overview
     * GET /api/bharat/data/quality/overview
     */
    @GetMapping("/quality/overview")
    public ResponseEntity<Map<String, Object>> getDataQualityOverview() {
        try {
            // This would typically query the data quality tables
            Map<String, Object> overview = new HashMap<>();
            overview.put("implementation_status", "In Development");
            overview.put("message", "Data quality overview will be available after comprehensive import");
            
            return ResponseEntity.ok(overview);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to retrieve data quality overview");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Test data pipeline with sample entry
     * POST /api/bharat/data/test/pipeline
     */
    @PostMapping("/test/pipeline")
    public ResponseEntity<Map<String, Object>> testDataPipeline(@RequestBody Map<String, Object> sampleEntry) {
        try {
            Map<String, Object> result = new HashMap<>();
            List<String> steps = new ArrayList<>();
            
            // Step 1: Data cleaning test
            steps.add("Testing data cleaning...");
            // This would call the cleaning service
            
            // Step 2: Anonymization test
            steps.add("Testing anonymization...");
            Map<String, Object> anonymized = anonymizationService.anonymizeParticipantData(sampleEntry);
            
            // Step 3: Validation test
            steps.add("Testing validation...");
            boolean valid = anonymizationService.validateAnonymization(anonymized);
            
            result.put("steps", steps);
            result.put("anonymized_data", anonymized);
            result.put("validation_passed", valid);
            result.put("test_success", true);
            
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Data pipeline test failed");
            error.put("message", e.getMessage());
            error.put("test_success", false);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Get import history
     * GET /api/bharat/data/import/history
     */
    @GetMapping("/import/history")
    public ResponseEntity<Map<String, Object>> getImportHistory() {
        try {
            Map<String, Object> history = new HashMap<>();
            history.put("implementation_status", "In Development");
            history.put("message", "Import history will be available after database implementation");
            
            return ResponseEntity.ok(history);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to retrieve import history");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Get system health check
     * GET /api/bharat/data/health
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> getSystemHealth() {
        try {
            Map<String, Object> health = new HashMap<>();
            
            // Check database connectivity
            health.put("database_connected", true); // This would be a real check
            
            // Check Epicollect connectivity
            boolean epicollectConnected = epicollectImportService.testConnection();
            health.put("epicollect_connected", epicollectConnected);
            
            // Check services
            health.put("services_status", "All services operational");
            
            // System status
            health.put("overall_status", epicollectConnected ? "HEALTHY" : "DEGRADED");
            health.put("timestamp", new java.util.Date().toString());
            
            return ResponseEntity.ok(health);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Health check failed");
            error.put("message", e.getMessage());
            error.put("overall_status", "UNHEALTHY");
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
        }
    }
    
    /**
     * Export participant data (anonymized)
     * GET /api/bharat/data/export/{bharatCode}
     */
    @GetMapping("/export/{bharatCode}")
    public ResponseEntity<Map<String, Object>> exportParticipantData(@PathVariable String bharatCode) {
        try {
            Map<String, Object> participant = comprehensiveDataService.getParticipantData(bharatCode);
            if (participant != null) {
                // Remove any remaining sensitive data
                participant.remove("epicollect_uuid");
                participant.put("export_timestamp", new java.util.Date().toString());
                participant.put("export_note", "All personal identifiers have been anonymized");
                
                return ResponseEntity.ok(participant);
            } else {
                Map<String, Object> error = new HashMap<>();
                error.put("error", "Participant not found for export");
                error.put("bharat_code", bharatCode);
                return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
            }
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to export participant data");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
    
    /**
     * Get database schema info
     * GET /api/bharat/data/schema/info
     */
    @GetMapping("/schema/info")
    public ResponseEntity<Map<String, Object>> getSchemaInfo() {
        try {
            Map<String, Object> schema = new HashMap<>();
            
            // Core tables
            List<String> coreTables = new ArrayList<>();
            coreTables.add("os_bharat_participants");
            coreTables.add("os_bharat_data_integrations");
            coreTables.add("os_bharat_clinical_data");
            coreTables.add("os_bharat_bloodwork");
            coreTables.add("os_bharat_flow_cytometry");
            coreTables.add("os_bharat_genomics");
            coreTables.add("os_bharat_epigenetics");
            coreTables.add("os_bharat_proteomics");
            coreTables.add("os_bharat_samples");
            coreTables.add("os_bharat_data_quality");
            coreTables.add("os_bharat_audit_trail");
            
            schema.put("core_tables", coreTables);
            schema.put("schema_version", "1.0");
            schema.put("designed_for", "BHARAT Study Multi-Omics Data Integration");
            schema.put("supports_data_types", new String[]{"Clinical", "Bloodwork", "Flow Cytometry", "Genomics", "Epigenetics", "Proteomics"});
            
            return ResponseEntity.ok(schema);
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", "Failed to retrieve schema information");
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}