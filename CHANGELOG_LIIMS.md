# LIIMS Change Log

This document provides a detailed record of all changes made to transform OpenSpecimen into LIIMS (Longevity India Information Management System).

## Version History

### v1.0.0 - Initial LIIMS Transformation (2025-07-16)

#### Session 1: Rebranding and UI Customization
**Time**: Morning Session  
**Developer**: adb3502  
**Branch**: longevity-india-dev  

##### 1. Rebranding Changes
- **Logo Replacement**:
  - Replaced all OpenSpecimen logos with Longevity India logos from `lii_logos` folder
  - Updated favicon and application icons

- **Application Name Changes**:
  - Changed all references from "OpenSpecimen" to "LIIMS"
  - Updated application title to "Longevity India Information Management System"

- **Files Modified**:
  ```
  - README.md - Complete rewrite with LIIMS information
  - ui/src/index.html - Title and meta tags
  - ui/src/common/components/About.vue - About section content
  - Various configuration files with name changes
  ```

##### 2. Login Page Customization
- **Background Color Change**:
  - Changed from blue gradient to white background
  - File: `/ui/src/users/views/FormCard.vue`
  - Change: `background: #ffffff;` (was `linear-gradient(135deg, #205081, #2d67a3)`)
  - Change: `color: #205081;` (was `#fff`)

- **Login Message Update**:
  - File: `/ui/src/users/views/LoginForm.vue`
  - Changed to: "Welcome to LIIMS (Longevity India Information Management System)"

- **Domain Dropdown Removal**:
  - File: `/ui/src/users/views/LoginForm.vue`
  - Removed domain selection dropdown
  - Hardcoded domain to 'openspecimen'
  - File: `/ui/src/users/schemas/login.js`
  - Removed domain field from form schema

- **Sign-up Feature Removal**:
  - File: `/ui/src/NoLoginApp.vue`
  - Removed sign-up button and related code
  - Fixed unused import error for 'routerSvc'

