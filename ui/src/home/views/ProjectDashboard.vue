<template>
  <os-page>
    <os-page-head>
      <span>
        <div class="project-header">
          <div class="project-breadcrumb">
            <os-button text left-icon="arrow-left" label="Projects" @click="backToProjects" />
            <span class="breadcrumb-separator">/</span>
          </div>
          <div class="project-title-section">
            <h3>{{ projectInfo.name }}</h3>
            <p>{{ projectInfo.description }}</p>
          </div>
        </div>
      </span>

      <template #right>
        <div class="project-actions">
          <os-button v-if="projectId === 'bharat-study'" style="margin-right: 0.5rem;" left-icon="users"
            label="Enrollment Dashboard" @click="goToEnrollmentDashboard" />
          <os-button style="margin-right: 0.5rem;" left-icon="cog"
            label="Settings" @click="openProjectSettings" />
          <os-button left-icon="plus"
            label="Add Widget" @click="showAddWidgetDialog" />
        </div>
      </template>
    </os-page-head>

    <os-page-body>
      <div class="dashboard-container">
        <!-- Dashboard Grid -->
        <div class="dashboard-grid">
          <!-- Sample Statistics Widget -->
          <div class="dashboard-widget widget-large">
            <os-card>
              <template #header>
                <div class="widget-header">
                  <h4>Sample Statistics</h4>
                  <os-button size="small" left-icon="expand" @click="expandWidget('sample-stats')" />
                </div>
              </template>
              <template #body>
                <div class="stats-grid">
                  <div class="stat-item">
                    <div class="stat-icon samples-icon">
                      <os-icon name="vial" />
                    </div>
                    <div class="stat-content">
                      <span class="stat-number">{{ projectStats.totalSamples }}</span>
                      <span class="stat-label">Total Samples</span>
                      <span class="stat-change positive">+127 this month</span>
                    </div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-icon participants-icon">
                      <os-icon name="users" />
                    </div>
                    <div class="stat-content">
                      <span class="stat-number">{{ projectStats.totalParticipants }}</span>
                      <span class="stat-label">Participants</span>
                      <span class="stat-change positive">+23 this month</span>
                    </div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-icon storage-icon">
                      <os-icon name="box" />
                    </div>
                    <div class="stat-content">
                      <span class="stat-number">{{ projectStats.storageBoxes }}</span>
                      <span class="stat-label">Storage Boxes</span>
                      <span class="stat-change neutral">+12 this month</span>
                    </div>
                  </div>
                </div>
              </template>
            </os-card>
          </div>

          <!-- Age/Gender Distribution Chart Placeholder -->
          <div class="dashboard-widget widget-medium">
            <os-card>
              <template #header>
                <h4>Age/Gender Distribution</h4>
              </template>
              <template #body>
                <div class="chart-placeholder">
                  <div class="chart-icon">
                    <os-icon name="chart-pie" />
                  </div>
                  <p>Age and gender distribution chart</p>
                  <p class="chart-note">Data visualization will be implemented here</p>
                </div>
              </template>
            </os-card>
          </div>

          <!-- India Map Placeholder -->
          <div class="dashboard-widget widget-medium">
            <os-card>
              <template #header>
                <h4>Sample Collection Map</h4>
              </template>
              <template #body>
                <div class="chart-placeholder">
                  <div class="chart-icon">
                    <os-icon name="map" />
                  </div>
                  <p>India map showing sample collection sites</p>
                  <p class="chart-note">Interactive map will be implemented here</p>
                </div>
              </template>
            </os-card>
          </div>

          <!-- Recent Collections -->
          <div class="dashboard-widget widget-medium">
            <os-card>
              <template #header>
                <h4>Recent Collections</h4>
              </template>
              <template #body>
                <div class="recent-collections">
                  <div class="collection-item" v-for="collection in recentCollections" :key="collection.id">
                    <div class="collection-info">
                      <div class="participant-id">{{ collection.participantId }}</div>
                      <div class="collection-details">
                        <span class="sample-type">{{ collection.sampleType }}</span>
                        <span class="collection-date">{{ formatDate(collection.date) }}</span>
                      </div>
                    </div>
                    <div class="collection-status">
                      <span :class="['status-badge', collection.status.toLowerCase()]">
                        {{ collection.status }}
                      </span>
                    </div>
                  </div>
                </div>
              </template>
            </os-card>
          </div>

          <!-- Storage Overview -->
          <div class="dashboard-widget widget-medium">
            <os-card>
              <template #header>
                <h4>Storage Overview</h4>
              </template>
              <template #body>
                <div class="storage-overview">
                  <div class="storage-location" v-for="location in storageLocations" :key="location.id">
                    <div class="location-header">
                      <h5>{{ location.name }}</h5>
                      <span class="capacity">{{ location.used }}/{{ location.total }}</span>
                    </div>
                    <div class="capacity-bar">
                      <div class="capacity-fill" :style="{ width: location.percentage + '%' }"></div>
                    </div>
                    <div class="location-details">
                      <span class="temperature">{{ location.temperature }}</span>
                      <span class="box-count">{{ location.boxes }} boxes</span>
                    </div>
                  </div>
                </div>
              </template>
            </os-card>
          </div>

          <!-- Sample Tracking -->
          <div class="dashboard-widget widget-large">
            <os-card>
              <template #header>
                <div class="widget-header">
                  <h4>Sample Tracking</h4>
                  <os-button size="small" left-icon="search" label="Advanced Search" />
                </div>
              </template>
              <template #body>
                <div class="sample-tracking">
                  <div class="tracking-search">
                    <os-text-field 
                      v-model="searchQuery" 
                      placeholder="Search by Participant ID, Barcode, or Box Number..." 
                      left-icon="search"
                    />
                  </div>
                  <div class="tracking-results">
                    <div class="sample-row" v-for="sample in filteredSamples" :key="sample.id">
                      <div class="sample-basic-info">
                        <div class="participant-id">{{ sample.participantId }}</div>
                        <div class="barcode">{{ sample.barcode }}</div>
                      </div>
                      <div class="sample-details">
                        <span class="sample-type">{{ sample.type }}</span>
                        <span class="aliquot">Aliquot {{ sample.aliquotNumber }}</span>
                      </div>
                      <div class="storage-info">
                        <span class="box-number">Box {{ sample.boxNumber }}</span>
                        <span class="location">{{ sample.location }}</span>
                      </div>
                      <div class="sample-actions">
                        <os-button size="small" left-icon="eye" @click="viewSample(sample)" />
                        <os-button size="small" left-icon="edit" @click="editSample(sample)" />
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </os-card>
          </div>
        </div>
      </div>
    </os-page-body>

    <!-- Add Widget Dialog -->
    <os-dialog ref="addWidgetDialog">
      <template #header>
        <span>Add Dashboard Widget</span>
      </template>
      <template #content>
        <div class="available-widgets">
          <div class="widget-option" v-for="widget in availableWidgets" :key="widget.id">
            <div class="widget-preview">
              <os-icon :name="widget.icon" />
            </div>
            <div class="widget-info">
              <h5>{{ widget.name }}</h5>
              <p>{{ widget.description }}</p>
            </div>
            <div class="widget-action">
              <os-button size="small" label="Add" @click="addWidget(widget)" />
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <os-button text label="Close" @click="closeAddWidgetDialog" />
      </template>
    </os-dialog>
  </os-page>
