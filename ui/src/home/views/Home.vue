<template>
  <os-page>
    <os-page-head>
      <span>
        <h3>Projects Dashboard</h3>
        <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">Select a project to access its data and analytics</p>
      </span>

      <template #right>
        <os-button style="margin-top: -0.5rem;" left-icon="plus"
          label="New Project" @click="showNewProjectDialog" />
      </template>
    </os-page-head>

    <os-page-body>
      <div class="projects-container">
        <!-- Project Cards Grid -->
        <div class="projects-grid">
          <!-- BHARAT Study Project -->
          <div class="project-card" @click="navigateToProject('bharat-study')">
            <div class="project-card-header bharat-theme">
              <div class="project-icon">
                <os-icon name="dna" />
              </div>
              <div class="project-status active">
                <span class="status-dot"></span>
                Active
              </div>
            </div>
            <div class="project-card-body">
              <h3>BHARAT Study</h3>
              <p>Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions</p>
              <div class="project-stats">
                <div class="stat">
                  <span class="stat-value">1,247</span>
                  <span class="stat-label">Participants</span>
                </div>
                <div class="stat">
                  <span class="stat-value">3,891</span>
                  <span class="stat-label">Samples</span>
                </div>
                <div class="stat">
                  <span class="stat-value">156</span>
                  <span class="stat-label">Active Boxes</span>
                </div>
              </div>
              <div class="project-progress">
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 73%"></div>
                </div>
                <span class="progress-text">73% Complete</span>
              </div>
            </div>
            <div class="project-card-footer">
              <div class="last-activity">
                <os-icon name="clock" />
                Last updated 2 hours ago
              </div>
              <div class="project-lead">
                <os-icon name="user" />
                Dr. Ravi Kumar
              </div>
            </div>
          </div>

          <!-- Organ Aging Project -->
          <div class="project-card" @click="navigateToProject('organ-aging')">
            <div class="project-card-header organ-theme">
              <div class="project-icon">
                <os-icon name="heart" />
              </div>
              <div class="project-status active">
                <span class="status-dot"></span>
                Active
              </div>
            </div>
            <div class="project-card-body">
              <h3>Organ Aging Project</h3>
              <p>Comprehensive study of organ-specific aging biomarkers and interventions</p>
              <div class="project-stats">
                <div class="stat">
                  <span class="stat-value">892</span>
                  <span class="stat-label">Participants</span>
                </div>
                <div class="stat">
                  <span class="stat-value">2,347</span>
                  <span class="stat-label">Samples</span>
                </div>
                <div class="stat">
                  <span class="stat-value">89</span>
                  <span class="stat-label">Active Boxes</span>
                </div>
              </div>
              <div class="project-progress">
                <div class="progress-bar">
                  <div class="progress-fill organ-progress" style="width: 45%"></div>
                </div>
                <span class="progress-text">45% Complete</span>
              </div>
            </div>
            <div class="project-card-footer">
              <div class="last-activity">
                <os-icon name="clock" />
                Last updated 1 day ago
              </div>
              <div class="project-lead">
                <os-icon name="user" />
                Dr. Priya Sharma
              </div>
            </div>
          </div>

          <!-- Cognitive Health Study -->
          <div class="project-card" @click="navigateToProject('cognitive-health')">
            <div class="project-card-header cognitive-theme">
              <div class="project-icon">
                <os-icon name="brain" />
              </div>
              <div class="project-status planning">
                <span class="status-dot"></span>
                Planning
              </div>
            </div>
            <div class="project-card-body">
              <h3>Cognitive Health Study</h3>
              <p>Longitudinal study of cognitive aging and neurodegeneration biomarkers</p>
              <div class="project-stats">
                <div class="stat">
                  <span class="stat-value">0</span>
                  <span class="stat-label">Participants</span>
                </div>
                <div class="stat">
                  <span class="stat-value">0</span>
                  <span class="stat-label">Samples</span>
                </div>
                <div class="stat">
                  <span class="stat-value">0</span>
                  <span class="stat-label">Active Boxes</span>
                </div>
              </div>
              <div class="project-progress">
                <div class="progress-bar">
                  <div class="progress-fill cognitive-progress" style="width: 15%"></div>
                </div>
                <span class="progress-text">15% Setup Complete</span>
              </div>
            </div>
            <div class="project-card-footer">
              <div class="last-activity">
                <os-icon name="clock" />
                Created 1 week ago
              </div>
              <div class="project-lead">
                <os-icon name="user" />
                Dr. Anil Reddy
              </div>
            </div>
          </div>

          <!-- Add New Project Card -->
          <div class="project-card add-project-card" @click="showNewProjectDialog">
            <div class="add-project-content">
              <div class="add-project-icon">
                <os-icon name="plus" />
              </div>
              <h3>Create New Project</h3>
              <p>Set up a new research project with sample collection protocols</p>
            </div>
          </div>
        </div>

        <!-- Quick Actions Panel -->
        <div class="quick-actions-panel">
          <h4>Quick Actions</h4>
          <div class="quick-actions-grid">
            <div class="quick-action-item" @click="quickAction('add-participant')">
              <os-icon name="user-plus" />
              <span>Add Participant</span>
            </div>
            <div class="quick-action-item" @click="quickAction('sample-collection')">
              <os-icon name="vial" />
              <span>Collect Sample</span>
            </div>
            <div class="quick-action-item" @click="quickAction('storage-management')">
              <os-icon name="box" />
              <span>Manage Storage</span>
            </div>
            <div class="quick-action-item" @click="quickAction('generate-report')">
              <os-icon name="chart" />
              <span>Generate Report</span>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="recent-activity-panel">
          <h4>Recent Activity</h4>
          <div class="activity-list">
            <div class="activity-item">
              <div class="activity-icon bharat-bg">
                <os-icon name="vial" />
              </div>
              <div class="activity-content">
                <div class="activity-title">Blood sample collected - BHARAT-001234</div>
                <div class="activity-meta">BHARAT Study • 2 hours ago • Dr. Kumar</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon organ-bg">
                <os-icon name="user-plus" />
              </div>
              <div class="activity-content">
                <div class="activity-title">New participant enrolled - OAP-000567</div>
                <div class="activity-meta">Organ Aging Project • 5 hours ago • Dr. Sharma</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon bharat-bg">
                <os-icon name="box" />
              </div>
              <div class="activity-content">
                <div class="activity-title">Storage box B-156 moved to Freezer-A</div>
                <div class="activity-meta">BHARAT Study • 1 day ago • Lab Tech</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </os-page-body>

    <!-- New Project Dialog -->
    <os-dialog ref="newProjectDialog">
      <template #header>
        <span>Create New Project</span>
      </template>
      <template #content>
        <os-form ref="newProjectForm" :schema="newProjectSchema" :data="newProjectData" />
      </template>
      <template #footer>
        <os-button text label="Cancel" @click="closeNewProjectDialog" />
        <os-button primary label="Create Project" @click="createProject" />
      </template>
    </os-dialog>
  </os-page>
