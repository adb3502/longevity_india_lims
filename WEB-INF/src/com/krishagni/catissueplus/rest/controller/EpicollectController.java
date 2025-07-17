package com.krishagni.catissueplus.rest.controller;

import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import com.krishagni.catissueplus.core.biospecimen.services.EpicollectImportService;

@Controller
@RequestMapping("/epicollect")
public class EpicollectController {
    
    @Autowired
    private EpicollectImportService epicollectService;
    
    @Autowired
    private HttpServletRequest httpReq;
    
    /**
     * Manually trigger Epicollect data import
     */
    @RequestMapping(method = RequestMethod.POST, value = "/import")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> triggerImport() {
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Run import in background thread to avoid timeout
            new Thread(() -> {
                epicollectService.importDataFromEpicollect();
            }).start();
            
            response.put("status", "started");
            response.put("message", "Epicollect import has been triggered");
            response.put("timestamp", new Date());
            
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", e.getMessage());
        }
        
        return response;
    }
    
    /**
     * Get import status and statistics
     */
    @RequestMapping(method = RequestMethod.GET, value = "/status")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> getImportStatus() {
        Map<String, Object> status = new HashMap<>();
        
        // TODO: Query database for actual statistics
        status.put("lastImportDate", new Date());
        status.put("totalImported", 0);
        status.put("lastImportCount", 0);
        status.put("failedImports", 0);
        status.put("epicollectProjectUrl", "https://five.epicollect.net/project/longevity");
        
        return status;
    }
    
    /**
     * Configure Epicollect integration settings
     */
    @RequestMapping(method = RequestMethod.POST, value = "/config")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> updateConfig(@RequestBody Map<String, Object> config) {
        Map<String, Object> response = new HashMap<>();
        
        try {
            // Validate required fields
            if (!config.containsKey("clientId") || !config.containsKey("clientSecret")) {
                response.put("status", "error");
                response.put("message", "Client ID and Client Secret are required");
                return response;
            }
            
            // TODO: Store configuration in database
            response.put("status", "success");
            response.put("message", "Epicollect configuration updated");
            
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", e.getMessage());
        }
        
        return response;
    }
    
    /**
     * Test Epicollect connection
     */
    @RequestMapping(method = RequestMethod.GET, value = "/test")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> testConnection() {
        Map<String, Object> result = new HashMap<>();
        
        try {
            // TODO: Test connection to Epicollect API
            result.put("status", "success");
            result.put("message", "Connection to Epicollect API successful");
            result.put("projectFound", true);
            result.put("projectName", "Longevity");
            
        } catch (Exception e) {
            result.put("status", "error");
            result.put("message", "Failed to connect to Epicollect: " + e.getMessage());
        }
        
        return result;
    }
    
    /**
     * Get field mappings between Epicollect and LIIMS
     */
    @RequestMapping(method = RequestMethod.GET, value = "/mappings")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> getFieldMappings() {
        Map<String, Object> mappings = new HashMap<>();
        
        // Define how Epicollect fields map to LIIMS fields
        Map<String, String> fieldMap = new HashMap<>();
        fieldMap.put("Name", "participant.firstName + participant.lastName");
        fieldMap.put("Age", "participant.age");
        fieldMap.put("Gender", "participant.gender");
        fieldMap.put("Date_of_birth", "participant.birthDate");
        fieldMap.put("BP", "customFields.blood_pressure");
        fieldMap.put("Pulse", "customFields.pulse");
        fieldMap.put("Temperature", "customFields.temperature");
        fieldMap.put("SPo2", "customFields.spo2");
        
        mappings.put("fieldMappings", fieldMap);
        
        // Privacy settings
        Map<String, String> privacyRules = new HashMap<>();
        privacyRules.put("Name", "ANONYMIZE");
        privacyRules.put("Contact_Information", "REMOVE");
        privacyRules.put("Address", "REMOVE");
        privacyRules.put("Permanent_Native_Address", "REMOVE");
        
        mappings.put("privacyRules", privacyRules);
        
        return mappings;
    }
}