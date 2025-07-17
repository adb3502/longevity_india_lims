package com.krishagni.catissueplus.core.biospecimen.services;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.krishagni.catissueplus.core.common.events.RequestEvent;
import com.krishagni.catissueplus.core.common.events.ResponseEvent;
import com.krishagni.catissueplus.core.biospecimen.events.CollectionProtocolRegistrationDetail;
import com.krishagni.catissueplus.core.biospecimen.events.ParticipantDetail;
import com.krishagni.catissueplus.core.biospecimen.services.EpicollectDataCleaningService;

import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;

@Service
public class EpicollectImportService {
    
    private static final Log logger = LogFactory.getLog(EpicollectImportService.class);
    
    private static final String EPICOLLECT_BASE_URL = "https://five.epicollect.net";
    private static final String PROJECT_SLUG = "longevity";
    
    // Configuration - loaded from properties file
    private String CLIENT_ID;
    private String CLIENT_SECRET;
    
    public EpicollectImportService() {
        loadConfiguration();
    }
    
    private void loadConfiguration() {
        try {
            // First try to load from external config file
            java.util.Properties props = new java.util.Properties();
            java.io.File configFile = new java.io.File("epicollect-config.properties");
            if (configFile.exists()) {
                try (java.io.FileInputStream fis = new java.io.FileInputStream(configFile)) {
                    props.load(fis);
                    CLIENT_ID = props.getProperty("epicollect.client.id");
                    CLIENT_SECRET = props.getProperty("epicollect.client.secret");
                    logger.info("Loaded Epicollect configuration from file");
                }
            } else {
                // Fall back to environment variables
                CLIENT_ID = System.getenv("EPICOLLECT_CLIENT_ID");
                CLIENT_SECRET = System.getenv("EPICOLLECT_CLIENT_SECRET");
                logger.info("Using Epicollect configuration from environment");
            }
        } catch (Exception e) {
            logger.error("Error loading Epicollect configuration", e);
        }
    }
    
    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("dd/MM/yyyy");
    
    @Autowired
    private CollectionProtocolRegistrationService cprService;
    
    @Autowired
    private EpicollectDataCleaningService cleaningService;
    
    private ObjectMapper objectMapper = new ObjectMapper();
    
    private String accessToken;
    private long tokenExpiryTime;
    
    /**
     * Scheduled task to import data from Epicollect every hour
     */
    @Scheduled(fixedDelay = 3600000) // Run every hour
    public void importDataFromEpicollect() {
        try {
            logger.info("Starting Epicollect data import...");
            
            // Get or refresh access token
            ensureValidToken();
            
            // Fetch entries from Epicollect
            List<Map<String, Object>> entries = fetchEntries();
            
            // Process each entry
            int imported = 0;
            int skipped = 0;
            
            for (Map<String, Object> entry : entries) {
                try {
                    if (processEntry(entry)) {
                        imported++;
                    } else {
                        skipped++;
                    }
                } catch (Exception e) {
                    logger.error("Error processing entry: " + entry.get("ec5_uuid"), e);
                    skipped++;
                }
            }
            
            logger.info(String.format("Epicollect import completed. Imported: %d, Skipped: %d", imported, skipped));
            
        } catch (Exception e) {
            logger.error("Error during Epicollect import", e);
        }
    }
    
    /**
     * Ensure we have a valid access token
     */
    private void ensureValidToken() throws IOException {
        if (accessToken == null || System.currentTimeMillis() >= tokenExpiryTime) {
            refreshToken();
        }
    }
    
    /**
     * Get new access token from Epicollect
     */
    private void refreshToken() throws IOException {
        Map<String, String> tokenRequest = new HashMap<>();
        tokenRequest.put("grant_type", "client_credentials");
        tokenRequest.put("client_id", CLIENT_ID);
        tokenRequest.put("client_secret", CLIENT_SECRET);
        
        URL url = new URL(EPICOLLECT_BASE_URL + "/api/oauth/token");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/vnd.api+json");
        conn.setDoOutput(true);
        
        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = objectMapper.writeValueAsString(tokenRequest).getBytes("utf-8");
            os.write(input, 0, input.length);
        }
        
