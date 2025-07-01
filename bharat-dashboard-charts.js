
// BHARAT Study Dashboard Charts and Interactivity
// Generated on 2025-06-24 17:16:05

// Chart.js configuration and data
const chartColors = {
    ageGroups: ['#4CAF50', '#8BC34A', '#FF9800', '#FF5722', '#9C27B0'],
    visits: ['#4CAF50', '#FF9800', '#FF5722', '#9C27B0'],
    primary: '#4169E1',
    secondary: '#20B2AA',
    accent: '#00CED1'
};

let charts = {};

// Initialize all charts when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeEnrollmentChart();
    initializeAgeGroupChart();
    initializeVisitChart();
    loadDashboardData();
    setInterval(updateDashboard, 300000); // Update every 5 minutes
});

function initializeEnrollmentChart() {
    const ctx = document.getElementById('enrollmentChart').getContext('2d');
    charts.enrollment = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['AG1 (20-30)', 'AG2 (31-40)', 'AG3 (41-50)', 'AG4 (51-60)', 'AG5 (61-70)'],
            datasets: [{
                label: 'Enrolled',
                data: [126, 126, 126, 126, 126],
                backgroundColor: chartColors.ageGroups,
                borderWidth: 0
            }, {
                label: 'Target',
                data: [126, 126, 126, 126, 126],
                backgroundColor: 'rgba(255, 255, 255, 0.3)',
                borderColor: chartColors.ageGroups,
                borderWidth: 2,
                type: 'line'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Enrollment by Age Group'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 150
                }
            }
        }
    });
}

function initializeAgeGroupChart() {
    const ctx = document.getElementById('ageGroupChart').getContext('2d');
    charts.ageGroup = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['AG1 (20-30)', 'AG2 (31-40)', 'AG3 (41-50)', 'AG4 (51-60)', 'AG5 (61-70)'],
            datasets: [{
                data: [126, 126, 126, 126, 126],
                backgroundColor: chartColors.ageGroups,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Current Distribution'
                }
            }
        }
    });
}

function initializeVisitChart() {
    const ctx = document.getElementById('visitChart').getContext('2d');
    charts.visit = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Baseline (V0)', '6 Months (V1)', '12 Months (V2)', '24 Months (V3)'],
            datasets: [{
                label: 'Completed',
                data: [630, 615, 580, 425],
                backgroundColor: chartColors.visits,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Visit Completion Status'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 700
                }
            }
        }
    });
}

// Data loading and refresh functions
async function loadDashboardData() {
    try {
        // Simulate API calls - replace with actual OpenSpecimen API calls
        updateEnrollmentMetrics();
        updateCollectionMetrics();
        updateAlerts();
        console.log('Dashboard data loaded successfully');
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showAlert('Error loading dashboard data', 'error');
    }
}

function updateEnrollmentMetrics() {
    // Simulate real-time enrollment data
    const metrics = {
        totalEnrolled: 630,
        enrollmentRate: '100%',
        ageGroupData: [126, 126, 126, 126, 126]
    };
    
    document.getElementById('totalEnrolled').textContent = metrics.totalEnrolled;
    document.getElementById('enrollmentRate').textContent = metrics.enrollmentRate;
    
    // Update charts
    if (charts.enrollment) {
        charts.enrollment.data.datasets[0].data = metrics.ageGroupData;
        charts.enrollment.update();
    }
    
    if (charts.ageGroup) {
        charts.ageGroup.data.datasets[0].data = metrics.ageGroupData;
        charts.ageGroup.update();
    }
}

function updateCollectionMetrics() {
    // Simulate collection metrics
    const metrics = {
        samplesCollected: 2847,
        samplesProcessed: 2156,
        analysesComplete: 1932,
        qcPassRate: '94.2%'
    };
    
    document.getElementById('samplesCollected').textContent = metrics.samplesCollected.toLocaleString();
    document.getElementById('samplesProcessed').textContent = metrics.samplesProcessed.toLocaleString();
    document.getElementById('analysesComplete').textContent = metrics.analysesComplete.toLocaleString();
    document.getElementById('qcPassRate').textContent = metrics.qcPassRate;
}

function updateAlerts() {
    const alertContainer = document.getElementById('alertContainer');
    
    // Check for enrollment alerts
    const enrollmentRate = 100; // Percentage
    if (enrollmentRate >= 95) {
        showAlert('🎉 Excellent! Enrollment target achieved across all age groups.', 'success');
    } else if (enrollmentRate < 80) {
        showAlert('⚠️ Enrollment below target in some age groups. Consider outreach strategies.', 'warning');
    }
    
    // Check QC alerts
    const qcPassRate = 94.2;
    if (qcPassRate < 90) {
        showAlert('🔍 QC pass rate below 90%. Please review laboratory procedures.', 'error');
    }
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-banner ${type}`;
    alertDiv.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; font-size: 1.2rem; cursor: pointer;">&times;</button>
    `;
    alertContainer.appendChild(alertDiv);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.remove();
        }
    }, 10000);
}

