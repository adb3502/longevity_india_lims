# BHARAT Dashboard & Data Integration Specifications

## Data Integration Architecture

### Current Data Sources
1. **Epicollect** - Clinical metadata
2. **Diagnostic Labs** - Blood test results (CSV/API)
3. **Flow Cytometry** - Immunophenotyping data
4. **OpenSpecimen** - Sample tracking
5. **ODK Collect** - Field collection data (future)

### Data Flow Pipeline
```
Epicollect → API Pull → Parse JSON → Store in os_bharat_integrations → Update Participant Record
Lab APIs → Scheduled Import → Parse Results → Store Raw + Processed → Generate Alerts
Flow Cytometry → File Upload → Parse FCS → Extract Populations → Store Analysis
```

## Dashboard Components

### 1. Main BHARAT Dashboard
**URL**: `/bharat/dashboard`

**Widgets**:
```javascript
// Real-time enrollment statistics
const EnrollmentWidget = {
  totalTarget: 5000,
  currentEnrolled: 1247,
  byAgeGroup: {
    "18-29": { target: 1000, current: 289, male: 145, female: 144 },
    "30-44": { target: 1000, current: 312, male: 156, female: 156 },
    "45-59": { target: 1000, current: 298, male: 149, female: 149 },
    "60-74": { target: 1000, current: 245, male: 122, female: 123 },
    "75+":   { target: 1000, current: 103, male: 51, female: 52 }
  }
};

// Sample inventory status
const SampleInventoryWidget = {
  totalSamples: 3891,
  byType: {
    "Blood EDTA": 1247,
    "Blood SST": 1247,
    "Serum Aliquots": 3741,
    "Plasma Aliquots": 2494,
    "Urine": 1198,
    "Hair": 1156,
    "Cheek Swab": 1247,
    "Stool": 432
  },
  storageUtilization: {
    "-80C Freezer 1": "67%",
    "-80C Freezer 2": "45%",
    "LN2 Tank 1": "78%"
  }
};

// Data completeness tracker
const DataCompletenessWidget = {
  byDataType: {
    "Clinical Metadata": "98%",
    "Blood Results": "89%",
    "Immunophenotyping": "72%",
    "Genomics": "0%", // Not started
    "Proteomics": "0%" // Not started
  }
};
```

### 2. Participant Detail Dashboard
**URL**: `/bharat/participants/{code}/dashboard`

**Components**:

#### Clinical Summary Card
```javascript
const ClinicalSummary = {
  vitals: {
    bloodPressure: "120/80",
    heartRate: 72,
    bmi: 23.5,
    temperature: 98.6
  },
  epicollectData: {
    medications: ["Metformin", "Lisinopril"],
    conditions: ["Type 2 Diabetes", "Hypertension"],
    familyHistory: {
      diabetes: true,
      cancer: false,
      heartDisease: true
    }
  }
};
```

#### Lab Results Visualization
```javascript
// Time series plot for key biomarkers
const LabResultsChart = {
  type: 'line',
  data: {
    labels: ['Baseline', '3 months', '6 months'],
    datasets: [
      { label: 'HbA1c', data: [6.8, 6.5, 6.2] },
      { label: 'LDL', data: [145, 132, 118] },
      { label: 'Creatinine', data: [0.9, 0.9, 1.0] }
    ]
  }
};
```

#### Immunophenotyping Results
```javascript
const ImmuneProfile = {
  tcells: {
    cd4: { percentage: 42.3, absolute: 850 },
    cd8: { percentage: 28.1, absolute: 565 },
    ratio: 1.5
  },
  bcells: { percentage: 12.4, absolute: 249 },
  nkCells: { percentage: 8.7, absolute: 175 }
};
```

### 3. Center-wise Comparison Dashboard
**URL**: `/bharat/centers/compare`

Compare enrollment, sample quality, and data completeness across centers.

## API Endpoints for Dashboard Data

### Enrollment Statistics
```
GET /api/bharat/stats/enrollment
Response: {
  total: 1247,
  byCenter: { "RAM": 450, "VEL": 397, "PGI": 400 },
  byAgeGroup: { ... },
  byGender: { "M": 623, "F": 624 },
  trend: [ { date: "2024-01-01", count: 1050 }, ... ]
}
```

