# Epicollect5 Integration Guide for LIIMS

## Overview
This guide explains how to configure and use the Epicollect5 integration in LIIMS for importing participant data from the Longevity project.

## Configuration

### 1. Set Up Credentials
The Epicollect5 API credentials have been configured in `epicollect-config.properties`:
- Client ID: 5589
- Project: longevity (315 entries as of last check)

**Security Note**: The configuration file containing secrets is excluded from version control via .gitignore.

### 2. Configuration File Structure
```properties
epicollect.client.id=5589
epicollect.client.secret=YOUR_SECRET_HERE
epicollect.project.slug=longevity
epicollect.base.url=https://five.epicollect.net
epicollect.import.schedule=0 0 * * * ?  # Every hour
epicollect.import.enabled=true
```

### 3. Test Connection
Run the test script to verify connectivity:
```bash
./test-epicollect-connection.sh
```

## Data Import Process

### Automatic Import
- Imports run automatically every hour (configurable)
- Service checks for new/updated entries
- Only imports entries not previously processed

### Manual Import
1. Navigate to the Epicollect Integration page in LIIMS
2. Click "Import Now" button
3. Monitor progress in the activity log

### Data Privacy
During import, the following privacy rules are applied:
- **Names**: Anonymized to "Participant ANON-XXXXXX"
- **Contact Information**: Removed
- **Addresses**: Removed
- **Age/Gender**: Retained for study requirements
- **Clinical Data**: Retained (vitals, medical history)

## Field Mappings

| Epicollect Field | LIIMS Field | Privacy Rule |
|-----------------|-------------|--------------|
| Name | participant.firstName + lastName | ANONYMIZE |
| Age | participant.age | RETAIN |
| Gender | participant.gender | RETAIN |
| Date_of_birth | participant.birthDate | RETAIN |
| Contact_Information | - | REMOVE |
| Address | - | REMOVE |
| BP | customFields.blood_pressure | RETAIN |
| Pulse | customFields.pulse | RETAIN |
| Temperature | customFields.temperature | RETAIN |
| SPo2 | customFields.spo2 | RETAIN |

## Monitoring

### Import Status
Check import status via:
1. LIIMS UI: Epicollect Integration page
2. API: `GET /api/epicollect/status`
3. Logs: Check application logs for detailed import information

### Troubleshooting

**Import Failures**:
- Check credentials in config file
- Verify network connectivity to Epicollect5
- Check application logs for specific errors

**Missing Data**:
- Verify field mappings match current Epicollect form
- Check privacy rules aren't filtering required data
- Ensure participant doesn't already exist (duplicates are skipped)

## API Endpoints

### Manual Import Trigger
```
POST /api/epicollect/import
```

### Get Import Status
```
GET /api/epicollect/status
```

### Get Field Mappings
```
GET /api/epicollect/mappings
```

### Update Configuration
```
POST /api/epicollect/config
Body: {
  "clientId": "5589",
  "clientSecret": "YOUR_SECRET"
}
```

## Security Considerations

1. **Credentials Storage**: 
   - Never commit credentials to version control
   - Use the config file or environment variables
   - Rotate secrets periodically

2. **Data Privacy**:
   - All personal identifiers are removed/anonymized
   - Only essential research data is retained
   - Audit logs track all imports

3. **Access Control**:
   - Only administrators can trigger manual imports
   - Import logs are restricted to authorized users

## Development Notes

### Adding New Field Mappings
1. Update `extractPersonalInfo()` method in `EpicollectImportService.java`
2. Add privacy rule if needed
3. Update this documentation

### Modifying Import Schedule
Change the cron expression in config:
```properties
# Every 30 minutes
epicollect.import.schedule=0 */30 * * * ?

# Daily at 2 AM
epicollect.import.schedule=0 0 2 * * ?
```

## Current Statistics
- Total Epicollect Entries: 315
- Project: Longevity
- Centers: RAM (Ramaiah), VEL (Vellore), PGI (Chandigarh)
- Age Groups: 5 (18-29, 30-44, 45-59, 60-74, 75+)

---
Last Updated: 2025-07-17