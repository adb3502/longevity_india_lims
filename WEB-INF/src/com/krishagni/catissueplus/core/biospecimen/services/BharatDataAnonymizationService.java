package com.krishagni.catissueplus.core.biospecimen.services;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.stereotype.Service;

/**
 * Comprehensive data anonymization service for BHARAT study
 * Removes all personally identifiable information (PII) while preserving
 * research-relevant data and maintaining data linkage through anonymous IDs
 */
@Service
public class BharatDataAnonymizationService {
    
    private static final Log logger = LogFactory.getLog(BharatDataAnonymizationService.class);
    
    // Patterns for detecting PII
    private static final Pattern NAME_PATTERN = Pattern.compile("^[A-Za-z\\s\\.]{2,50}$");
    private static final Pattern PHONE_PATTERN = Pattern.compile("^[\\+]?[0-9\\s\\-\\(\\)]{8,15}$");
    private static final Pattern EMAIL_PATTERN = Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
    private static final Pattern AADHAAR_PATTERN = Pattern.compile("^[0-9]{4}\\s?[0-9]{4}\\s?[0-9]{4}$");
    private static final Pattern ADDRESS_KEYWORDS = Pattern.compile("(?i)(street|road|lane|avenue|plot|door|house|apartment|flat|building|colony|nagar|puram|gali|marg)");
    
    // Salt for consistent hashing (should be loaded from secure config)
    private static final String HASH_SALT = "BHARAT_STUDY_2024_SALT_KEY";
    
    // Anonymization statistics
    private final Map<String, Integer> anonymizationStats = new HashMap<>();
    
    /**
     * Anonymize complete participant data entry
     */
    public Map<String, Object> anonymizeParticipantData(Map<String, Object> rawData) {
        Map<String, Object> anonymizedData = new HashMap<>();
        
        logger.info("Starting anonymization for participant data");
        
        // Process each field in the raw data
        for (Map.Entry<String, Object> entry : rawData.entrySet()) {
            String fieldName = entry.getKey();
            Object value = entry.getValue();
            
            // Anonymize based on field type and content
            Object anonymizedValue = anonymizeField(fieldName, value);
            anonymizedData.put(fieldName, anonymizedValue);
        }
        
        // Generate anonymous participant ID
        String anonymousId = generateAnonymousId(rawData);
        anonymizedData.put("anonymous_participant_id", anonymousId);
        
        // Add anonymization metadata
        anonymizedData.put("anonymization_timestamp", new Date().toString());
        anonymizedData.put("anonymization_version", "1.0");
        
        logger.info("Anonymization completed. Fields processed: " + rawData.size());
        
        return anonymizedData;
    }
    
    /**
     * Anonymize individual field based on content and context
     */
    private Object anonymizeField(String fieldName, Object value) {
        if (value == null) {
            return null;
        }
        
        String stringValue = value.toString().trim();
        
        // Skip empty values
        if (StringUtils.isBlank(stringValue)) {
            return stringValue;
        }
        
        // Check for direct PII fields
        if (isDirectPIIField(fieldName)) {
            return anonymizeDirectPII(fieldName, stringValue);
        }
        
        // Check for indirect PII in content
        if (containsIndirectPII(stringValue)) {
            return anonymizeIndirectPII(fieldName, stringValue);
        }
        
        // For clinical data, preserve medical relevance while removing identifiers
        if (isClinicalField(fieldName)) {
            return anonymizeClinicalData(fieldName, stringValue);
        }
        
        // Return as-is if no PII detected
        return value;
    }
    
    /**
     * Check if field name indicates direct PII
     */
    private boolean isDirectPIIField(String fieldName) {
        String lowerFieldName = fieldName.toLowerCase();
        
        return lowerFieldName.contains("name") ||
               lowerFieldName.contains("phone") ||
               lowerFieldName.contains("mobile") ||
               lowerFieldName.contains("email") ||
               lowerFieldName.contains("address") ||
               lowerFieldName.contains("aadhaar") ||
               lowerFieldName.contains("pan") ||
               lowerFieldName.contains("voter") ||
               lowerFieldName.contains("passport") ||
               lowerFieldName.contains("father") ||
               lowerFieldName.contains("mother") ||
               lowerFieldName.contains("spouse") ||
               lowerFieldName.contains("guardian") ||
               lowerFieldName.contains("emergency_contact") ||
               lowerFieldName.contains("next_of_kin");
    }
    
    /**
     * Anonymize direct PII fields
     */
    private String anonymizeDirectPII(String fieldName, String value) {
        String lowerFieldName = fieldName.toLowerCase();
        
        // Names - replace with anonymous identifier
        if (lowerFieldName.contains("name")) {
            incrementStat("names_anonymized");
            return "PARTICIPANT_" + generateShortHash(value);
        }
        
        // Phone numbers - replace with pattern
        if (lowerFieldName.contains("phone") || lowerFieldName.contains("mobile")) {
            incrementStat("phones_anonymized");
            return "XXX-XXX-" + value.substring(Math.max(0, value.length() - 4));
        }
        
        // Email addresses - replace with anonymous email
        if (lowerFieldName.contains("email")) {
            incrementStat("emails_anonymized");
            return "participant_" + generateShortHash(value) + "@anonymized.bharat";
        }
        
        // Addresses - replace with city/state only
        if (lowerFieldName.contains("address")) {
            incrementStat("addresses_anonymized");
            return anonymizeAddress(value);
        }
        
        // Government IDs - completely remove
        if (lowerFieldName.contains("aadhaar") || lowerFieldName.contains("pan") || 
            lowerFieldName.contains("voter") || lowerFieldName.contains("passport")) {
            incrementStat("ids_anonymized");
            return "[REDACTED]";
        }
        
        // Default anonymization
        incrementStat("other_pii_anonymized");
        return "[ANONYMIZED]";
    }
    
