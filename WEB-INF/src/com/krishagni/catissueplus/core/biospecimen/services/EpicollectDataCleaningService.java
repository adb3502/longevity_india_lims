package com.krishagni.catissueplus.core.biospecimen.services;

import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.stereotype.Service;

@Service
public class EpicollectDataCleaningService {
    
    private static final Log logger = LogFactory.getLog(EpicollectDataCleaningService.class);
    
    // Valid center codes - Updated with real active centers
    private static final Map<String, String> CENTER_MAPPINGS = new HashMap<>();
    static {
        // Ramaiah Memorial Hospital (Active)
        CENTER_MAPPINGS.put("ramaiah", "RAM");
        CENTER_MAPPINGS.put("ram", "RAM");
        CENTER_MAPPINGS.put("rmc", "RAM");
        CENTER_MAPPINGS.put("ms ramaiah", "RAM");
        CENTER_MAPPINGS.put("ramaiah memorial hospital", "RAM");
        
        // Sri Madhusudan Sai Institute of Medical Sciences and Research (Active)
        CENTER_MAPPINGS.put("smsimsr", "SSI");
        CENTER_MAPPINGS.put("sri madhusudan sai", "SSI");
        CENTER_MAPPINGS.put("satya sai", "SSI");
        CENTER_MAPPINGS.put("satyasai", "SSI");
        CENTER_MAPPINGS.put("ssi", "SSI");
        CENTER_MAPPINGS.put("sri sathya sai", "SSI");
        CENTER_MAPPINGS.put("chikkaballapur", "SSI");
        
        // Baptist Hospital (Future)
        CENTER_MAPPINGS.put("baptist", "BAP");
        CENTER_MAPPINGS.put("bap", "BAP");
        CENTER_MAPPINGS.put("baptist hospital", "BAP");
        
        // Bangalore Medical College (Future)
        CENTER_MAPPINGS.put("bangalore medical", "BMC");
        CENTER_MAPPINGS.put("bmc", "BMC");
        CENTER_MAPPINGS.put("bangalore medical college", "BMC");
        CENTER_MAPPINGS.put("bmcri", "BMC");
    }
    
    /**
     * Clean and standardize a single entry from Epicollect
     */
    public Map<String, Object> cleanEntry(Map<String, Object> rawEntry) {
        Map<String, Object> cleaned = new HashMap<>();
        
        // Extract and clean sample ID - this is the primary identifier
        String sampleId = cleanSampleId(rawEntry);
        if (StringUtils.isBlank(sampleId)) {
            logger.warn("Entry missing sample ID, skipping: " + rawEntry);
            return null;
        }
        cleaned.put("sampleId", sampleId);
        
        // Extract age group and gender from the new format sample ID
        String[] parts = sampleId.split("-");
        if (parts.length == 3) {
            String ageGenderCode = parts[1]; // e.g., "2A" or "5B"
            if (ageGenderCode.length() == 2) {
                cleaned.put("ageGroup", Integer.parseInt(ageGenderCode.substring(0, 1)));
                cleaned.put("gender", ageGenderCode.substring(1, 2));
            }
        }
        
        // Clean personal information
        cleaned.putAll(cleanPersonalInfo(rawEntry));
        
        // Clean center information (now determined during sampleId cleaning)
        String center = determineCenterCode(rawEntry);
        cleaned.put("centerCode", center);
        
        // Clean clinical data
        cleaned.putAll(cleanClinicalData(rawEntry));
        
        // Clean timestamps
        cleaned.put("collectionDate", cleanDate(rawEntry.get("created_at")));
        cleaned.put("uploadDate", cleanDate(rawEntry.get("uploaded_at")));
        
        // Track data completeness
        cleaned.put("dataCompleteness", calculateDataCompleteness(cleaned));
        
        return cleaned;
    }
    
    /**
     * Clean sample ID - convert from old format to new format
     */
    private String cleanSampleId(Map<String, Object> entry) {
        // Try multiple field names for the sample ID
        String sampleId = getStringValue(entry, "84_ID_In_the_format_", "title", "sample_id", "sampleId", "Sample_ID");
        if (sampleId == null) {
            return null;
        }
        
        // Convert from old format to new format
        return convertOldToNewFormat(sampleId, entry);
    }
    
