# BHARAT Study Manual Import Guide

## Step 1: Access OpenSpecimen Admin Interface

1. Go to: `http://localhost:8082/openspecimen`
2. Login with: **Username**: `admin`, **Password**: `AmruthDB7!`

## Step 2: Create Collection Protocol

### Option A: JSON Import (Recommended)
1. Navigate to **Collection Protocols** → **List**
2. Click **Import** button
3. Upload the file: `bharat-study-protocol-simple.json`
4. Review and confirm the import

### Option B: Manual Creation
1. Navigate to **Collection Protocols** → **Add**
2. Fill in the basic details:
   - **Title**: "BHARAT Study - Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions"
   - **Short Title**: "BHARAT-STUDY"
   - **Code**: "BHARAT"
   - **Principal Investigator**: Select existing user
   - **Start Date**: January 1, 2024
   - **End Date**: December 31, 2025
   - **Anticipated Participants**: 630

3. **Label Settings**:
   - **Participant ID Format**: `BHARAT-%SYS_UID(4)%`
   - **Specimen Label Format**: `%PPI%-%VISIT_NAME%-%SP_TYPE_ABBR%%SYS_UID(2)%`
   - **Aliquot Label Format**: `%PARENT_SPMN_LABEL%-%SYS_UID(2)%`

4. **Add Collection Events**:
   
   **Event 1: Baseline Visit (V0)**
   - Event Label: "Baseline Visit"
   - Event Point: 0 days
   - Clinical Diagnosis: "V0"
   - Specimens to collect:
     - Whole Blood (10ml, EDTA Tube)
     - Saliva (5ml, Saliva Collection Tube)  
     - Hair (1 sample, Hair Collection Envelope)

   **Event 2: 6 Month Follow-up (V1)**
   - Event Label: "6 Month Follow-up"
   - Event Point: 182 days
   - Clinical Diagnosis: "V1"
   - Specimens: Whole Blood, Saliva

   **Event 3: 12 Month Follow-up (V2)**
   - Event Label: "12 Month Follow-up"
   - Event Point: 365 days
   - Clinical Diagnosis: "V2"
   - Specimens: Whole Blood

   **Event 4: 24 Month Follow-up (V3)**
   - Event Label: "24 Month Follow-up"
   - Event Point: 730 days
   - Clinical Diagnosis: "V3"
   - Specimens: Whole Blood

## Step 3: Create Required Specimen Types (if not present)

1. Navigate to **Administrative** → **Specimen Types**
2. Add if missing:
   - Hair
   - Saliva
   - Buccal Cells

## Step 4: Access BHARAT Dashboards

Once the protocol is created, access your custom dashboards:

1. **Study Overview**: `http://localhost:8082/openspecimen/dist/bharat-study-overview-dashboard.html`
2. **Biomarker Analytics**: `http://localhost:8082/openspecimen/dist/bharat-biomarker-analytics-dashboard.html`
3. **Inventory Management**: `http://localhost:8082/openspecimen/dist/bharat-inventory-dashboard.html`

## Step 5: Test Participant Registration

1. Navigate to **Participants** → **Register**
2. Select "BHARAT-STUDY" protocol
3. Register a test participant
4. Schedule visits and collect specimens
5. Verify the hierarchical labeling works: `BHARAT-AG3-P0234-V0-BLD01`

## Step 6: Configure User Permissions

1. Navigate to **Administrative** → **Roles**
2. Create BHARAT Study specific roles:
   - **BHARAT Study Coordinator**
   - **BHARAT Lab Technician** 
   - **BHARAT Data Analyst**

## Troubleshooting

### If Import Fails:
- Check that all required specimen types exist
- Verify user permissions
- Use the manual creation method instead

### If Dashboards Don't Load:
- Ensure files are in `/www/dist/` directory
- Check browser console for JavaScript errors
- Verify Chart.js library is accessible

### If Labeling Doesn't Work:
- Check Collection Protocol label settings
- Verify specimen requirements are properly configured
- Test with a sample participant registration

## Next Steps

1. **Customize Forms**: Import the multi-omics analysis forms
2. **Configure Reports**: Set up the aging research analytics
3. **Train Users**: Provide access to study coordinators
4. **Data Collection**: Begin participant enrollment and sample collection

## Support

For technical support with the BHARAT Study implementation:
- Email: bharat-study@longevityindia.org
- Documentation: Available in `/dist/configs/` directory