        int responseCode = conn.getResponseCode();
        if (responseCode != HttpURLConnection.HTTP_OK) {
            throw new IOException("Failed to get access token: HTTP " + responseCode);
        }
        
        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            
            Map<String, Object> tokenResponse = objectMapper.readValue(
                response.toString(), 
                Map.class
            );
            
            accessToken = (String) tokenResponse.get("access_token");
            int expiresIn = (Integer) tokenResponse.get("expires_in");
            tokenExpiryTime = System.currentTimeMillis() + (expiresIn * 1000L) - 60000L; // Refresh 1 minute early
            
            logger.info("Successfully refreshed Epicollect access token");
        }
    }
    
    /**
     * Fetch entries from Epicollect API
     */
    private List<Map<String, Object>> fetchEntries() throws IOException {
        List<Map<String, Object>> allEntries = new ArrayList<>();
        String nextUrl = EPICOLLECT_BASE_URL + "/api/export/entries/" + PROJECT_SLUG;
        
        while (nextUrl != null) {
            URL url = new URL(nextUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Authorization", "Bearer " + accessToken);
            
            int responseCode = conn.getResponseCode();
            if (responseCode != HttpURLConnection.HTTP_OK) {
                throw new IOException("Failed to fetch entries: HTTP " + responseCode);
            }
            
            try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                
                Map<String, Object> responseData = objectMapper.readValue(
                    response.toString(), 
                    Map.class
                );
                
                Map<String, Object> data = (Map<String, Object>) responseData.get("data");
                List<Map<String, Object>> entries = (List<Map<String, Object>>) data.get("entries");
                allEntries.addAll(entries);
                
                // Check for next page
                Map<String, Object> links = (Map<String, Object>) responseData.get("links");
                nextUrl = (String) links.get("next");
            }
        }
        
        logger.info("Fetched " + allEntries.size() + " entries from Epicollect");
        
        // Use cleaning service to deduplicate entries
        if (!allEntries.isEmpty()) {
            allEntries = cleaningService.deduplicateEntries(allEntries);
            logger.info("After deduplication: " + allEntries.size() + " entries");
        }
        
        return allEntries;
    }
    
    /**
     * Process a single Epicollect entry
     */
    private boolean processEntry(Map<String, Object> entry) throws Exception {
        // Extract participant data from entry
        String epicollectUuid = (String) entry.get("ec5_uuid");
        
        // Check if already imported
        if (isAlreadyImported(epicollectUuid)) {
            return false;
        }
        
        // Clean and validate the entry using the cleaning service
        Map<String, Object> cleanedEntry = cleaningService.cleanEntry(entry);
        if (cleanedEntry == null) {
            logger.warn("Entry rejected during cleaning: " + epicollectUuid);
            return false;
        }
        
        // Parse personal information branch
        Map<String, Object> personalInfo = extractPersonalInfo(entry);
        if (personalInfo == null) {
            logger.warn("No personal information found for entry: " + epicollectUuid);
            return false;
        }
        
        // Create participant
        ParticipantDetail participant = new ParticipantDetail();
        
        // Extract and sanitize personal data
        String name = (String) personalInfo.get("name");
        if (name != null && !name.isEmpty()) {
            // Scrub personal information - replace with anonymous identifier
            participant.setFirstName("Participant");
            participant.setLastName(generateAnonymousId(epicollectUuid));
        }
        
        // Extract age and gender
        Integer age = parseInteger(personalInfo.get("age"));
        String gender = mapGender((String) personalInfo.get("gender"));
        participant.setGender(gender);
        
        // Calculate birth year from age (approximate)
        if (age != null) {
            int birthYear = Calendar.getInstance().get(Calendar.YEAR) - age;
            participant.setBirthDate(DATE_FORMAT.parse("01/01/" + birthYear));
        }
        
        // Get center code from cleaned entry
        String centerCode = (String) cleanedEntry.get("centerCode");
        if (centerCode == null || "UNK".equals(centerCode)) {
            centerCode = "RAM"; // Default to RAM if unknown
        }
        
        // Create CPR registration
        CollectionProtocolRegistrationDetail cpr = new CollectionProtocolRegistrationDetail();
        cpr.setCpId(1L); // BHARAT Study CP ID
        cpr.setRegistrationDate(new Date());
        cpr.setParticipant(participant);
        
        // Create custom field for Epicollect link
        Map<String, Object> customFields = new HashMap<>();
        customFields.put("epicollect_uuid", epicollectUuid);
        customFields.put("import_date", new Date());
        
        // Extract vitals if available
        Map<String, Object> vitals = extractVitals(entry);
        if (vitals != null) {
            customFields.putAll(vitals);
        }
        
        // Store custom fields
        // TODO: Set custom fields on participant or CPR
        
        // Create participant through service
        RequestEvent<CollectionProtocolRegistrationDetail> req = new RequestEvent<>(cpr);
        ResponseEvent<CollectionProtocolRegistrationDetail> resp = cprService.createRegistration(req);
        
        if (!resp.isSuccessful()) {
            logger.error("Failed to create participant: " + resp.getError().getMessage());
            return false;
        }
        
        // Store integration record
        storeIntegrationRecord(resp.getPayload().getId(), epicollectUuid, entry);
        
        return true;
    }
    
    /**
     * Extract personal information from entry
     */
    private Map<String, Object> extractPersonalInfo(Map<String, Object> entry) {
        // Personal information is stored in a branch
        // The structure varies based on Epicollect form design
        // This is a simplified extraction - adjust based on actual data structure
        
        Map<String, Object> personalInfo = new HashMap<>();
        
        // Try to extract from known fields
        for (String key : entry.keySet()) {
            if (key.contains("Name")) {
                personalInfo.put("name", entry.get(key));
            } else if (key.contains("Age")) {
                personalInfo.put("age", entry.get(key));
            } else if (key.contains("Gender")) {
                personalInfo.put("gender", entry.get(key));
            } else if (key.contains("Date_of_birth")) {
                personalInfo.put("dob", entry.get(key));
            }
        }
        
        return personalInfo.isEmpty() ? null : personalInfo;
    }
    
    /**
     * Extract vitals information
     */
    private Map<String, Object> extractVitals(Map<String, Object> entry) {
        Map<String, Object> vitals = new HashMap<>();
        
        // Extract vital signs
        for (String key : entry.keySet()) {
            if (key.contains("BP")) {
                vitals.put("blood_pressure", entry.get(key));
            } else if (key.contains("Pulse")) {
                vitals.put("pulse", entry.get(key));
            } else if (key.contains("Temperature")) {
                vitals.put("temperature", entry.get(key));
            } else if (key.contains("SPo2")) {
                vitals.put("spo2", entry.get(key));
            }
        }
        
        return vitals.isEmpty() ? null : vitals;
    }
    
    /**
     * Generate anonymous identifier from UUID
     */
    private String generateAnonymousId(String uuid) {
        // Use last 6 characters of UUID as anonymous ID
        return "ANON-" + uuid.substring(uuid.length() - 6).toUpperCase();
    }
    
    /**
     * Map Epicollect gender values to OpenSpecimen values
     */
    private String mapGender(String epicollectGender) {
        if (epicollectGender == null) {
            return "Unknown";
        }
        
        switch (epicollectGender.toLowerCase()) {
            case "male":
                return "Male";
            case "female":
                return "Female";
            case "others":
                return "Unknown";
            default:
                return "Unknown";
        }
    }
    
    /**
     * Parse integer safely
     */
    private Integer parseInteger(Object value) {
        if (value == null) {
            return null;
        }
        
        try {
            if (value instanceof Number) {
                return ((Number) value).intValue();
            } else {
                return Integer.parseInt(value.toString());
            }
        } catch (NumberFormatException e) {
            return null;
        }
    }
    
    /**
     * Check if entry was already imported
     */
    private boolean isAlreadyImported(String epicollectUuid) {
        // TODO: Query database to check if this UUID was already imported
        // For now, return false
        return false;
    }
    
    /**
     * Store integration record in database
     */
    private void storeIntegrationRecord(Long participantId, String epicollectUuid, Map<String, Object> rawData) {
        // TODO: Store in os_bharat_data_integrations table
        logger.info("Stored integration record for participant " + participantId + " with Epicollect UUID " + epicollectUuid);
    }
    
    /**
     * Check if Epicollect service is properly configured
     */
    public boolean isConfigured() {
        return CLIENT_ID != null && CLIENT_SECRET != null && 
               !CLIENT_ID.isEmpty() && !CLIENT_SECRET.isEmpty();
    }
}