import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;

public class EpicollectConnectionTest {
    
    private static final String EPICOLLECT_BASE_URL = "https://five.epicollect.net";
    private static final String CLIENT_ID = "5589";
    private static final String CLIENT_SECRET = "TCuKqS3Czq3YvYR9MqkskmF4dnGZkeH5PwjZ9wZk";
    private static final String PROJECT_SLUG = "longevity";
    
    public static void main(String[] args) {
        try {
            // Test 1: Get access token
            System.out.println("Testing Epicollect OAuth token retrieval...");
            String accessToken = getAccessToken();
            System.out.println("✓ Access token retrieved successfully");
            
            // Test 2: Test API connection with token
            System.out.println("\nTesting API connection...");
            int entryCount = getEntryCount(accessToken);
            System.out.println("✓ Connected to Epicollect API successfully");
            System.out.println("✓ Found " + entryCount + " entries available");
            
            // Test 3: Fetch a sample entry
            System.out.println("\nFetching sample entry...");
            fetchSampleEntry(accessToken);
            System.out.println("✓ Sample entry fetched successfully");
            
            System.out.println("\n🎉 All tests passed! Epicollect integration is ready.");
            
        } catch (Exception e) {
            System.err.println("❌ Test failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private static String getAccessToken() throws Exception {
        Map<String, String> tokenRequest = new HashMap<>();
        tokenRequest.put("grant_type", "client_credentials");
        tokenRequest.put("client_id", CLIENT_ID);
        tokenRequest.put("client_secret", CLIENT_SECRET);
        
        URL url = new URL(EPICOLLECT_BASE_URL + "/api/oauth/token");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/vnd.api+json");
        conn.setDoOutput(true);
        
        ObjectMapper mapper = new ObjectMapper();
        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = mapper.writeValueAsString(tokenRequest).getBytes("utf-8");
            os.write(input, 0, input.length);
        }
        
        int responseCode = conn.getResponseCode();
        if (responseCode != HttpURLConnection.HTTP_OK) {
            throw new RuntimeException("Failed to get access token: HTTP " + responseCode);
        }
        
        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            
            Map<String, Object> tokenResponse = mapper.readValue(response.toString(), Map.class);
            return (String) tokenResponse.get("access_token");
        }
    }
    
    private static int getEntryCount(String accessToken) throws Exception {
        URL url = new URL(EPICOLLECT_BASE_URL + "/api/export/entries/" + PROJECT_SLUG + "?per_page=1");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Authorization", "Bearer " + accessToken);
        
        int responseCode = conn.getResponseCode();
        if (responseCode != HttpURLConnection.HTTP_OK) {
            throw new RuntimeException("Failed to fetch entries: HTTP " + responseCode);
        }
        
        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Object> responseData = mapper.readValue(response.toString(), Map.class);
            Map<String, Object> meta = (Map<String, Object>) responseData.get("meta");
            return (Integer) meta.get("total");
        }
    }
    
    private static void fetchSampleEntry(String accessToken) throws Exception {
        URL url = new URL(EPICOLLECT_BASE_URL + "/api/export/entries/" + PROJECT_SLUG + "?per_page=1");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Authorization", "Bearer " + accessToken);
        
        int responseCode = conn.getResponseCode();
        if (responseCode != HttpURLConnection.HTTP_OK) {
            throw new RuntimeException("Failed to fetch sample entry: HTTP " + responseCode);
        }
        
        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            
            ObjectMapper mapper = new ObjectMapper();
            Map<String, Object> responseData = mapper.readValue(response.toString(), Map.class);
            Map<String, Object> data = (Map<String, Object>) responseData.get("data");
            java.util.List<Map<String, Object>> entries = (java.util.List<Map<String, Object>>) data.get("entries");
            
            if (!entries.isEmpty()) {
                Map<String, Object> entry = entries.get(0);
                System.out.println("Sample entry UUID: " + entry.get("ec5_uuid"));
                System.out.println("Sample entry created: " + entry.get("created_at"));
                System.out.println("Sample entry keys: " + entry.keySet().size() + " fields");
            }
        }
    }
}