</template>

<script>
import routerSvc from '@/common/services/Router.js';

import http from '@/common/services/HttpClient.js';

export default {
  name: 'HomePage',

  data() {
    return {
      newProjectData: {
        name: '',
        description: '',
        type: '',
        lead: '',
        startDate: new Date()
      },
      
      newProjectSchema: {
        layout: {
          rows: [
            {
              fields: [
                {
                  type: 'text',
                  name: 'name',
                  placeholder: 'Project Name',
                  validations: { required: { message: 'Project name is required' } }
                }
              ]
            },
            {
              fields: [
                {
                  type: 'textarea',
                  name: 'description',
                  placeholder: 'Project Description',
                  rows: 3
                }
              ]
            },
            {
              fields: [
                {
                  type: 'dropdown',
                  name: 'type',
                  placeholder: 'Project Type',
                  listSource: {
                    options: [
                      { value: 'aging', label: 'Aging Research' },
                      { value: 'biomarker', label: 'Biomarker Discovery' },
                      { value: 'clinical', label: 'Clinical Study' },
                      { value: 'longitudinal', label: 'Longitudinal Study' }
                    ],
                    displayProp: 'label',
                    selectProp: 'value'
                  }
                }
              ]
            },
            {
              fields: [
                {
                  type: 'text',
                  name: 'lead',
                  placeholder: 'Principal Investigator'
                }
              ]
            }
          ]
        }
      }
    }
  },

  async created() {
    // Load real statistics from API
    await this.loadEnrollmentStats();
    await this.loadInventoryStats();
  },

  methods: {
    async loadEnrollmentStats() {
      try {
        const stats = await http.get('bharat/stats/enrollment');
        // Update project stats based on API response
        if (stats && stats.total) {
          // Update BHARAT Study stats
          const bharatProject = this.projects.find(p => p.id === 'bharat-study');
          if (bharatProject) {
            bharatProject.stats.participants = stats.total;
            // Update age group stats if available
            if (stats.byAgeGroup) {
              bharatProject.stats.byAgeGroup = stats.byAgeGroup;
            }
          }
        }
      } catch (error) {
        console.error('Failed to load enrollment stats:', error);
      }
    },

    async loadInventoryStats() {
      try {
        const stats = await http.get('bharat/stats/inventory');
        // Update inventory stats
        if (stats && stats.byType) {
          const bharatProject = this.projects.find(p => p.id === 'bharat-study');
          if (bharatProject && stats.byType['Blood EDTA']) {
            bharatProject.stats.samples = Object.values(stats.byType).reduce((sum, count) => sum + count, 0);
            bharatProject.stats.boxes = Math.ceil(bharatProject.stats.samples / 100); // Estimate boxes
          }
        }
      } catch (error) {
        console.error('Failed to load inventory stats:', error);
      }
    },
    navigateToProject(projectId) {
      // Navigate to project-specific dashboard
      routerSvc.goto('ProjectDashboard', { projectId });
    },

    showNewProjectDialog() {
      this.$refs.newProjectDialog.open();
    },

    closeNewProjectDialog() {
      this.$refs.newProjectDialog.close();
    },

    createProject() {
      if (!this.$refs.newProjectForm.validate()) {
        return;
      }
      
      // TODO: Implement project creation logic
      console.log('Creating project:', this.newProjectData);
      this.closeNewProjectDialog();
      
      // Reset form
      this.newProjectData = {
        name: '',
        description: '',
        type: '',
        lead: '',
        startDate: new Date()
      };
    },

    quickAction(action) {
      switch(action) {
        case 'add-participant':
          routerSvc.goto('ParticipantRegistration');
          break;
        case 'sample-collection':
          routerSvc.goto('SampleCollection');
          break;
        case 'storage-management':
          routerSvc.goto('StorageManagement');
          break;
        case 'generate-report':
          routerSvc.goto('ReportsGeneration');
          break;
      }
    }
  }
}
</script>