    /**
     * Check if content contains indirect PII
     */
    private boolean containsIndirectPII(String content) {
        return NAME_PATTERN.matcher(content).matches() ||
               PHONE_PATTERN.matcher(content).matches() ||
               EMAIL_PATTERN.matcher(content).matches() ||
               AADHAAR_PATTERN.matcher(content).matches() ||
               ADDRESS_KEYWORDS.matcher(content).find();
    }
    
    /**
     * Anonymize indirect PII found in content
     */
    private String anonymizeIndirectPII(String fieldName, String content) {
        String anonymized = content;
        
        // Replace phone numbers
        anonymized = anonymized.replaceAll("\\b[0-9]{10}\\b", "[PHONE_REDACTED]");
        anonymized = anonymized.replaceAll("\\b\\+91[0-9]{10}\\b", "[PHONE_REDACTED]");
        
        // Replace email addresses
        anonymized = anonymized.replaceAll("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b", "[EMAIL_REDACTED]");
        
        // Replace Aadhaar numbers
        anonymized = anonymized.replaceAll("\\b[0-9]{4}\\s?[0-9]{4}\\s?[0-9]{4}\\b", "[AADHAAR_REDACTED]");
        
        // Replace potential names (sequences of capitalized words)
        anonymized = anonymized.replaceAll("\\b[A-Z][a-z]+\\s+[A-Z][a-z]+\\b", "[NAME_REDACTED]");
        
        // Replace address components
        anonymized = ADDRESS_KEYWORDS.matcher(anonymized).replaceAll("[ADDRESS_REDACTED]");
        
        if (!anonymized.equals(content)) {
            incrementStat("indirect_pii_anonymized");
        }
        
        return anonymized;
    }
    
    /**
     * Check if field is clinical data
     */
    private boolean isClinicalField(String fieldName) {
        String lowerFieldName = fieldName.toLowerCase();
        
        return lowerFieldName.contains("medical") ||
               lowerFieldName.contains("diagnosis") ||
               lowerFieldName.contains("medication") ||
               lowerFieldName.contains("treatment") ||
               lowerFieldName.contains("symptom") ||
               lowerFieldName.contains("condition") ||
               lowerFieldName.contains("disease") ||
               lowerFieldName.contains("procedure") ||
               lowerFieldName.contains("surgery") ||
               lowerFieldName.contains("allergy") ||
               lowerFieldName.contains("family_history") ||
               lowerFieldName.contains("social_history");
    }
    
    /**
     * Anonymize clinical data while preserving medical relevance
     */
    private String anonymizeClinicalData(String fieldName, String content) {
        String anonymized = content;
        
        // Remove doctor names while preserving medical information
        anonymized = anonymized.replaceAll("\\bDr\\.?\\s+[A-Z][a-z]+\\s+[A-Z][a-z]+\\b", "Dr. [PHYSICIAN_NAME]");
        
        // Remove hospital names while preserving medical procedures
        anonymized = anonymized.replaceAll("\\b[A-Z][a-z]+\\s+(Hospital|Medical Center|Clinic|Healthcare)\\b", "[HEALTHCARE_FACILITY]");
        
        // Remove specific dates while preserving relative timing
        anonymized = anonymized.replaceAll("\\b\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4}\\b", "[DATE_REDACTED]");
        
        // Remove medication brand names but preserve generic names
        anonymized = anonymized.replaceAll("\\b[A-Z][a-z]+\\s*\\(([a-z]+)\\)\\b", "[BRAND_NAME]($1)");
        
        incrementStat("clinical_data_anonymized");
        return anonymized;
    }
    
    /**
     * Anonymize address while preserving geographical relevance
     */
    private String anonymizeAddress(String address) {
        // Extract city and state information
        String[] parts = address.split(",");
        
        // Keep only city and state (last 2 parts typically)
        if (parts.length >= 2) {
            String city = parts[parts.length - 2].trim();
            String state = parts[parts.length - 1].trim();
            
            // Remove specific address details but keep general location
            return "[ADDRESS_REDACTED], " + city + ", " + state;
        }
        
        return "[ADDRESS_REDACTED]";
    }
    