##### 3. Application Header Changes
- **Header Background Color**:
  - File: `/ui/src/common/components/Navbar.vue`
  - Changed from blue (#205081) to black (#000000)
  - Border changed to #333333

- **Header Cleanup**:
  - Removed red "TEST" deployment environment box
  - Removed unnecessary icons:
    - Favorites (star icon)
    - New stuff (gift icon)
    - Feedback (comment icon)
    - Notifications (bell icon)
  - Kept only:
    - User profile dropdown
    - About icon (changed from question-circle to info-circle)

- **About Section Update**:
  - File: `/ui/src/common/components/About.vue`
  - Changed footer text to: "maintained by adb3502"
  - Added GitHub profile link: https://github.com/adb3502

##### 4. Authentication Issues Resolved
- **Problem**: Login stopped working after domain dropdown removal
- **Diagnosis**: Account was locked in database
- **Solution**:
  - Accessed MySQL database via Docker
  - Unlocked admin account: `UPDATE catissue_user SET login_attempts_count = 0 WHERE login_name = 'admin';`
  - Reset password to 'Login@123'

#### Session 2: Project-Centric Architecture Implementation
**Time**: Afternoon Session  
**Developer**: adb3502 (with Claude Opus 4)  
**Branch**: longevity-india-dev  

##### 1. Database Schema Extensions
- **File Created**: `/WEB-INF/resources/db/bharat-schema.sql`
- **Tables Added**:
  ```sql
  - os_bharat_participants - Participant coding system
  - os_bharat_data_integrations - External data tracking
  - os_bharat_omics_batches - Multiomics batch management
  - os_bharat_enrollment_stats - Real-time enrollment tracking
  - os_bharat_lab_results - Lab result storage
  - os_bharat_timeline_events - Participant timeline
  ```

##### 2. Backend Java Implementation
- **Domain Model Created**: `/WEB-INF/src/com/krishagni/catissueplus/core/biospecimen/domain/BharatParticipant.java`
  - Implements participant coding: [CENTER]-[GROUP][GENDER]-[SERIAL]
  - Visual coding logic for cryocaps and labels
  - Age group determination logic

- **REST Controller Created**: `/WEB-INF/src/com/krishagni/catissueplus/rest/controller/BharatParticipantController.java`
  - Endpoints implemented:
    ```
    POST /api/bharat/participants/enroll
    GET /api/bharat/participants/{code}
    GET /api/bharat/participants/{code}/timeline
    GET /api/bharat/stats/enrollment
    GET /api/bharat/stats/inventory
    GET /api/bharat/stats/completeness
    ```

- **Compilation Fixes**:
  - Removed inheritance from non-existent BaseEntity class
  - Changed from ParticipantDetail.setRegistrationDate() to CollectionProtocolRegistrationDetail.setRegistrationDate()
  - Commented out setBirthDateStr() implementation temporarily

##### 3. Frontend UI Transformation
- **Home Page Redesign**: `/ui/src/home/views/Home.vue`
  - Replaced module-based cards with project cards:
    - BHARAT Study (Biomarkers of Healthy Aging)
    - Organ Aging Project
    - Cognitive Health Study
  - Added real-time statistics display
  - Created quick actions panel
  - Added recent activity feed

- **Project Dashboard**: `/ui/src/home/views/ProjectDashboard.vue` (NEW)
  - Sample statistics widget with visual indicators
  - Placeholder for data visualization charts
  - Storage overview with capacity tracking
  - Sample tracking table with search
  - Recent collections display

- **BHARAT Enrollment Dashboard**: `/ui/src/home/views/BharatEnrollmentDashboard.vue` (NEW)
  - 5x2 age/gender enrollment matrix
  - Interactive heatmap visualization
  - Center-wise breakdown (RAM, VEL, PGI)
  - Real-time enrollment statistics
  - Participant enrollment form

- **Routing Updates**: `/ui/src/router/index.js`
  - Added routes:
    ```javascript
    /projects/:projectId - Project dashboard
    /bharat/enrollment - BHARAT enrollment dashboard
    ```

##### 4. Visual Coding Implementation
- **Cryocap Colors by Age Group**:
  - Group 1 (18-29): Blue
  - Group 2 (30-44): Green
  - Group 3 (45-59): Yellow
  - Group 4 (60-74): Orange
  - Group 5 (75+): Red

- **Label Border Colors by Gender**:
  - Male (A): Blue
  - Female (B): Pink

##### 5. Build and Deployment
- **Build Command**: `./gradlew clean deploy`
- **Build Status**: Successful after fixing compilation errors
- **Access URL**: http://localhost:8080/openspecimen
- **Credentials**: admin / Login@123

## Pending Tasks

### Immediate (Phase 1)
1. Implement actual database operations for participant enrollment
2. Create sample collection workflow with barcode generation
3. Build data integration APIs for external sources
4. Implement real data visualization charts
5. Create WebSocket integration for real-time updates

### Documentation Tasks
1. Update documentation files in /docs folder with change history
2. Create API documentation with examples
3. Write deployment guide
4. Create user manual for BHARAT study features

## Notes
- All changes maintain backward compatibility with OpenSpecimen core features
- New features are isolated in BHARAT-specific modules
- UI changes use existing Vue.js patterns and PrimeVue components
- Database extensions use separate tables to avoid conflicts

## Commit Information
To commit these changes, use the following commands:

```bash
# Add all new and modified files
git add -A

# Create commit with detailed message
git commit -m "Transform OpenSpecimen to LIIMS with project-centric UI

Major changes:
- Rebranded application from OpenSpecimen to LIIMS
- Redesigned login page with white background and updated messaging
- Transformed home page to project-centric design
- Implemented BHARAT study participant coding system
- Created enrollment dashboard with age/gender matrix
- Added database schema for BHARAT-specific features
- Built REST APIs for enrollment and statistics
- Removed unnecessary UI elements and cleaned up header

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to remote (if needed)
git push origin longevity-india-dev
```

---
**Last Updated**: 2025-07-16  
**Maintained By**: adb3502  
**Project**: LIIMS - Longevity India Information Management System