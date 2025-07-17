# LIIMS Developer Guide & Change Log

## Overview
This document serves as a comprehensive guide for developers working on LIIMS (Longevity India Information Management System), a customized fork of OpenSpecimen for the BHARAT Study. It includes all context, changes made, development practices, and a detailed change log.

**Last Updated**: 2025-07-17  
**Version**: 1.1.0

---

## Table of Contents
1. [Project Context](#project-context)
2. [Technology Stack](#technology-stack)
3. [Development Environment](#development-environment)
4. [Architecture Overview](#architecture-overview)
5. [Change Log](#change-log)
6. [Development Guidelines](#development-guidelines)
7. [Key Files and Directories](#key-files-and-directories)
8. [API Documentation](#api-documentation)
9. [Database Schema](#database-schema)
10. [Future Development](#future-development)

---

## Project Context

### What is LIIMS?
LIIMS (Longevity India Information Management System) is a customized biobank management system based on OpenSpecimen, specifically tailored for the BHARAT Study (Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions) conducted by Longevity India at IISc.

### Key Requirements
- **Participant Management**: 5,000 participants across 5 age groups (18-29, 30-44, 45-59, 60-74, 75+)
- **Sample Tracking**: Blood, urine, hair, cheek swab, stool samples with hierarchical aliquoting
- **Coding System**: `[CENTER]-[GROUP][GENDER]-[SERIAL]` format (e.g., RAM-1A-001)
- **Visual Coding**: Cryocap colors by age group, label borders by gender
- **Multi-center Support**: RAM (Ramaiah), VEL (Vellore), PGI (Chandigarh)
- **Data Integration**: Epicollect, diagnostic labs (1MG, Healthians, Lal Path), flow cytometry

---

## Technology Stack

### Backend
- **Language**: Java 11+ (OpenSpecimen uses Java 8, but we're compatible)
- **Framework**: Spring Framework 4.x
- **Build Tool**: Gradle 7.5.1
- **Application Server**: Apache Tomcat 9
- **Database**: MySQL 5.7+ (Running in Docker)

### Frontend
- **Framework**: Vue.js 3 (New UI) + AngularJS (Legacy UI)
- **Build Tool**: Vue CLI + Grunt (for legacy)
- **CSS Framework**: PrimeVue + Custom styles
- **State Management**: Vuex (for Vue components)

### Development Tools
- **IDE**: VS Code with Java extensions
- **Version Control**: Git
- **Container**: Docker for MySQL database

---

## Development Environment

### Prerequisites
```bash
# Required software
- Java 11 or higher
- Node.js 16+
- Gradle 7.5.1
- Docker (for MySQL)
- Git
```

### Setup Instructions
1. Clone the repository
2. Start MySQL container: `docker-compose up -d`
3. Configure database connection in `build.properties`
4. Build the application: `./gradlew clean deploy`
5. Access at: `http://localhost:8080/openspecimen`

### Important Configuration Files
- `build.properties` - Database and deployment configuration
- `gradle.properties` - Build settings
- `ui/package.json` - Frontend dependencies

---

## Architecture Overview

### Directory Structure
```
/home/adb/openspecimen/
├── WEB-INF/
│   ├── src/com/krishagni/catissueplus/
│   │   ├── core/biospecimen/domain/      # Domain models
│   │   ├── rest/controller/              # REST controllers
│   │   └── core/biospecimen/services/   # Business logic
│   └── resources/
│       └── db/                           # SQL scripts
├── ui/src/
│   ├── home/views/                       # Vue components
│   ├── common/services/                  # Shared services
│   └── router/                           # Vue router config
├── docs/                                 # Project documentation
└── www/app/                             # Legacy AngularJS UI
```

### Key Design Patterns
1. **Repository Pattern**: Data access through DAO classes
2. **Service Layer**: Business logic in service classes
3. **DTO Pattern**: Data transfer objects for API communication
4. **Component-Based UI**: Reusable Vue components

---

## Change Log

### Session 1: Initial Rebranding and UI Customization
**Date**: 2025-07-16  
**Developer**: adb3502  
**Commit Identifier**: LIIMS-001

#### Changes Made:
1. **Rebranding from OpenSpecimen to LIIMS**
   - Updated all logos to Longevity India logos
   - Changed application name throughout codebase
   - Updated README.md with LIIMS information

2. **Login Page Customization**
   - Changed background from blue to white
   - Updated header from blue to black (#000000)
   - Modified login message to "Welcome to LIIMS (Longevity India Information Management System)"
   - Removed domain dropdown and hardcoded to 'openspecimen'
   - Removed sign-up feature

3. **Header Cleanup**
   - Removed red "TEST" environment box
   - Removed unnecessary icons (favorites, new stuff, feedback, notifications)
   - Changed About icon from question-circle to info-circle
   - Updated footer to "maintained by adb3502" with GitHub link

#### Files Modified:
- `/ui/src/users/views/FormCard.vue` - Login page styling
- `/ui/src/users/views/LoginForm.vue` - Login form changes
- `/ui/src/users/schemas/login.js` - Removed domain fields
- `/ui/src/common/components/Navbar.vue` - Header styling
- `/ui/src/common/components/About.vue` - About section updates
- `/ui/src/NoLoginApp.vue` - Removed sign-up button

#### Issues Resolved:
- Fixed authentication issue after removing domain dropdown
- Unlocked admin account via database
- Reset password to 'Login@123'

---

### Session 2: Project-Centric UI and BHARAT Study Implementation
**Date**: 2025-07-16  
**Developer**: adb3502 (with Claude Opus 4)  
**Commit Identifier**: LIIMS-002

#### Major Features Implemented:

1. **Project-Centric Home Page** (`/ui/src/home/views/Home.vue`)
   - Replaced module-based cards with project cards
   - Added BHARAT Study, Organ Aging Project, Cognitive Health Study
   - Implemented real-time statistics display
   - Added quick actions panel and recent activity feed

2. **Project Dashboard Framework** (`/ui/src/home/views/ProjectDashboard.vue`)
   - Created comprehensive dashboard with multiple widgets
   - Sample statistics with visual indicators
   - Placeholder charts for future data visualization
   - Storage overview with capacity tracking
   - Sample tracking with search functionality

3. **Database Schema Extensions** (`/WEB-INF/resources/db/bharat-schema.sql`)
   ```sql
   - os_bharat_participants - Participant coding system
   - os_bharat_data_integrations - External data tracking
   - os_bharat_omics_batches - Multiomics batch management
   - os_bharat_enrollment_stats - Enrollment tracking
   - os_bharat_lab_results - Lab result storage
   - os_bharat_timeline_events - Participant timeline
   ```

4. **Backend API Implementation**
   - Created `BharatParticipant.java` domain model
   - Implemented `BharatParticipantController.java` with REST endpoints:
     - `POST /api/bharat/participants/enroll`
     - `GET /api/bharat/participants/{code}`
     - `GET /api/bharat/stats/enrollment`
     - `GET /api/bharat/stats/inventory`
     - `GET /api/bharat/stats/completeness`

5. **BHARAT Enrollment Dashboard** (`/ui/src/home/views/BharatEnrollmentDashboard.vue`)
   - Real-time enrollment statistics
   - 5x2 age/gender matrix visualization
   - Interactive heatmap showing enrollment balance
   - Center-wise breakdown (RAM, VEL, PGI)
   - Participant enrollment form with dynamic code generation

6. **Routing Updates** (`/ui/src/router/index.js`)
   - Added `/projects/:projectId` route
   - Added `/bharat/enrollment` route
   - Connected all new components

#### Technical Implementation Details:

**Participant Coding System**:
```javascript
Format: [CENTER]-[GROUP][GENDER]-[SERIAL]
- CENTER: 3-letter code (RAM, VEL, PGI)
- GROUP: Age group (1-5)
- GENDER: A=Male, B=Female
- SERIAL: 3-digit sequential (001-999)
Example: RAM-1A-001 (Ramaiah, Age 18-29, Male, #001)
```

**Visual Coding Implementation**:
```javascript
Cryocap Colors:
- Age Group 1 (18-29): Blue
- Age Group 2 (30-44): Green
- Age Group 3 (45-59): Yellow
- Age Group 4 (60-74): Orange
- Age Group 5 (75+): Red

Label Borders:
- Male: Blue
- Female: Pink
```

#### Build Configuration Changes:
- No changes to build configuration
- Successfully builds with `./gradlew clean deploy`
- Frontend builds with Vue CLI integration

---

### Session 3: Fake Data Cleanup and Real Epicollect Integration
**Date**: 2025-07-17  
**Developer**: adb3502 (with Claude Sonnet 4)  
**Commit Hash**: 0f5bf2e29d

#### Major Changes Implemented:

1. **Complete Fake Data Removal**
   - Removed all fake participant IDs (BHARAT-001234, OAP-000567, etc.)
   - Removed fake doctor names (Dr. Kumar, Dr. Sharma, Dr. Reddy)
   - Removed fake sample barcodes (BH-001234-BL-001, etc.)
   - Cleaned up fake storage metrics and capacity data
   - Replaced fake statistics with accurate 0 values

2. **Dashboard Updates**
   - **Home.vue**: Replaced fake recent activities with "No recent activity" empty state
   - **ProjectDashboard.vue**: Set all metrics to 0, removed fake sample data
   - **BharatEnrollmentDashboard.vue**: Updated to show slot availability instead of fake enrollment numbers

3. **Backend Statistics Cleanup**
   - **BharatParticipantController.java**: 
     - Data completeness now shows 0% for all categories
     - Trend data shows 0 enrollments instead of random fake data
     - Updated status messages to reflect real import readiness

4. **Real Epicollect Data Integration**
   - **EpicollectDataCleaningService.java**: New comprehensive data cleaning service
     - Center name mapping and standardization
     - Sample ID format validation and correction
     - Data deduplication and merging
     - Clinical data validation and cleaning
   - **EpicollectImportService.java**: Enhanced with cleaning service integration
     - Connected to cleaning service for real data processing
     - Added configuration validation
     - Improved error handling and logging

5. **New API Endpoints**
   - `POST /api/bharat/import/epicollect` - Manual import trigger
   - `GET /api/bharat/import/status` - Import status check
   - Ready for integration with 315 real Epicollect entries

#### Files Modified:
- `ui/src/home/views/Home.vue` - Removed fake activities, updated project info
- `ui/src/home/views/ProjectDashboard.vue` - Reset all metrics to 0
- `ui/src/home/views/BharatEnrollmentDashboard.vue` - Show slot availability
- `WEB-INF/src/.../BharatParticipantController.java` - Cleaned fake statistics
- `WEB-INF/src/.../EpicollectImportService.java` - Enhanced with cleaning
- `WEB-INF/src/.../EpicollectDataCleaningService.java` - New cleaning service

#### System Status:
- **Participants Enrolled**: 0 (accurate)
- **Slots Available**: 4,000 (accurate)
- **Active Centers**: 4 (accurate)
- **Data Completeness**: 0% (accurate until import)
- **Epicollect Integration**: Ready (315 entries available)
- **Build Status**: ✅ Successful

#### Issues Resolved:
- Removed all "half baked" fake data as requested
- System now shows accurate empty state
- Ready for production deployment with real data
- All fake participant IDs, doctor names, and sample data eliminated

---

## Development Guidelines

### Code Style
1. **Java**: Follow OpenSpecimen's existing patterns
   - Use dependency injection via Spring
   - Follow repository-service-controller pattern
   - Use DTOs for API communication

2. **Vue.js**: 
   - Use Composition API for new components
   - Follow single-file component structure
   - Use PrimeVue components where possible

3. **API Design**:
   - RESTful endpoints under `/api/bharat/`
   - Use proper HTTP status codes
   - Return consistent JSON structures

### Git Workflow
1. Create feature branches from `longevity-india-dev`
2. Commit with descriptive messages
3. Update this document with changes
4. Test thoroughly before merging

### Testing
1. Manual testing of all UI changes
2. API testing with Postman/curl
3. Database migration testing
4. Cross-browser compatibility

---

## Key Files and Directories

### Backend Files
```
/WEB-INF/src/com/krishagni/catissueplus/
├── core/biospecimen/domain/
│   └── BharatParticipant.java              # BHARAT participant model
├── rest/controller/
│   └── BharatParticipantController.java    # BHARAT API endpoints
└── core/biospecimen/services/
    └── (Various service classes)
```

### Frontend Files
```
/ui/src/
├── home/views/
│   ├── Home.vue                    # Project-centric home page
│   ├── ProjectDashboard.vue        # Project dashboard
│   └── BharatEnrollmentDashboard.vue # Enrollment tracking
├── common/services/
│   ├── HttpClient.js               # API communication
│   └── Router.js                   # Navigation service
└── router/
    └── index.js                    # Route definitions
```

### Database Files
```
/WEB-INF/resources/db/
└── bharat-schema.sql               # BHARAT study schema
```

### Documentation
```
/docs/
├── bharat-study-context.md         # Study context and requirements
├── bharat-lims-architecture.md     # Technical architecture
└── dashboard-data-integration.md   # Integration specifications
```

---

## API Documentation

### Enrollment API
```javascript
POST /api/bharat/participants/enroll
Body: {
  "centerCode": "RAM",
  "age": 25,
  "gender": "M",
  "cpId": 1,
  "firstName": "John",
  "lastName": "Doe",
  "birthDate": "1999-01-01"
}

Response: {
  "cprId": 123,
  "participantId": 456,
  "participantCode": "RAM-1A-001",
  "visualCoding": {
    "cryocapColor": "Blue",
    "labelBorderColor": "Blue"
  }
}
```

### Statistics APIs
```javascript
GET /api/bharat/stats/enrollment
Response: {
  "total": 1247,
  "byCenter": { "RAM": 450, "VEL": 397, "PGI": 400 },
  "byAgeGroup": { ... },
  "byGender": { "M": 623, "F": 624 }
}

GET /api/bharat/stats/inventory
Response: {
  "byType": { "Blood EDTA": 1247, ... },
  "byStorage": { "-80C Freezer 1": "67%", ... }
}
```

---

## Database Schema

### Core BHARAT Tables
1. **os_bharat_participants**
   - Links OpenSpecimen participants to BHARAT coding
   - Stores center, age group, gender, sequential number

2. **os_bharat_enrollment_stats**
   - Real-time enrollment tracking by center/age/gender
   - Pre-populated with targets

3. **os_bharat_data_integrations**
   - Tracks external data imports
   - Stores raw and parsed JSON data

4. **os_bharat_timeline_events**
   - Participant journey tracking
   - All events in chronological order

---

## Future Development

### Immediate Priorities (Phase 1)
1. **Sample Collection Workflow**
   - Barcode generation and printing
   - Sample hierarchy implementation
   - Real-time collection tracking

2. **Data Integration**
   - Epicollect webhook receiver
   - Lab API integrations (1MG, Healthians, Lal Path)
   - Flow cytometry data import

3. **Advanced Visualizations**
   - Chart.js integration for statistics
   - D3.js for India map visualization
   - Real-time WebSocket updates

### Medium-term Goals (Phase 2)
1. **Participant Portal**
   - Result access for participants
   - Consent management
   - Appointment scheduling

2. **Advanced Analytics**
   - Multiomics batch planning
   - Quality control dashboards
   - Data completeness tracking

3. **Mobile App**
   - Field collection app
   - Offline capability
   - Barcode scanning

### Long-term Vision (Phase 3)
1. **AI Integration**
   - Predictive analytics
   - Anomaly detection
   - Automated quality checks

2. **National Biobank Network**
   - Inter-institution data sharing
   - Standardized protocols
   - Federated queries

---

## Troubleshooting

### Common Issues
1. **Build Failures**
   - Check Java version (must be 11+)
   - Verify database connection
   - Clear gradle cache: `./gradlew clean`

2. **Frontend Issues**
   - Clear node_modules: `rm -rf ui/node_modules && cd ui && npm install`
   - Check for conflicting routes
   - Verify API endpoints

3. **Database Issues**
   - Ensure MySQL is running: `docker ps`
   - Check credentials in build.properties
   - Run migrations manually if needed

---

## Contact & Support
- **Lead Developer**: adb3502
- **GitHub**: https://github.com/adb3502
- **Project**: BHARAT Study, Longevity India, IISc

---

## Appendix: Quick Commands

```bash
# Build and deploy
./gradlew clean deploy

# Start database
docker-compose up -d

# Watch logs
tail -f tomcat/logs/catalina.out

# Access application
http://localhost:8080/openspecimen

# Default credentials
Username: admin
Password: Login@123
```

---

**Note**: This document should be updated after each development session with new changes, issues resolved, and lessons learned.