    /**
     * Convert old format (5B-003, 2a-013) to new format (RAM-5B-003, RAM-2A-013)
     */
    private String convertOldToNewFormat(String oldId, Map<String, Object> entry) {
        if (oldId == null) {
            return null;
        }
        
        // Clean the old ID
        oldId = oldId.replaceAll("\\s+", "").toUpperCase();
        
        // Extract center code from the entry
        String centerCode = determineCenterCode(entry);
        
        // Check if it's already in new format
        if (Pattern.matches("[A-Z]{3}-\\d[A-B]-\\d{3}", oldId)) {
            return oldId; // Already in new format
        }
        
        // Handle old format conversion (e.g., "5B-003" → "RAM-5B-003")
        if (Pattern.matches("\\d[A-B]-\\d{3}", oldId)) {
            return centerCode + "-" + oldId;
        }
        
        // Handle variations with different separators or formats
        if (Pattern.matches("\\d[A-B]\\d{3}", oldId)) {
            // Insert hyphen: "5B003" → "5B-003"
            String formatted = oldId.substring(0, 2) + "-" + oldId.substring(2);
            return centerCode + "-" + formatted;
        }
        
        logger.warn("Cannot convert old format to new format: " + oldId);
        return centerCode + "-" + oldId; // Best effort
    }
    
    /**
     * Determine center code from entry data
     */
    private String determineCenterCode(Map<String, Object> entry) {
        String centerName = getStringValue(entry, "86_Collection_Centre", "center", "collection_center");
        if (centerName != null) {
            String normalized = centerName.toLowerCase().trim();
            
            // Check for Ramaiah variations
            if (normalized.contains("ramaiah")) {
                return "RAM";
            }
            
            // Check for SMSIMSR/Satya Sai variations
            if (normalized.contains("smsimsr") || normalized.contains("sri madhusudan sai") || 
                normalized.contains("satya") || normalized.contains("sai") || 
                normalized.contains("chikkaballapur")) {
                return "SSI";
            }
            
            // Check for Baptist variations
            if (normalized.contains("baptist")) {
                return "BAP";
            }
            
            // Check for Bangalore Medical variations
            if (normalized.contains("bangalore medical") || normalized.contains("bmcri")) {
                return "BMC";
            }
        }
        
        // Default to RAM since most current data is from Ramaiah
        logger.warn("Cannot determine center code, defaulting to RAM for entry: " + entry);
        return "RAM";
    }
    
    /**
     * Helper method to get string value from entry using multiple possible field names
     */
    private String getStringValue(Map<String, Object> entry, String... fieldNames) {
        for (String fieldName : fieldNames) {
            Object value = entry.get(fieldName);
            if (value != null && !value.toString().trim().isEmpty()) {
                return value.toString().trim();
            }
        }
        return null;
    }
    
    /**
     * Try to fix common sample ID format issues
     */
    private String fixSampleIdFormat(String sampleId) {
        // Handle missing hyphens
        if (sampleId.matches("[A-Z]{3}\\d[A-B]\\d{3}")) {
            return sampleId.substring(0, 3) + "-" + sampleId.substring(3, 5) + "-" + sampleId.substring(5);
        }
        
        // Handle lowercase
        sampleId = sampleId.toUpperCase();
        
        // Handle common typos in gender (A/B)
        sampleId = sampleId.replace("1M", "1A").replace("1F", "1B");
        sampleId = sampleId.replace("2M", "2A").replace("2F", "2B");
        sampleId = sampleId.replace("3M", "3A").replace("3F", "3B");
        sampleId = sampleId.replace("4M", "4A").replace("4F", "4B");
        sampleId = sampleId.replace("5M", "5A").replace("5F", "5B");
        
        return sampleId;
    }
    