</template>

<script>
import routerSvc from '@/common/services/Router.js';

export default {
  name: 'ProjectDashboard',

  props: ['projectId'],

  data() {
    return {
      searchQuery: '',
      
      projectInfo: {
        name: 'BHARAT Study',
        description: 'Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions',
        lead: 'Dr. Ravi Kumar',
        status: 'Active'
      },

      projectStats: {
        totalSamples: 3891,
        totalParticipants: 1247,
        storageBoxes: 156
      },

      recentCollections: [
        {
          id: 1,
          participantId: 'BHARAT-001234',
          sampleType: 'Blood',
          date: new Date(Date.now() - 2 * 60 * 60 * 1000),
          status: 'Processed'
        },
        {
          id: 2,
          participantId: 'BHARAT-001235',
          sampleType: 'Saliva',
          date: new Date(Date.now() - 4 * 60 * 60 * 1000),
          status: 'Collected'
        },
        {
          id: 3,
          participantId: 'BHARAT-001236',
          sampleType: 'Urine',
          date: new Date(Date.now() - 6 * 60 * 60 * 1000),
          status: 'Processing'
        }
      ],

      storageLocations: [
        {
          id: 1,
          name: 'Freezer A (-80°C)',
          used: 1250,
          total: 1500,
          percentage: 83,
          temperature: '-80°C',
          boxes: 45
        },
        {
          id: 2,
          name: 'Freezer B (-20°C)', 
          used: 890,
          total: 1200,
          percentage: 74,
          temperature: '-20°C',
          boxes: 32
        },
        {
          id: 3,
          name: 'Refrigerator (4°C)',
          used: 340,
          total: 500,
          percentage: 68,
          temperature: '4°C',
          boxes: 18
        }
      ],

      sampleData: [
        {
          id: 1,
          participantId: 'BHARAT-001234',
          barcode: 'BH-001234-BL-001',
          type: 'Blood',
          aliquotNumber: '001',
          boxNumber: 'B-156',
          location: 'Freezer-A'
        },
        {
          id: 2,
          participantId: 'BHARAT-001235',
          barcode: 'BH-001235-SA-002', 
          type: 'Saliva',
          aliquotNumber: '002',
          boxNumber: 'S-089',
          location: 'Freezer-B'
        },
        {
          id: 3,
          participantId: 'BHARAT-001236',
          barcode: 'BH-001236-UR-003',
          type: 'Urine',
          aliquotNumber: '003',
          boxNumber: 'U-045',
          location: 'Refrigerator'
        }
      ],

      availableWidgets: [
        {
          id: 'quality-control',
          name: 'Quality Control',
          description: 'Sample quality metrics and alerts',
          icon: 'shield-check'
        },
        {
          id: 'data-export',
          name: 'Data Export',
          description: 'Export and download project data',
          icon: 'download'
        },
        {
          id: 'compliance',
          name: 'Compliance Monitor',
          description: 'Regulatory compliance tracking',
          icon: 'clipboard-check'
        }
      ]
    }
  },

  computed: {
    filteredSamples() {
      if (!this.searchQuery) {
        return this.sampleData;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.sampleData.filter(sample => 
        sample.participantId.toLowerCase().includes(query) ||
        sample.barcode.toLowerCase().includes(query) ||
        sample.boxNumber.toLowerCase().includes(query)
      );
    }
  },

  created() {
    // Load project-specific data based on projectId
    this.loadProjectData();
  },

  methods: {
    loadProjectData() {
      // TODO: Load actual project data from API
      console.log('Loading data for project:', this.projectId);
      
      // Update project info based on projectId
      if (this.projectId === 'organ-aging') {
        this.projectInfo = {
          name: 'Organ Aging Project',
          description: 'Comprehensive study of organ-specific aging biomarkers and interventions',
          lead: 'Dr. Priya Sharma',
          status: 'Active'
        };
        this.projectStats = {
          totalSamples: 2347,
          totalParticipants: 892,
          storageBoxes: 89
        };
      } else if (this.projectId === 'cognitive-health') {
        this.projectInfo = {
          name: 'Cognitive Health Study',
          description: 'Longitudinal study of cognitive aging and neurodegeneration biomarkers',
          lead: 'Dr. Anil Reddy',
          status: 'Planning'
        };
        this.projectStats = {
          totalSamples: 0,
          totalParticipants: 0,
          storageBoxes: 0
        };
      }
    },

    backToProjects() {
      routerSvc.goto('HomePage');
    },

    openProjectSettings() {
      // TODO: Implement project settings
      console.log('Opening project settings');
    },

    showAddWidgetDialog() {
      this.$refs.addWidgetDialog.open();
    },

    closeAddWidgetDialog() {
      this.$refs.addWidgetDialog.close();
    },

    addWidget(widget) {
      // TODO: Implement widget addition
      console.log('Adding widget:', widget);
      this.closeAddWidgetDialog();
    },

    expandWidget(widgetType) {
      // TODO: Implement widget expansion
      console.log('Expanding widget:', widgetType);
    },

    viewSample(sample) {
      // TODO: Implement sample view
      console.log('Viewing sample:', sample);
    },

    editSample(sample) {
      // TODO: Implement sample edit
      console.log('Editing sample:', sample);
    },

    formatDate(date) {
      return new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
        Math.floor((date - new Date()) / (1000 * 60 * 60)), 'hour'
      );
    },

    goToEnrollmentDashboard() {
      routerSvc.goto('BharatEnrollment');
    }
  }
}
</script>

