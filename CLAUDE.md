# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenSpecimen is a web-based biobanking informatics platform for managing biological specimens in research and clinical settings. It's a multi-tier enterprise application with dual frontend architecture (AngularJS legacy + Vue.js modern) and a comprehensive Java backend.

## Technology Stack

**Backend:**
- Java 16 with Spring Framework 5.3.22
- Hibernate 5.6.11 with Envers for audit trails
- Spring Security 5.7.3 (supports SAML)
- Liquibase 4.8.0 for database migrations
- AspectJ 1.9.19 for AOP
- MySQL database (Oracle also supported)

**Frontend:**
- Vue.js 3.4.6 with PrimeVue UI components (active development - `/ui` directory)
- AngularJS 1.8.2 (legacy - `/www` directory)

**Build Tools:**
- Gradle for Java build
- npm/Vue CLI for Vue.js
- Grunt for AngularJS

## Common Development Commands

### Build Commands
```bash
# Full build (compiles Java, builds both frontends, creates WAR)
./gradlew build

# Environment-specific builds
./gradlew build -Penv=dev    # Development (default)
./gradlew build -Penv=prod   # Production
./gradlew build -Penv=test   # Test

# Deploy to local Tomcat (development only)
./gradlew deploy

# Clean build artifacts
./gradlew clean
```

### Test Commands
```bash
# Run Java unit tests
./gradlew test

# Compile test classes
./gradlew testClasses
```

### Frontend Development

**Vue.js (active development):**
```bash
cd ui
npm install                  # Install dependencies
npm run serve               # Development server with hot-reload
npm run build              # Production build
npm run lint               # ESLint code checking
```

**AngularJS (legacy):**
```bash
cd www
npm install && bower install  # Install dependencies
grunt serve                   # Development server
grunt build                  # Production build
```

## Project Architecture

### Directory Structure
```
/
├── WEB-INF/src/com/krishagni/catissueplus/
│   ├── core/                # Business logic modules
│   │   ├── administrative/  # Users, sites, containers
│   │   ├── biospecimen/     # Specimens, participants, protocols
│   │   ├── audit/           # Audit trail functionality
│   │   ├── auth/            # Authentication/authorization
│   │   ├── de/              # Dynamic extensions (forms)
│   │   └── query/           # Query engine
│   └── rest/                # REST API controllers
├── ui/                      # Vue.js frontend (modern)
├── www/                     # AngularJS frontend (legacy)
├── WEB-INF/resources/
│   ├── db/                  # Liquibase database migrations
│   └── email-templates/     # Email notification templates
└── build.properties         # Build/deployment configuration
```

### Architecture Patterns
- **Layered Architecture**: Controllers → Services → Domain → Repository/DAO
- **Domain-Driven Design**: Rich domain models with aggregates (CollectionProtocol, Specimen)
- **Repository Pattern**: DAO interfaces with criteria-based queries
- **AOP**: Transaction management, audit logging, attribute change tracking
- **Plugin Architecture**: Extensible through plugins and dynamic forms
- **Event-Driven**: Domain events for decoupling (SpecimenSavedEvent, OrderSavedEvent)

### Key Modules
1. **Specimen Management**: Collection protocols, participant registration, specimen lifecycle
2. **Distribution**: Distribution protocols, order management, shipment tracking
3. **Administrative**: User/role management, sites, container types
4. **Data Collection**: Dynamic forms designer, custom fields, query builder
5. **Integration**: REST APIs, bulk import/export, barcode printing

## Database Configuration

- Primary database: MySQL (configured via JNDI: `jdbc/openspecimen`)
- Data directory: `/opt/tomcat9/os-data` (configurable in `build.properties`)
- Schema management: Liquibase migrations in `WEB-INF/resources/db/`
- Multi-tenant support with data isolation

## Development Notes

### Frontend Development Status
- **Vue.js** (`/ui`) is the active development path - use this for new features
- **AngularJS** (`/www`) is legacy but still maintained
- Both frontends are built as part of the main gradle build process

### Code Quality
- Vue.js: ESLint configured with Vue 3 essential rules
- Java: AspectJ weaving during compilation
- No specific Java linting tools configured

### Testing
- Integration tests located in `/WEB-INF/integration-test/`
- Test data as XML files for different modules
- Limited unit test coverage - focus is on integration testing
- H2 in-memory database for test scenarios

### Build Process
- Requires Java 16
- AspectJ weaving occurs during compilation
- Frontend builds are integrated into main gradle build
- Outputs WAR file for Tomcat deployment

### Configuration Files
- `build.properties`: Environment-specific build configuration
- `WEB-INF/resources/`: Application configuration and resources
- Multiple Spring contexts for different concerns (main, REST API, plugins)