### Sample Inventory
```
GET /api/bharat/stats/inventory
Response: {
  byType: { ... },
  byStorage: { ... },
  pendingProcessing: 47,
  qcFailed: 12
}
```

### Data Completeness
```
GET /api/bharat/stats/completeness
Response: {
  overall: 0.82,
  byDataType: { ... },
  byCenter: { ... },
  missingCritical: [
    { participant: "RAM-1A-023", missing: ["blood_results"] }
  ]
}
```

### Participant Timeline
```
GET /api/bharat/participants/{code}/timeline
Response: [
  { date: "2024-01-15", event: "Enrolled", details: {} },
  { date: "2024-01-15", event: "Samples Collected", details: { types: ["BE", "BS", "U"] } },
  { date: "2024-01-20", event: "Lab Results Received", details: { source: "1MG" } },
  { date: "2024-01-22", event: "Flow Cytometry Completed", details: {} }
]
```

## Visualization Libraries to Use

### For React Components
```javascript
// Chart.js for standard charts
import { Line, Bar, Doughnut } from 'react-chartjs-2';

// D3.js for complex visualizations
import * as d3 from 'd3';

// Heatmap for enrollment matrix
const EnrollmentHeatmap = () => {
  // Use D3 to create age vs gender heatmap
  // Color intensity = completion percentage
};

// Sankey diagram for sample flow
const SampleFlowDiagram = () => {
  // Show flow from collection → processing → storage → analysis
};
```

## Real-time Updates

### WebSocket Integration
```javascript
// Real-time sample tracking
const SampleTracker = () => {
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8080/bharat/updates');
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      // Update dashboard in real-time
      // e.g., new enrollment, sample processed, results received
    };
    
    return () => ws.close();
  }, []);
};
```

## Export Functionality

### Dashboard Reports
```javascript
// Generate PDF report
const exportDashboard = async () => {
  const response = await fetch('/api/bharat/reports/dashboard', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'enrollment_summary',
      format: 'pdf',
      dateRange: { from: '2024-01-01', to: '2024-12-31' }
    })
  });
  
  const blob = await response.blob();
  downloadFile(blob, 'bharat_dashboard_report.pdf');
};
```

## Alerts & Notifications

### Quality Control Alerts
```javascript
const QCAlerts = {
  sampleQuality: {
    trigger: "hemolysis detected",
    action: "Flag sample, notify lab manager"
  },
  dataCompleteness: {
    trigger: "Missing data > 7 days",
    action: "Email reminder to data entry team"
  },
  enrollmentBalance: {
    trigger: "Age/gender group > 10% ahead",
    action: "Alert sampling coordinator"
  }
};
```

## Mobile-Responsive Design

All dashboards should work on tablets for field coordinators:
- Collapsible sidebar navigation
- Touch-friendly controls
- Offline capability for viewing cached data
- Quick actions for common tasks

## Performance Optimization

### Caching Strategy
```javascript
// Cache enrollment stats for 5 minutes
const CACHE_DURATION = 5 * 60 * 1000;
let statsCache = { data: null, timestamp: 0 };

const getEnrollmentStats = async () => {
  if (statsCache.data && Date.now() - statsCache.timestamp < CACHE_DURATION) {
    return statsCache.data;
  }
  
  const data = await fetchEnrollmentStats();
  statsCache = { data, timestamp: Date.now() };
  return data;
};
```

### Pagination for Large Datasets
```javascript
// Paginate participant list
const ParticipantList = () => {
  const [page, setPage] = useState(1);
  const pageSize = 50;
  
  // Load only current page data
  const { data, total } = useParticipants(page, pageSize);
};
```

## Change History

### 2025-07-16 - Initial Dashboard Implementation
- Designed data integration architecture for multiple sources
- Created dashboard component specifications
- Defined API endpoints for dashboard data
- Outlined visualization components using Chart.js and D3.js
- Added real-time WebSocket integration design
- Included export functionality and alert mechanisms
- Ensured mobile-responsive design considerations
- Implemented performance optimization strategies