<style scoped>
.project-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.project-breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.breadcrumb-separator {
  color: #6b7280;
  font-size: 0.875rem;
}

.project-title-section h3 {
  margin: 0 0 0.25rem 0;
  color: #1f2937;
}

.project-title-section p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.project-actions {
  display: flex;
  align-items: center;
}

.dashboard-container {
  padding: 1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}

.dashboard-widget {
  border-radius: 8px;
  overflow: hidden;
}

.widget-large {
  grid-column: span 6;
}

.widget-medium {
  grid-column: span 4;
}

.widget-small {
  grid-column: span 3;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.widget-header h4 {
  margin: 0;
  font-weight: 600;
  color: #1f2937;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.samples-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.participants-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.storage-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.stat-change {
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.stat-change.positive {
  color: #10b981;
}

.stat-change.neutral {
  color: #6b7280;
}

.chart-placeholder {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.chart-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.chart-note {
  font-size: 0.75rem;
  font-style: italic;
  margin-top: 0.5rem;
}

.recent-collections {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.collection-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 6px;
}

.participant-id {
  font-weight: 600;
  color: #1f2937;
}

.collection-details {
  display: flex;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.processed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.collected {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.processing {
  background: #fef3c7;
  color: #92400e;
}

.storage-overview {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.storage-location {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 6px;
}

.location-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.location-header h5 {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
}

.capacity {
  font-size: 0.75rem;
  color: #6b7280;
}

.capacity-bar {
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.capacity-fill {
  height: 100%;
  background: #3b82f6;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.location-details {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #6b7280;
}

.sample-tracking {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tracking-search {
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.tracking-results {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sample-row {
  display: grid;
  grid-template-columns: 2fr 2fr 2fr 1fr;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 6px;
}

.sample-basic-info .participant-id {
  font-weight: 600;
  color: #1f2937;
}

.sample-basic-info .barcode {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.sample-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sample-details .sample-type {
  font-weight: 500;
  color: #1f2937;
}

.sample-details .aliquot {
  font-size: 0.75rem;
  color: #6b7280;
}

.storage-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.storage-info .box-number {
  font-weight: 500;
  color: #1f2937;
}

.storage-info .location {
  font-size: 0.75rem;
  color: #6b7280;
}

.sample-actions {
  display: flex;
  gap: 0.25rem;
  justify-content: flex-end;
}

.available-widgets {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.widget-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.widget-preview {
  width: 48px;
  height: 48px;
  background: #f3f4f6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: #6b7280;
}

.widget-info {
  flex: 1;
}

.widget-info h5 {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: #1f2937;
}

.widget-info p {
  margin: 0;
  font-size: 0.875rem;
  color: #6b7280;
}

@media (max-width: 1200px) {
  .widget-large {
    grid-column: span 12;
  }
  
  .widget-medium {
    grid-column: span 6;
  }
}

@media (max-width: 768px) {
  .dashboard-widget {
    grid-column: span 12;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .sample-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}
</style>