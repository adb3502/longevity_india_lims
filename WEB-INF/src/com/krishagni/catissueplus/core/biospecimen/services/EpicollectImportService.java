package com.krishagni.catissueplus.core.biospecimen.services;

import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.sql.DataSource;

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
import com.krishagni.catissueplus.core.biospecimen.services.CollectionProtocolRegistrationService;

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
    
    @Autowired
    private DataSource dataSource;
    
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
            int errors = 0;
            
            for (Map<String, Object> entry : entries) {
                try {
                    String uuid = (String) entry.get("ec5_uuid");
                    if (processEntry(entry)) {
                        imported++;
                        logger.debug("Successfully imported entry: " + uuid);
                    } else {
                        skipped++;
                        logger.debug("Skipped entry: " + uuid);
                    }
                } catch (Exception e) {
                    errors++;
                    logger.error("Error processing entry: " + entry.get("ec5_uuid"), e);
                }
            }
            
            logger.info(String.format("Epicollect import completed. Imported: %d, Skipped: %d, Errors: %d", 
                imported, skipped, errors));
            
        } catch (Exception e) {
            logger.error("Fatal error during Epicollect import", e);
            throw new RuntimeException("Epicollect import failed", e);
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
            int originalSize = allEntries.size();
            allEntries = cleaningService.deduplicateEntries(allEntries);
            logger.info(String.format("Deduplication: %d original entries -> %d unique entries", 
                originalSize, allEntries.size()));
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
            logger.warn("No center code found for entry " + epicollectUuid + ", defaulting to RAM");
        }
        
        logger.info(String.format("Processing entry %s: center=%s, age=%s, gender=%s", 
            epicollectUuid, centerCode, age, gender));
        
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
        
        // Create participant through service
        RequestEvent<CollectionProtocolRegistrationDetail> req = new RequestEvent<>(cpr);
        ResponseEvent<CollectionProtocolRegistrationDetail> resp = cprService.createRegistration(req);
        
        if (!resp.isSuccessful()) {
            logger.error("Failed to create participant: " + resp.getError().getMessage());
            return false;
        }
        
        CollectionProtocolRegistrationDetail createdCpr = resp.getPayload();
        
        // Store clinical data (vitals) in custom table
        storeClinicalData(createdCpr.getId(), customFields);
        
        // Store integration record
        storeIntegrationRecord(createdCpr.getId(), epicollectUuid, entry);
        
        return true;
    }
    
    /**
     * Extract personal information from entry using actual Epicollect field references
     */
    private Map<String, Object> extractPersonalInfo(Map<String, Object> entry) {
        Map<String, Object> personalInfo = new HashMap<>();
        
        // Based on the actual Epicollect structure from longevity.json
        String nameRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_65d304321b916_65d3044f1b917";
        String ageRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_65d304321b916_66f4e4eab428d";
        String genderRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_65d304321b916_65d3049e1b919";
        String birthDateRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_65d304321b916_66fe666d6315a";
        
        if (entry.containsKey(nameRef)) {
            personalInfo.put("name", entry.get(nameRef));
        }
        if (entry.containsKey(ageRef)) {
            personalInfo.put("age", entry.get(ageRef));
        }
        if (entry.containsKey(genderRef)) {
            personalInfo.put("gender", entry.get(genderRef));
        }
        if (entry.containsKey(birthDateRef)) {
            personalInfo.put("dob", entry.get(birthDateRef));
        }
        
        // Also try the generic field names as fallback
        if (personalInfo.isEmpty()) {
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
        }
        
        return personalInfo.isEmpty() ? null : personalInfo;
    }
    
    /**
     * Extract vitals information using actual Epicollect field references
     */
    private Map<String, Object> extractVitals(Map<String, Object> entry) {
        Map<String, Object> vitals = new HashMap<>();
        
        // Based on the actual Epicollect structure from longevity.json
        String pulseRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_668b942e4c43f_66fe62f7e9559";
        String bpRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_668b942e4c43f_668b94554c441";
        String rrRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_668b942e4c43f_66fe633ce955a";
        String spo2Ref = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_668b942e4c43f_66fe6360e955b";
        String tempRef = "c0520922d953469fadd93baa4ec6e69e_65c06eff6c2b0_668b942e4c43f_66fe6380e955c";
        
        if (entry.containsKey(pulseRef)) {
            vitals.put("pulse", entry.get(pulseRef));
        }
        if (entry.containsKey(bpRef)) {
            vitals.put("blood_pressure", entry.get(bpRef));
        }
        if (entry.containsKey(rrRef)) {
            vitals.put("respiratory_rate", entry.get(rrRef));
        }
        if (entry.containsKey(spo2Ref)) {
            vitals.put("spo2", entry.get(spo2Ref));
        }
        if (entry.containsKey(tempRef)) {
            vitals.put("temperature", entry.get(tempRef));
        }
        
        // Also try the generic field names as fallback
        if (vitals.isEmpty()) {
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
        String sql = "SELECT COUNT(*) FROM os_bharat_data_integrations WHERE epicollect_uuid = ?";
        
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, epicollectUuid);
            ResultSet rs = stmt.executeQuery();
            
            if (rs.next()) {
                return rs.getInt(1) > 0;
            }
        } catch (SQLException e) {
            logger.error("Error checking if entry already imported: " + epicollectUuid, e);
        }
        
        return false;
    }
    
    /**
     * Store integration record in database
     */
    private void storeIntegrationRecord(Long participantId, String epicollectUuid, Map<String, Object> rawData) {
        String sql = "INSERT INTO os_bharat_data_integrations (participant_id, epicollect_uuid, raw_data, imported_at) VALUES (?, ?, ?, ?)";
        
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setLong(1, participantId);
            stmt.setString(2, epicollectUuid);
            stmt.setString(3, objectMapper.writeValueAsString(rawData));
            stmt.setTimestamp(4, new java.sql.Timestamp(System.currentTimeMillis()));
            
            stmt.executeUpdate();
            logger.info("Stored integration record for participant " + participantId + " with Epicollect UUID " + epicollectUuid);
            
        } catch (SQLException | IOException e) {
            logger.error("Error storing integration record for " + epicollectUuid, e);
        }
    }
    
    /**
     * Store clinical data (vitals) in custom table
     */
    private void storeClinicalData(Long cprId, Map<String, Object> clinicalData) {
        if (clinicalData == null || clinicalData.isEmpty()) {
            return;
        }
        
        String sql = "INSERT INTO os_bharat_clinical_data (cpr_id, field_name, field_value, recorded_at) VALUES (?, ?, ?, ?)";
        
        try (Connection conn = dataSource.getConnection()) {
            conn.setAutoCommit(false);
            
            try (PreparedStatement stmt = conn.prepareStatement(sql)) {
                for (Map.Entry<String, Object> entry : clinicalData.entrySet()) {
                    if (entry.getValue() != null) {
                        stmt.setLong(1, cprId);
                        stmt.setString(2, entry.getKey());
                        stmt.setString(3, entry.getValue().toString());
                        stmt.setTimestamp(4, new java.sql.Timestamp(System.currentTimeMillis()));
                        stmt.addBatch();
                    }
                }
                
                stmt.executeBatch();
                conn.commit();
                
                logger.info("Stored " + clinicalData.size() + " clinical data fields for CPR " + cprId);
                
            } catch (SQLException e) {
                conn.rollback();
                throw e;
            }
        } catch (SQLException e) {
            logger.error("Error storing clinical data for CPR " + cprId, e);
        }
    }
    
    /**
     * Check if Epicollect service is properly configured
     */
    public boolean isConfigured() {
        return CLIENT_ID != null && CLIENT_SECRET != null && 
               !CLIENT_ID.isEmpty() && !CLIENT_SECRET.isEmpty();
    }
}