<style scoped>
.projects-container {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.project-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #e0e0e0;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.project-card-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  position: relative;
}

.bharat-theme {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.organ-theme {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.cognitive-theme {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.project-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.project-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4ade80;
}

.project-status.planning .status-dot {
  background: #fbbf24;
}

.project-card-body {
  padding: 1.5rem;
}

.project-card-body h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.project-card-body p {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

.project-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.project-progress {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #667eea;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.organ-progress {
  background: #f5576c;
}

.cognitive-progress {
  background: #4facfe;
}

.progress-text {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.project-card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: #6b7280;
}

.last-activity, .project-lead {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.add-project-card {
  border: 2px dashed #d1d5db;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-project-card:hover {
  border-color: #667eea;
  background: #f0f4ff;
}

.add-project-content {
  text-align: center;
  padding: 2rem;
}

.add-project-icon {
  font-size: 3rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.add-project-card:hover .add-project-icon {
  color: #667eea;
}

.add-project-content h3 {
  margin: 0 0 0.5rem 0;
  color: #374151;
}

.add-project-content p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.quick-actions-panel, .recent-activity-panel {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-actions-panel h4, .recent-activity-panel h4 {
  margin: 0 0 1rem 0;
  color: #1f2937;
  font-weight: 600;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.quick-action-item {
  padding: 1rem;
  text-align: center;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #fafafa;
}

.quick-action-item:hover {
  background: #f0f4ff;
  border-color: #667eea;
  color: #667eea;
}

.quick-action-item .os-icon-wrapper {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.quick-action-item span {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: #f9fafb;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

.bharat-bg {
  background: #667eea;
}

.organ-bg {
  background: #f5576c;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.activity-meta {
  font-size: 0.75rem;
  color: #6b7280;
}

@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>