    /**
     * Clean personal information
     */
    private Map<String, Object> cleanPersonalInfo(Map<String, Object> entry) {
        Map<String, Object> info = new HashMap<>();
        
        // Age
        Integer age = cleanInteger(getStringValue(entry, "age", "Age", "age_years"));
        if (age != null && age >= 18 && age <= 120) {
            info.put("age", age);
            info.put("ageGroup", getAgeGroup(age));
        }
        
        // Gender
        String gender = cleanGender(getStringValue(entry, "gender", "Gender", "sex"));
        info.put("gender", gender);
        
        // Clean name but anonymize
        String name = getStringValue(entry, "name", "Name", "participant_name");
        if (StringUtils.isNotBlank(name)) {
            info.put("hasName", true);
            // Don't store actual name, just flag that it exists
        }
        
        return info;
    }
    
    /**
     * Clean center code
     */
    private String cleanCenterCode(Map<String, Object> entry) {
        String center = getStringValue(entry, "center", "Center", "hospital", "site");
        if (center == null) {
            // Try to extract from sample ID
            String sampleId = cleanSampleId(entry);
            if (sampleId != null && sampleId.length() >= 3) {
                return sampleId.substring(0, 3);
            }
            return "UNK"; // Unknown
        }
        
        // Normalize and map
        center = center.toLowerCase().trim();
        for (Map.Entry<String, String> mapping : CENTER_MAPPINGS.entrySet()) {
            if (center.contains(mapping.getKey())) {
                return mapping.getValue();
            }
        }
        
        logger.warn("Unknown center: " + center);
        return "UNK";
    }
    
    /**
     * Clean clinical data
     */
    private Map<String, Object> cleanClinicalData(Map<String, Object> entry) {
        Map<String, Object> clinical = new HashMap<>();
        
        // Blood pressure
        String bp = getStringValue(entry, "bp", "BP", "blood_pressure");
        if (bp != null) {
            bp = bp.replaceAll("\\s+", "");
            if (bp.matches("\\d{2,3}/\\d{2,3}")) {
                clinical.put("bloodPressure", bp);
            }
        }
        
        // Pulse
        Integer pulse = cleanInteger(getStringValue(entry, "pulse", "Pulse", "heart_rate"));
        if (pulse != null && pulse >= 40 && pulse <= 200) {
            clinical.put("pulse", pulse);
        }
        
        // Temperature
        Double temp = cleanDouble(getStringValue(entry, "temperature", "Temperature", "temp"));
        if (temp != null && temp >= 95.0 && temp <= 105.0) {
            clinical.put("temperature", temp);
        }
        
        // SpO2
        Integer spo2 = cleanInteger(getStringValue(entry, "spo2", "SpO2", "oxygen"));
        if (spo2 != null && spo2 >= 70 && spo2 <= 100) {
            clinical.put("spo2", spo2);
        }
        
        // Check for blood work status
        Boolean hasBloodWork = checkDataExists(entry, "blood_results", "lab_results", "blood_work");
        clinical.put("hasBloodWork", hasBloodWork);
        
        // Check for omics data
        Boolean hasOmics = checkDataExists(entry, "omics", "genomics", "proteomics");
        clinical.put("hasOmicsData", hasOmics);
        
        return clinical;
    }
    
    
    // Removed duplicate method - using implementation below
    
    // Removed duplicate methods - using implementations below
    
    /**
     * Clean integer value
     */
    private Integer cleanInteger(String value) {
        if (value == null) return null;
        try {
            // Remove any non-digit characters
            value = value.replaceAll("[^0-9]", "");
            return Integer.parseInt(value);
        } catch (NumberFormatException e) {
            return null;
        }
    }
    
    /**
     * Clean double value
     */
    private Double cleanDouble(String value) {
        if (value == null) return null;
        try {
            // Remove any non-digit characters except decimal point
            value = value.replaceAll("[^0-9.]", "");
            return Double.parseDouble(value);
        } catch (NumberFormatException e) {
            return null;
        }
    }
    
    /**
     * Clean gender value
     */
    private String cleanGender(String gender) {
        if (gender == null) return "Unknown";
        
        gender = gender.toLowerCase().trim();
        if (gender.startsWith("m") || gender.equals("1")) {
            return "Male";
        } else if (gender.startsWith("f") || gender.equals("2")) {
            return "Female";
        } else if (gender.contains("other")) {
            return "Other";
        }
        
        return "Unknown";
    }
    
