<template>
  <os-page>
    <os-page-head>
      <span>
        <h3>BHARAT Study Enrollment Dashboard</h3>
        <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">
          Real-time enrollment tracking and balance monitoring
        </p>
      </span>

      <template #right>
        <os-button left-icon="download" label="Export Report" @click="exportReport" />
        <os-button primary left-icon="user-plus" label="Enroll Participant" @click="enrollParticipant" />
      </template>
    </os-page-head>

    <os-page-body>
      <div class="enrollment-dashboard">
        <!-- Summary Statistics -->
        <div class="summary-cards">
          <div class="stat-card total">
            <div class="stat-icon">
              <os-icon name="users" />
            </div>
            <div class="stat-content">
              <h2>{{ stats.total }}</h2>
              <p>Total Enrolled</p>
              <div class="progress">
                <div class="progress-bar" :style="{ width: totalProgress + '%' }"></div>
              </div>
              <span class="progress-text">{{ totalProgress }}% of 5,000 target</span>
            </div>
          </div>

          <div class="stat-card today">
            <div class="stat-icon">
              <os-icon name="calendar-day" />
            </div>
            <div class="stat-content">
              <h2>{{ stats.todayCount }}</h2>
              <p>Enrolled Today</p>
              <span class="trend" :class="{ positive: stats.todayTrend > 0 }">
                <os-icon :name="stats.todayTrend > 0 ? 'arrow-up' : 'arrow-down'" />
                {{ Math.abs(stats.todayTrend) }}% vs yesterday
              </span>
            </div>
          </div>

          <div class="stat-card balance">
            <div class="stat-icon">
              <os-icon name="balance-scale" />
            </div>
            <div class="stat-content">
              <h2>{{ genderBalance }}%</h2>
              <p>Gender Balance</p>
              <div class="gender-bar">
                <div class="male-bar" :style="{ width: malePercentage + '%' }"></div>
                <div class="female-bar" :style="{ width: femalePercentage + '%' }"></div>
              </div>
              <div class="gender-labels">
                <span class="male">Male: {{ stats.byGender.M }}</span>
                <span class="female">Female: {{ stats.byGender.F }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Enrollment Matrix -->
        <div class="enrollment-matrix-container">
          <h4>Enrollment by Age Group and Gender</h4>
          <div class="enrollment-matrix">
            <table>
              <thead>
                <tr>
                  <th>Age Group</th>
                  <th>Male Target</th>
                  <th>Male Enrolled</th>
                  <th>Female Target</th>
                  <th>Female Enrolled</th>
                  <th>Total Progress</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="group in ageGroups" :key="group.name">
                  <td class="age-group">{{ group.name }}</td>
                  <td class="target">{{ group.maleTarget }}</td>
                  <td class="enrolled">
                    <span :class="getEnrollmentClass(group.maleEnrolled, group.maleTarget)">
                      {{ group.maleEnrolled }}
                    </span>
                  </td>
                  <td class="target">{{ group.femaleTarget }}</td>
                  <td class="enrolled">
                    <span :class="getEnrollmentClass(group.femaleEnrolled, group.femaleTarget)">
                      {{ group.femaleEnrolled }}
                    </span>
                  </td>
                  <td>
                    <div class="progress-cell">
                      <div class="progress-bar-small">
                        <div class="progress-fill" :style="{ width: group.progress + '%' }"></div>
                      </div>
                      <span class="progress-percentage">{{ group.progress }}%</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Visual Heatmap -->
          <div class="enrollment-heatmap">
            <h5>Enrollment Heatmap</h5>
            <div class="heatmap-grid">
              <div class="heatmap-row" v-for="group in ageGroups" :key="group.name">
                <div class="age-label">{{ group.name }}</div>
                <div 
                  class="heatmap-cell male" 
                  :style="{ backgroundColor: getHeatmapColor(group.maleEnrolled, group.maleTarget) }"
                  @click="showDetails(group.name, 'M')"
                >
                  <span>M: {{ group.maleEnrolled }}</span>
                </div>
                <div 
                  class="heatmap-cell female" 
                  :style="{ backgroundColor: getHeatmapColor(group.femaleEnrolled, group.femaleTarget) }"
                  @click="showDetails(group.name, 'F')"
                >
                  <span>F: {{ group.femaleEnrolled }}</span>
                </div>
              </div>
            </div>
            <div class="heatmap-legend">
              <span>0%</span>
              <div class="gradient"></div>
              <span>100%</span>
            </div>
          </div>
        </div>

        <!-- Center-wise Breakdown -->
        <div class="center-breakdown">
          <h4>Enrollment by Center</h4>
          <div class="center-cards">
            <div class="center-card" v-for="center in centers" :key="center.code">
              <h5>{{ center.name }} ({{ center.code }})</h5>
              <div class="center-stats">
                <div class="center-total">
                  <span class="number">{{ center.enrolled }}</span>
                  <span class="label">Total</span>
                </div>
                <div class="center-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: center.progress + '%' }"></div>
                  </div>
                  <span>{{ center.progress }}% of {{ center.target }}</span>
                </div>
              </div>
              <div class="center-actions">
                <os-button size="small" text label="View Details" @click="viewCenterDetails(center.code)" />
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Enrollments -->
        <div class="recent-enrollments">
          <h4>Recent Enrollments</h4>
          <div class="enrollments-list">
            <div class="enrollment-item" v-for="enrollment in recentEnrollments" :key="enrollment.code">
              <div class="participant-info">
                <span class="participant-code">{{ enrollment.code }}</span>
                <span class="participant-details">
                  {{ enrollment.ageGroup }} years, {{ enrollment.gender }}
                </span>
              </div>
              <div class="enrollment-meta">
                <span class="center">{{ enrollment.center }}</span>
                <span class="time">{{ formatTime(enrollment.enrolledAt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </os-page-body>

    <!-- Enrollment Dialog -->
    <os-dialog ref="enrollDialog">
      <template #header>
        <span>Enroll New Participant</span>
      </template>
      <template #content>
        <os-form ref="enrollForm" :schema="enrollSchema" :data="enrollData" />
      </template>
      <template #footer>
        <os-button text label="Cancel" @click="closeEnrollDialog" />
        <os-button primary label="Enroll" @click="submitEnrollment" />
      </template>
    </os-dialog>
  </os-page>
</template>

<script>
import http from '@/common/services/HttpClient.js';
import alertSvc from '@/common/services/Alerts.js';

export default {
  name: 'BharatEnrollmentDashboard',

  data() {
    return {
      stats: {
        total: 0,
        todayCount: 0,
        todayTrend: 0,
        byGender: { M: 0, F: 0 },
        byAgeGroup: {}
      },

      ageGroups: [
        { name: '18-29', maleTarget: 500, maleEnrolled: 0, femaleTarget: 500, femaleEnrolled: 0, progress: 0 },
        { name: '30-44', maleTarget: 500, maleEnrolled: 0, femaleTarget: 500, femaleEnrolled: 0, progress: 0 },
        { name: '45-59', maleTarget: 500, maleEnrolled: 0, femaleTarget: 500, femaleEnrolled: 0, progress: 0 },
        { name: '60-74', maleTarget: 500, maleEnrolled: 0, femaleTarget: 500, femaleEnrolled: 0, progress: 0 },
        { name: '75+', maleTarget: 500, maleEnrolled: 0, femaleTarget: 500, femaleEnrolled: 0, progress: 0 }
      ],

      centers: [
        { code: 'RAM', name: 'Ramaiah Hospital', target: 1667, enrolled: 0, progress: 0 },
        { code: 'VEL', name: 'Vellore Hospital', target: 1667, enrolled: 0, progress: 0 },
        { code: 'PGI', name: 'PGI Chandigarh', target: 1666, enrolled: 0, progress: 0 }
      ],

      recentEnrollments: [],

      enrollData: {
        centerCode: '',
        firstName: '',
        lastName: '',
        birthDate: '',
        age: null,
        gender: '',
        cpId: -1 // Will be set based on selected project
      },

      enrollSchema: {
        layout: {
          rows: [
            {
              fields: [
                {
                  type: 'dropdown',
                  name: 'centerCode',
                  placeholder: 'Select Center',
                  validations: { required: { message: 'Center is required' } },
                  listSource: {
                    options: [
                      { value: 'RAM', label: 'Ramaiah Hospital' },
                      { value: 'VEL', label: 'Vellore Hospital' },
                      { value: 'PGI', label: 'PGI Chandigarh' }
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
                  name: 'firstName',
                  placeholder: 'First Name',
                  validations: { required: { message: 'First name is required' } }
                },
                {
                  type: 'text',
                  name: 'lastName',
                  placeholder: 'Last Name',
                  validations: { required: { message: 'Last name is required' } }
                }
              ]
            },
            {
              fields: [
                {
                  type: 'datePicker',
                  name: 'birthDate',
                  placeholder: 'Birth Date',
                  validations: { required: { message: 'Birth date is required' } }
                },
                {
                  type: 'number',
                  name: 'age',
                  placeholder: 'Age',
                  validations: { 
                    required: { message: 'Age is required' },
                    min: { value: 18, message: 'Must be 18 or older' }
                  }
                }
              ]
            },
            {
              fields: [
                {
                  type: 'radio',
                  name: 'gender',
                  placeholder: 'Gender',
                  validations: { required: { message: 'Gender is required' } },
                  listSource: {
                    options: [
                      { value: 'M', label: 'Male' },
                      { value: 'F', label: 'Female' }
                    ],
                    displayProp: 'label',
                    selectProp: 'value'
                  }
                }
              ]
            }
          ]
        }
      },

      refreshInterval: null
    };
  },

  computed: {
    totalProgress() {
      return Math.round((this.stats.total / 5000) * 100);
    },

    genderBalance() {
      const total = this.stats.byGender.M + this.stats.byGender.F;
      if (total === 0) return 50;
      return Math.round(Math.min(this.stats.byGender.M, this.stats.byGender.F) / total * 100 * 2);
    },

    malePercentage() {
      const total = this.stats.byGender.M + this.stats.byGender.F;
      return total > 0 ? Math.round((this.stats.byGender.M / total) * 100) : 50;
    },

    femalePercentage() {
      const total = this.stats.byGender.M + this.stats.byGender.F;
      return total > 0 ? Math.round((this.stats.byGender.F / total) * 100) : 50;
    }
  },

  async created() {
    await this.loadStats();
    // Refresh stats every 30 seconds
    this.refreshInterval = setInterval(() => this.loadStats(), 30000);
  },

  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },

  methods: {
    async loadStats() {
      try {
        const stats = await http.get('bharat/stats/enrollment');
        this.stats = stats;

        // Update age groups
        if (stats.byAgeGroup) {
          this.ageGroups.forEach(group => {
            const data = stats.byAgeGroup[group.name];
            if (data) {
              group.maleEnrolled = data.male || 0;
              group.femaleEnrolled = data.female || 0;
              group.progress = Math.round(((group.maleEnrolled + group.femaleEnrolled) / (group.maleTarget + group.femaleTarget)) * 100);
            }
          });
        }

        // Update centers
        if (stats.byCenter) {
          this.centers.forEach(center => {
            center.enrolled = stats.byCenter[center.code] || 0;
            center.progress = Math.round((center.enrolled / center.target) * 100);
          });
        }

        // Load recent enrollments
        await this.loadRecentEnrollments();
      } catch (error) {
        console.error('Failed to load enrollment stats:', error);
      }
    },

    async loadRecentEnrollments() {
      // TODO: Implement API call to get recent enrollments
      // For now, use dummy data
      this.recentEnrollments = [
        { code: 'RAM-1A-001', ageGroup: '25', gender: 'Male', center: 'RAM', enrolledAt: new Date() },
        { code: 'VEL-2B-045', ageGroup: '38', gender: 'Female', center: 'VEL', enrolledAt: new Date(Date.now() - 3600000) },
        { code: 'PGI-3A-023', ageGroup: '52', gender: 'Male', center: 'PGI', enrolledAt: new Date(Date.now() - 7200000) }
      ];
    },

    getEnrollmentClass(enrolled, target) {
      const percentage = (enrolled / target) * 100;
      if (percentage >= 100) return 'over-enrolled';
      if (percentage >= 90) return 'near-target';
      if (percentage >= 70) return 'on-track';
      if (percentage >= 50) return 'progressing';
      return 'behind';
    },

    getHeatmapColor(enrolled, target) {
      const percentage = Math.min((enrolled / target) * 100, 100);
      // Generate color from red (0%) to green (100%)
      const hue = (percentage * 120) / 100; // 0 = red, 120 = green
      return `hsl(${hue}, 70%, 50%)`;
    },

    showDetails(ageGroup, gender) {
      // TODO: Show detailed participant list for this age group and gender
      console.log('Show details for', ageGroup, gender);
    },

    viewCenterDetails(centerCode) {
      // TODO: Navigate to center-specific view
      console.log('View center details:', centerCode);
    },

    enrollParticipant() {
      this.$refs.enrollDialog.open();
    },

    closeEnrollDialog() {
      this.$refs.enrollDialog.close();
      // Reset form
      this.enrollData = {
        centerCode: '',
        firstName: '',
        lastName: '',
        birthDate: '',
        age: null,
        gender: '',
        cpId: -1
      };
    },

    async submitEnrollment() {
      if (!this.$refs.enrollForm.validate()) {
        return;
      }

      try {
        // TODO: Get actual CP ID for BHARAT study
        this.enrollData.cpId = 1; // Dummy CP ID

        const result = await http.post('bharat/participants/enroll', this.enrollData);
        
        if (result.error) {
          alertSvc.error(result.error);
          return;
        }

        alertSvc.success(`Participant enrolled successfully! Code: ${result.participantCode}`);
        this.closeEnrollDialog();
        
        // Reload stats
        await this.loadStats();
      } catch (error) {
        alertSvc.error('Failed to enroll participant: ' + error.message);
      }
    },

    async exportReport() {
      try {
        // TODO: Implement report export
        alertSvc.info('Report export will be implemented soon');
      } catch (error) {
        alertSvc.error('Failed to export report: ' + error.message);
      }
    },

    formatTime(date) {
      const now = new Date();
      const diff = now - date;
      const hours = Math.floor(diff / 3600000);
      
      if (hours < 1) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} minutes ago`;
      } else if (hours < 24) {
        return `${hours} hours ago`;
      } else {
        const days = Math.floor(hours / 24);
        return `${days} days ago`;
      }
    }
  }
};
</script>

<style scoped>
.enrollment-dashboard {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-card.total .stat-icon {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-card.today .stat-icon {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.stat-card.balance .stat-icon {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.stat-content {
  flex: 1;
}

.stat-content h2 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-content p {
  margin: 0.25rem 0 0.5rem 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.progress {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.75rem;
}

.progress-bar {
  height: 100%;
  background: #667eea;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
  display: block;
}

.trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #dc2626;
}

.trend.positive {
  color: #10b981;
}

.gender-bar {
  display: flex;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.75rem;
}

.male-bar {
  background: #3b82f6;
  transition: width 0.3s ease;
}

.female-bar {
  background: #ec4899;
  transition: width 0.3s ease;
}

.gender-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.75rem;
}

.gender-labels .male {
  color: #3b82f6;
}

.gender-labels .female {
  color: #ec4899;
}

.enrollment-matrix-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.enrollment-matrix-container h4 {
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-weight: 600;
}

.enrollment-matrix table {
  width: 100%;
  border-collapse: collapse;
}

.enrollment-matrix th {
  background: #f9fafb;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

.enrollment-matrix td {
  padding: 0.75rem;
  border-bottom: 1px solid #f3f4f6;
}

.age-group {
  font-weight: 600;
  color: #1f2937;
}

.target {
  color: #6b7280;
}

.enrolled {
  font-weight: 600;
}

.enrolled span {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.enrolled .behind {
  color: #dc2626;
  background: #fee2e2;
}

.enrolled .progressing {
  color: #f59e0b;
  background: #fef3c7;
}

.enrolled .on-track {
  color: #3b82f6;
  background: #dbeafe;
}

.enrolled .near-target {
  color: #10b981;
  background: #d1fae5;
}

.enrolled .over-enrolled {
  color: #7c3aed;
  background: #ede9fe;
}

.progress-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-bar-small {
  flex: 1;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #667eea;
  transition: width 0.3s ease;
}

.progress-percentage {
  font-size: 0.75rem;
  color: #6b7280;
  min-width: 35px;
  text-align: right;
}

.enrollment-heatmap {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.enrollment-heatmap h5 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-weight: 600;
  font-size: 0.875rem;
}

.heatmap-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.heatmap-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.age-label {
  width: 80px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.heatmap-cell {
  flex: 1;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.heatmap-cell:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.heatmap-legend {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.heatmap-legend .gradient {
  flex: 1;
  height: 8px;
  background: linear-gradient(to right, #dc2626, #f59e0b, #10b981);
  border-radius: 4px;
}

.center-breakdown {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.center-breakdown h4 {
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-weight: 600;
}

.center-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.center-card {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.center-card h5 {
  margin: 0 0 1rem 0;
  color: #1f2937;
  font-weight: 600;
}

.center-stats {
  margin-bottom: 1rem;
}

.center-total {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.center-total .number {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

.center-total .label {
  font-size: 0.875rem;
  color: #6b7280;
}

.center-progress {
  font-size: 0.75rem;
  color: #6b7280;
}

.center-progress .progress-bar {
  margin: 0.5rem 0;
}

.recent-enrollments {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.recent-enrollments h4 {
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-weight: 600;
}

.enrollments-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.enrollment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 6px;
}

.participant-info {
  display: flex;
  flex-direction: column;
}

.participant-code {
  font-weight: 600;
  color: #1f2937;
}

.participant-details {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.enrollment-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.enrollment-meta .center {
  padding: 0.25rem 0.5rem;
  background: #e0e7ff;
  color: #4338ca;
  border-radius: 4px;
  font-weight: 500;
}

@media (max-width: 1200px) {
  .summary-cards {
    grid-template-columns: 1fr;
  }

  .center-cards {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .enrollment-dashboard {
    padding: 0.5rem;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
  }

  .heatmap-cell {
    font-size: 0.75rem;
    padding: 0.5rem;
  }
}
</style>