    /**
     * Generate anonymous participant ID based on original data
     */
    private String generateAnonymousId(Map<String, Object> rawData) {
        // Create a deterministic hash based on key identifying fields
        StringBuilder identifierBuilder = new StringBuilder();
        
        // Use stable fields that won't change but are unique
        identifierBuilder.append(rawData.get("ec5_uuid"));
        identifierBuilder.append(rawData.get("created_at"));
        identifierBuilder.append(rawData.get("84_ID_In_the_format_")); // Sample ID
        
        return "BHARAT_ANON_" + generateHash(identifierBuilder.toString());
    }
    
    /**
     * Generate consistent hash for anonymization
     */
    private String generateHash(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            digest.update(HASH_SALT.getBytes());
            byte[] hashBytes = digest.digest(input.getBytes());
            
            StringBuilder hexString = new StringBuilder();
            for (byte b : hashBytes) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            
            return hexString.toString().substring(0, 12).toUpperCase();
        } catch (NoSuchAlgorithmException e) {
            logger.error("Error generating hash", e);
            return UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
        }
    }
    
    /**
     * Generate short hash for field anonymization
     */
    private String generateShortHash(String input) {
        return generateHash(input).substring(0, 8);
    }
    
    /**
     * Increment anonymization statistics
     */
    private void incrementStat(String statName) {
        anonymizationStats.put(statName, anonymizationStats.getOrDefault(statName, 0) + 1);
    }
    
    /**
     * Get anonymization statistics
     */
    public Map<String, Integer> getAnonymizationStats() {
        return new HashMap<>(anonymizationStats);
    }
    
    /**
     * Reset anonymization statistics
     */
    public void resetStats() {
        anonymizationStats.clear();
    }
    
    /**
     * Validate that data has been properly anonymized
     */
    public boolean validateAnonymization(Map<String, Object> data) {
        List<String> piiViolations = new ArrayList<>();
        
        for (Map.Entry<String, Object> entry : data.entrySet()) {
            String fieldName = entry.getKey();
            Object value = entry.getValue();
            
            if (value == null) continue;
            
            String stringValue = value.toString();
            
            // Check for remaining PII
            if (PHONE_PATTERN.matcher(stringValue).find()) {
                piiViolations.add("Phone number found in field: " + fieldName);
            }
            
            if (EMAIL_PATTERN.matcher(stringValue).find()) {
                piiViolations.add("Email address found in field: " + fieldName);
            }
            
            if (AADHAAR_PATTERN.matcher(stringValue).find()) {
                piiViolations.add("Aadhaar number found in field: " + fieldName);
            }
            
            // Check for potential names (multiple consecutive capitalized words)
            if (stringValue.matches(".*\\b[A-Z][a-z]+\\s+[A-Z][a-z]+\\s+[A-Z][a-z]+\\b.*")) {
                piiViolations.add("Potential name found in field: " + fieldName);
            }
        }
        
        if (!piiViolations.isEmpty()) {
            logger.warn("PII validation failed: " + String.join(", ", piiViolations));
            return false;
        }
        
        return true;
    }
    
    /**
     * Create anonymization report
     */
    public Map<String, Object> generateAnonymizationReport() {
        Map<String, Object> report = new HashMap<>();
        
        report.put("anonymization_stats", getAnonymizationStats());
        report.put("total_fields_processed", anonymizationStats.values().stream().mapToInt(Integer::intValue).sum());
        report.put("generation_timestamp", new Date().toString());
        report.put("anonymization_version", "1.0");
        
        return report;
    }
    
    /**
     * Extract research-relevant demographics while removing PII
     */
    public Map<String, Object> extractAnonymizedDemographics(Map<String, Object> rawData) {
        Map<String, Object> demographics = new HashMap<>();
        
        // Age (preserve as research data)
        Object age = rawData.get("age");
        if (age != null) {
            demographics.put("age", age);
            demographics.put("age_group", calculateAgeGroup(age));
        }
        
        // Gender (preserve as research data)
        Object gender = rawData.get("gender");
        if (gender != null) {
            demographics.put("gender", normalizeGender(gender.toString()));
        }
        
        // Collection center (preserve for research)
        Object center = rawData.get("86_Collection_Centre");
        if (center != null) {
            demographics.put("collection_center", center);
        }
        
        // Collection date (preserve for research)
        Object collectionDate = rawData.get("created_at");
        if (collectionDate != null) {
            demographics.put("collection_date", collectionDate);
        }
        
        return demographics;
    }
    
    /**
     * Calculate age group for research purposes
     */
    private int calculateAgeGroup(Object age) {
        try {
            int ageInt = Integer.parseInt(age.toString());
            if (ageInt >= 18 && ageInt <= 29) return 1;
            if (ageInt >= 30 && ageInt <= 44) return 2;
            if (ageInt >= 45 && ageInt <= 59) return 3;
            if (ageInt >= 60 && ageInt <= 74) return 4;
            if (ageInt >= 75) return 5;
        } catch (NumberFormatException e) {
            logger.warn("Invalid age format: " + age);
        }
        return 0; // Unknown
    }
    
    /**
     * Normalize gender for research purposes
     */
    private String normalizeGender(String gender) {
        String normalized = gender.toLowerCase().trim();
        if (normalized.startsWith("m") || normalized.equals("1")) return "M";
        if (normalized.startsWith("f") || normalized.equals("2")) return "F";
        return "O"; // Other
    }
}