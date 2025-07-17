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
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import com.krishagni.catissueplus.core.biospecimen.events.CollectionProtocolRegistrationDetail;
import com.krishagni.catissueplus.core.biospecimen.events.ParticipantDetail;
import com.krishagni.catissueplus.core.biospecimen.services.CollectionProtocolRegistrationService;
import com.krishagni.catissueplus.core.common.events.RequestEvent;
import com.krishagni.catissueplus.core.common.events.ResponseEvent;

@Controller
@RequestMapping("/bharat")
public class BharatParticipantController {
    
    @Autowired
    private CollectionProtocolRegistrationService cprService;
    
    @Autowired
    private HttpServletRequest httpReq;
    
    /**
     * Enroll a new participant in the BHARAT study
     */
    @RequestMapping(method = RequestMethod.POST, value = "/participants/enroll")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> enrollParticipant(@RequestBody Map<String, Object> enrollmentData) {
        try {
            // Extract enrollment data
            String centerCode = (String) enrollmentData.get("centerCode");
            Integer age = (Integer) enrollmentData.get("age");
            String gender = (String) enrollmentData.get("gender");
            Long cpId = ((Number) enrollmentData.get("cpId")).longValue();
            
            // Determine age group based on age
            Integer ageGroup = getAgeGroup(age);
            
            // Convert gender to BHARAT format (M/F to A/B)
            String bharatGender = "M".equals(gender) ? "A" : "B";
            
            // Get next sequential number for this center/age/gender combination
            Integer sequentialNumber = getNextSequentialNumber(centerCode, ageGroup, bharatGender);
            
            // Generate participant code
            String participantCode = String.format("%s-%d%s-%03d", 
                centerCode, ageGroup, bharatGender, sequentialNumber);
            
            // Create participant detail
            ParticipantDetail participant = new ParticipantDetail();
            
            // Set demographic details
            if (enrollmentData.containsKey("firstName")) {
                participant.setFirstName((String) enrollmentData.get("firstName"));
            }
            if (enrollmentData.containsKey("lastName")) {
                participant.setLastName((String) enrollmentData.get("lastName"));
            }
            if (enrollmentData.containsKey("birthDate")) {
                // TODO: Parse birth date from string
                // participant.setBirthDate(parsedDate);
            }
            participant.setGender(gender);
            
            // Create CPR registration
            CollectionProtocolRegistrationDetail cpr = new CollectionProtocolRegistrationDetail();
            cpr.setCpId(cpId);
            cpr.setPpid(participantCode);
            cpr.setRegistrationDate(new Date());
            cpr.setParticipant(participant);
            
            // Create participant through service
            RequestEvent<CollectionProtocolRegistrationDetail> req = new RequestEvent<>(cpr);
            ResponseEvent<CollectionProtocolRegistrationDetail> resp = cprService.createRegistration(req);
            
            if (!resp.isSuccessful()) {
                return Collections.singletonMap("error", resp.getError().getMessage());
            }
            
            CollectionProtocolRegistrationDetail created = resp.getPayload();
            
            // TODO: Create BHARAT participant record in custom table
            
            // Update enrollment statistics
            updateEnrollmentStats(centerCode, ageGroup, bharatGender, 1);
            
            // Return success response
            Map<String, Object> result = new HashMap<>();
            result.put("cprId", created.getId());
            result.put("participantId", created.getParticipant().getId());
            result.put("participantCode", participantCode);
            result.put("centerCode", centerCode);
            result.put("ageGroup", ageGroup);
            result.put("gender", bharatGender);
            result.put("sequentialNumber", sequentialNumber);
            result.put("visualCoding", getVisualCoding(ageGroup, bharatGender));
            
            return result;
            
        } catch (Exception e) {
            Map<String, Object> error = new HashMap<>();
            error.put("error", e.getMessage());
            return error;
        }
    }
    
    /**
     * Get participant by BHARAT code
     */
    @RequestMapping(method = RequestMethod.GET, value = "/participants/{code}")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> getParticipantByCode(@PathVariable("code") String code) {
        // TODO: Implement participant lookup by BHARAT code
        Map<String, Object> result = new HashMap<>();
        result.put("code", code);
        result.put("message", "To be implemented");
        return result;
    }
    
    /**
     * Get participant timeline
     */
    @RequestMapping(method = RequestMethod.GET, value = "/participants/{code}/timeline")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public List<Map<String, Object>> getParticipantTimeline(@PathVariable("code") String code) {
        // TODO: Implement timeline retrieval
        return Collections.emptyList();
    }
    