// Refresh functions for individual widgets
function refreshEnrollment() {
    console.log('Refreshing enrollment data...');
    updateEnrollmentMetrics();
    showAlert('📊 Enrollment data refreshed', 'success');
}

function refreshAgeGroups() {
    console.log('Refreshing age group data...');
    updateEnrollmentMetrics();
    showAlert('👥 Age group data refreshed', 'success');
}

function refreshVisits() {
    console.log('Refreshing visit data...');
    // Update visit chart with fresh data
    const visitData = [630, 615, 580, 425];
    if (charts.visit) {
        charts.visit.data.datasets[0].data = visitData;
        charts.visit.update();
    }
    
    // Update visit progress bars
    updateVisitProgress(visitData);
    showAlert('📅 Visit data refreshed', 'success');
}

function updateVisitProgress(data) {
    const progressContainer = document.getElementById('visitProgress');
    if (!progressContainer) return;
    
    const visits = ['V0', 'V1', 'V2', 'V3'];
    const totalParticipants = 630;
    
    progressContainer.innerHTML = '';
    
    visits.forEach((visit, index) => {
        const completed = data[index];
        const percentage = Math.round((completed / totalParticipants) * 100);
        
        const progressDiv = document.createElement('div');
        progressDiv.innerHTML = `
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 5px;">
                <span>${visit}</span>
                <span>${completed}/${totalParticipants} (${percentage}%)</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${percentage}%;"></div>
            </div>
        `;
        progressContainer.appendChild(progressDiv);
    });
}

function refreshCollection() {
    console.log('Refreshing collection metrics...');
    updateCollectionMetrics();
    showAlert('🧪 Collection metrics refreshed', 'success');
}

function refreshGeography() {
    console.log('Refreshing geographic data...');
    showAlert('🗺️ Geographic data refreshed', 'success');
}

// Navigation functions
function openBiomarkerDashboard() {
    window.location.href = '/bharat-biomarker-analytics-dashboard.html';
}

function openCollectionDashboard() {
    window.location.href = '/bharat-collection-metrics-dashboard.html';
}

function openQualityDashboard() {
    window.location.href = '/bharat-quality-control-dashboard.html';
}

function exportDashboard() {
    console.log('Exporting dashboard...');
    
    // Generate export data
    const exportData = {
        timestamp: new Date().toISOString(),
        enrollment: {
            total: 630,
            byAgeGroup: {
                AG1: 126,
                AG2: 126, 
                AG3: 126,
                AG4: 126,
                AG5: 126
            }
        },
        visits: {
            V0: 630,
            V1: 615,
            V2: 580,
            V3: 425
        },
        samples: {
            collected: 2847,
            processed: 2156,
            analyzed: 1932
        }
    };
    
    // Create and download CSV
    const csv = convertToCSV(exportData);
    downloadCSV(csv, `bharat-study-overview-${new Date().toISOString().split('T')[0]}.csv`);
    
    showAlert('📥 Dashboard data exported successfully', 'success');
}

function convertToCSV(data) {
    let csv = 'Metric,Value\n';
    csv += `Total Enrollment,${data.enrollment.total}\n`;
    Object.entries(data.enrollment.byAgeGroup).forEach(([ageGroup, count]) => {
        csv += `${ageGroup} Enrollment,${count}\n`;
    });
    Object.entries(data.visits).forEach(([visit, count]) => {
        csv += `${visit} Completion,${count}\n`;
    });
    csv += `Samples Collected,${data.samples.collected}\n`;
    csv += `Samples Processed,${data.samples.processed}\n`;
    csv += `Samples Analyzed,${data.samples.analyzed}\n`;
    return csv;
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Auto-update dashboard every 5 minutes
function updateDashboard() {
    console.log('Auto-updating dashboard...');
    loadDashboardData();
    document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
}

// Real-time notifications (WebSocket simulation)
function initializeRealTimeUpdates() {
    // Simulate real-time updates
    setInterval(() => {
        // Random chance of new enrollment
        if (Math.random() < 0.1) {
            showAlert('🎉 New participant enrolled!', 'success');
            updateEnrollmentMetrics();
        }
        
        // Random chance of completed analysis
        if (Math.random() < 0.2) {
            showAlert('🧪 New analysis completed', 'info');
            updateCollectionMetrics();
        }
    }, 30000); // Check every 30 seconds
}

// Initialize real-time updates
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initializeRealTimeUpdates, 2000);
});
