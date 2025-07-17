import java.util.HashMap;
import java.util.Map;

public class CodeConversionTest {
    
    public static void main(String[] args) {
        System.out.println("Testing Epicollect Code Conversion...\n");
        
        // Test cases from actual Epicollect data
        testConversion("5B-003", "Ramaiah Memorial Hospital", "RAM-5B-003");
        testConversion("2b-005", "Ramaiah Memorial Hospital", "RAM-2B-005");
        testConversion("2a-013", "Ramaiah Memorial Hospital", "RAM-2A-013");
        testConversion("2A-014", "Ramaiah Memorial Hospital", "RAM-2A-014");
        testConversion("2A-010", "Ramaiah Memorial Hospital", "RAM-2A-010");
        
        // Test different centers
        testConversion("3A-001", "Satya Sai Institute", "SSI-3A-001");
        testConversion("4B-002", "Baptist Hospital", "BAP-4B-002");
        testConversion("1A-003", "Bangalore Medical College", "BMC-1A-003");
        
        System.out.println("\n✅ All code conversion tests completed!");
    }
    
    private static void testConversion(String oldCode, String center, String expectedNew) {
        Map<String, Object> entry = new HashMap<>();
        entry.put("84_ID_In_the_format_", oldCode);
        entry.put("title", oldCode);
        entry.put("86_Collection_Centre", center);
        
        String result = convertOldToNewFormat(oldCode, entry);
        
        System.out.println(String.format("Old: %-10s + %-25s → New: %-12s %s", 
            oldCode, center, result, result.equals(expectedNew) ? "✅" : "❌"));
    }
    
    private static String convertOldToNewFormat(String oldId, Map<String, Object> entry) {
        if (oldId == null) {
            return null;
        }
        
        // Clean the old ID
        oldId = oldId.replaceAll("\\s+", "").toUpperCase();
        
        // Extract center code from the entry
        String centerCode = determineCenterCode(entry);
        
        // Check if it's already in new format
        if (oldId.matches("[A-Z]{3}-\\d[A-B]-\\d{3}")) {
            return oldId; // Already in new format
        }
        
        // Handle old format conversion (e.g., "5B-003" → "RAM-5B-003")
        if (oldId.matches("\\d[A-B]-\\d{3}")) {
            return centerCode + "-" + oldId;
        }
        
        // Handle variations with different separators or formats
        if (oldId.matches("\\d[A-B]\\d{3}")) {
            // Insert hyphen: "5B003" → "5B-003"
            String formatted = oldId.substring(0, 2) + "-" + oldId.substring(2);
            return centerCode + "-" + formatted;
        }
        
        return centerCode + "-" + oldId; // Best effort
    }
    
    private static String determineCenterCode(Map<String, Object> entry) {
        String centerName = (String) entry.get("86_Collection_Centre");
        if (centerName != null) {
            String normalized = centerName.toLowerCase().trim();
            
            if (normalized.contains("ramaiah")) {
                return "RAM";
            }
            if (normalized.contains("satya") || normalized.contains("sai")) {
                return "SSI";
            }
            if (normalized.contains("baptist")) {
                return "BAP";
            }
            if (normalized.contains("bangalore medical") || normalized.contains("bmcri")) {
                return "BMC";
            }
        }
        
        return "RAM"; // Default
    }
}