    /**
     * Get enrollment statistics
     */
    @RequestMapping(method = RequestMethod.GET, value = "/stats/enrollment")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> getEnrollmentStats(
            @RequestParam(value = "center", required = false) String center) {
        
        Map<String, Object> stats = new HashMap<>();
        stats.put("total", 1247); // TODO: Get from database
        
        Map<String, Integer> byCenter = new HashMap<>();
        byCenter.put("RAM", 450);
        byCenter.put("VEL", 397);
        byCenter.put("PGI", 400);
        stats.put("byCenter", byCenter);
        
        Map<String, Map<String, Object>> byAgeGroup = new HashMap<>();
        for (int i = 1; i <= 5; i++) {
            Map<String, Object> ageGroupStats = new HashMap<>();
            ageGroupStats.put("target", 1000);
            ageGroupStats.put("current", 200 + (i * 50)); // Dummy data
            ageGroupStats.put("male", 100 + (i * 25));
            ageGroupStats.put("female", 100 + (i * 25));
            
            String ageRange = getAgeRange(i);
            byAgeGroup.put(ageRange, ageGroupStats);
        }
        stats.put("byAgeGroup", byAgeGroup);
        
        Map<String, Integer> byGender = new HashMap<>();
        byGender.put("M", 623);
        byGender.put("F", 624);
        stats.put("byGender", byGender);
        
        return stats;
    }
    
    /**
     * Get sample inventory statistics
     */
    @RequestMapping(method = RequestMethod.GET, value = "/stats/inventory")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> getInventoryStats() {
        Map<String, Object> stats = new HashMap<>();
        
        Map<String, Integer> byType = new HashMap<>();
        byType.put("Blood EDTA", 1247);
        byType.put("Blood SST", 1247);
        byType.put("Serum Aliquots", 3741);
        byType.put("Plasma Aliquots", 2494);
        byType.put("Urine", 1198);
        byType.put("Hair", 1156);
        byType.put("Cheek Swab", 1247);
        byType.put("Stool", 432);
        stats.put("byType", byType);
        
        Map<String, String> byStorage = new HashMap<>();
        byStorage.put("-80C Freezer 1", "67%");
        byStorage.put("-80C Freezer 2", "45%");
        byStorage.put("LN2 Tank 1", "78%");
        stats.put("byStorage", byStorage);
        
        stats.put("pendingProcessing", 47);
        stats.put("qcFailed", 12);
        
        return stats;
    }
    
    /**
     * Get data completeness statistics
     */
    @RequestMapping(method = RequestMethod.GET, value = "/stats/completeness")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public Map<String, Object> getDataCompletenessStats() {
        Map<String, Object> stats = new HashMap<>();
        
        stats.put("overall", 0.82);
        
        Map<String, String> byDataType = new HashMap<>();
        byDataType.put("Clinical Metadata", "98%");
        byDataType.put("Blood Results", "89%");
        byDataType.put("Immunophenotyping", "72%");
        byDataType.put("Genomics", "0%");
        byDataType.put("Proteomics", "0%");
        stats.put("byDataType", byDataType);
        
        return stats;
    }
    
    // Helper methods
    
    private Integer getAgeGroup(Integer age) {
        if (age >= 18 && age <= 29) return 1;
        if (age >= 30 && age <= 44) return 2;
        if (age >= 45 && age <= 59) return 3;
        if (age >= 60 && age <= 74) return 4;
        if (age >= 75) return 5;
        throw new IllegalArgumentException("Age must be 18 or above");
    }
    
    private String getAgeRange(Integer ageGroup) {
        switch (ageGroup) {
            case 1: return "18-29";
            case 2: return "30-44";
            case 3: return "45-59";
            case 4: return "60-74";
            case 5: return "75+";
            default: return "Unknown";
        }
    }
    
    private Integer getNextSequentialNumber(String centerCode, Integer ageGroup, String gender) {
        // TODO: Implement database query to get next sequential number
        // For now, return a dummy value
        return 1;
    }
    
    private void updateEnrollmentStats(String centerCode, Integer ageGroup, String gender, int increment) {
        // TODO: Implement database update for enrollment statistics
    }
    
    private Map<String, String> getVisualCoding(Integer ageGroup, String gender) {
        Map<String, String> coding = new HashMap<>();
        
        // Cryocap colors by age group
        String cryocapColor;
        switch (ageGroup) {
            case 1: cryocapColor = "Blue"; break;
            case 2: cryocapColor = "Green"; break;
            case 3: cryocapColor = "Yellow"; break;
            case 4: cryocapColor = "Orange"; break;
            case 5: cryocapColor = "Red"; break;
            default: cryocapColor = "Unknown";
        }
        coding.put("cryocapColor", cryocapColor);
        
        // Label border colors by gender
        String labelBorderColor = "A".equals(gender) ? "Blue" : "Pink";
        coding.put("labelBorderColor", labelBorderColor);
        
        return coding;
    }
}