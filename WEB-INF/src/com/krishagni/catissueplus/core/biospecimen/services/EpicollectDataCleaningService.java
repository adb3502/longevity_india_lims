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
    
    // Valid center codes
    private static final Map<String, String> CENTER_MAPPINGS = new HashMap<>();
    static {
        CENTER_MAPPINGS.put("ramaiah", "RAM");
        CENTER_MAPPINGS.put("ram", "RAM");
        CENTER_MAPPINGS.put("rmc", "RAM");
        CENTER_MAPPINGS.put("ms ramaiah", "RAM");
        
        CENTER_MAPPINGS.put("satya sai", "SSI");
        CENTER_MAPPINGS.put("satyasai", "SSI");
        CENTER_MAPPINGS.put("ssi", "SSI");
        CENTER_MAPPINGS.put("sri sathya sai", "SSI");
        
        CENTER_MAPPINGS.put("baptist", "BAP");
        CENTER_MAPPINGS.put("bap", "BAP");
        CENTER_MAPPINGS.put("baptist hospital", "BAP");
        
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
        
        // Clean personal information
        cleaned.putAll(cleanPersonalInfo(rawEntry));
        
        // Clean center information
        String center = cleanCenterCode(rawEntry);
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
     * Clean sample ID - remove spaces, standardize format
     */
    private String cleanSampleId(Map<String, Object> entry) {
        String sampleId = getStringValue(entry, "sample_id", "sampleId", "Sample_ID");
        if (sampleId == null) {
            return null;
        }
        
        // Remove spaces and convert to uppercase
        sampleId = sampleId.replaceAll("\\s+", "").toUpperCase();
        
        // Validate format (expecting something like RAM-1A-001)
        if (!Pattern.matches("[A-Z]{3}-\\d[A-B]-\\d{3}", sampleId)) {
            logger.warn("Invalid sample ID format: " + sampleId);
            // Try to fix common issues
            sampleId = fixSampleIdFormat(sampleId);
        }
        
        return sampleId;
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
    
    /**
     * Get string value from multiple possible field names
     */
    private String getStringValue(Map<String, Object> entry, String... possibleKeys) {
        for (String key : possibleKeys) {
            // Try exact match
            Object value = entry.get(key);
            if (value != null && StringUtils.isNotBlank(value.toString())) {
                return value.toString().trim();
            }
            
            // Try case-insensitive match
            for (String entryKey : entry.keySet()) {
                if (entryKey.equalsIgnoreCase(key)) {
                    value = entry.get(entryKey);
                    if (value != null && StringUtils.isNotBlank(value.toString())) {
                        return value.toString().trim();
                    }
                }
            }
        }
        return null;
    }
    
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
    private Date cleanDate(Object dateValue) {
        if (dateValue == null) return null;
        
        try {
            if (dateValue instanceof Date) {
                return (Date) dateValue;
            }
            // Parse ISO format or other common formats
            // Implementation depends on actual date formats in data
            return new Date(); // Placeholder
        } catch (Exception e) {
            return null;
        }
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