    /**
     * Clean date value
     */
    private String cleanDate(Object dateValue) {
        if (dateValue == null) return null;
        return dateValue.toString(); // ISO format from Epicollect
    }
    
    /**
     * Check if certain data exists
     */
    private Boolean checkDataExists(Map<String, Object> entry, String... keys) {
        for (String key : keys) {
            Object value = getStringValue(entry, key);
            if (value != null && !value.toString().equalsIgnoreCase("pending") 
                && !value.toString().equalsIgnoreCase("na")
                && !value.toString().equalsIgnoreCase("n/a")) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Calculate data completeness percentage
     */
    private Double calculateDataCompleteness(Map<String, Object> cleaned) {
        int totalFields = 10; // Total expected fields
        int completedFields = 0;
        
        if (cleaned.get("sampleId") != null) completedFields++;
        if (cleaned.get("age") != null) completedFields++;
        if (cleaned.get("gender") != null && !"Unknown".equals(cleaned.get("gender"))) completedFields++;
        if (cleaned.get("centerCode") != null && !"UNK".equals(cleaned.get("centerCode"))) completedFields++;
        if (cleaned.get("bloodPressure") != null) completedFields++;
        if (cleaned.get("pulse") != null) completedFields++;
        if (cleaned.get("temperature") != null) completedFields++;
        if (cleaned.get("spo2") != null) completedFields++;
        if (Boolean.TRUE.equals(cleaned.get("hasBloodWork"))) completedFields++;
        if (Boolean.TRUE.equals(cleaned.get("hasOmicsData"))) completedFields++;
        
        return (completedFields * 100.0) / totalFields;
    }
    
    /**
     * Get age group from age
     */
    private Integer getAgeGroup(Integer age) {
        if (age >= 18 && age <= 29) return 1;
        if (age >= 30 && age <= 44) return 2;
        if (age >= 45 && age <= 59) return 3;
        if (age >= 60 && age <= 74) return 4;
        if (age >= 75) return 5;
        return null;
    }
    
    /**
     * Detect and merge duplicate entries
     */
    public List<Map<String, Object>> deduplicateEntries(List<Map<String, Object>> entries) {
        Map<String, Map<String, Object>> deduplicated = new HashMap<>();
        
        for (Map<String, Object> entry : entries) {
            String sampleId = (String) entry.get("sampleId");
            if (sampleId == null) continue;
            
            if (deduplicated.containsKey(sampleId)) {
                // Merge with existing entry, keeping most complete data
                Map<String, Object> existing = deduplicated.get(sampleId);
                Map<String, Object> merged = mergeEntries(existing, entry);
                deduplicated.put(sampleId, merged);
            } else {
                deduplicated.put(sampleId, entry);
            }
        }
        
        return new ArrayList<>(deduplicated.values());
    }
    
    /**
     * Merge two entries, preferring non-null values
     */
    private Map<String, Object> mergeEntries(Map<String, Object> existing, Map<String, Object> newEntry) {
        Map<String, Object> merged = new HashMap<>(existing);
        
        for (Map.Entry<String, Object> entry : newEntry.entrySet()) {
            if (entry.getValue() != null && 
                (merged.get(entry.getKey()) == null || 
                 isMoreComplete(entry.getValue(), merged.get(entry.getKey())))) {
                merged.put(entry.getKey(), entry.getValue());
            }
        }
        
        // Recalculate completeness
        merged.put("dataCompleteness", calculateDataCompleteness(merged));
        
        return merged;
    }
    
    /**
     * Check if new value is more complete than existing
     */
    private boolean isMoreComplete(Object newValue, Object existingValue) {
        if (existingValue == null) return true;
        if (newValue == null) return false;
        
        // Prefer longer strings (likely more complete)
        if (newValue instanceof String && existingValue instanceof String) {
            return ((String) newValue).length() > ((String) existingValue).length();
        }
        
        return false;
    }
}