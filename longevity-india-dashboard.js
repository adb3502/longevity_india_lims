// BHARAT Study Dashboard Customizations - Longevity India
// Generated on 2025-06-24 17:04:31

(function() {
    'use strict';
    
    // Age Group Color Mapping (Blue/Teal theme)
    const AGE_GROUP_COLORS = {
        'AG1': '#4CAF50',
        'AG2': '#8BC34A',
        'AG3': '#FF9800',
        'AG4': '#FF5722',
        'AG5': '#9C27B0'
    };
    
    // Visit Stage Colors
    const VISIT_COLORS = {
        'V0': '#4CAF50',
        'V1': '#FF9800',
        'V2': '#FF5722',
        'V3': '#9C27B0'
    };
    
    // Biomarker Category Colors
    const BIOMARKER_COLORS = {
        'genomics': '#2196F3',
        'proteomics': '#9C27B0',
        'metabolomics': '#FF9800',
        'epigenomics': '#4CAF50',
        'inflammation': '#F44336',
        'clinical': '#607D8B'
    };
    
    // Longevity India Primary Colors
    const LI_COLORS = {
        'primary': '#4169E1',
        'secondary': '#20B2AA',
        'accent': '#00CED1'
    };
    
    // Helper Functions
    function addBharatHeroSection() {
        const heroHtml = `
            <div class="bharat-dashboard-hero fade-in">
                <img src="/images/longevity-india-logo.png" alt="Longevity India" style="height: 60px; margin-bottom: 20px;">
                <h1>BHARAT Study Dashboard</h1>
                <p>Biomarkers of Healthy Aging, Resilience, Adversity, and Transitions</p>
            </div>
        `;
        
        const dashboardContainer = document.querySelector('.os-main-content') || document.querySelector('.main-content');
        if (dashboardContainer) {
            dashboardContainer.insertAdjacentHTML('afterbegin', heroHtml);
        }
    }
    
    function styleAgeGroupBadges() {
        document.querySelectorAll('[data-age-group]').forEach(element => {
            const ageGroup = element.getAttribute('data-age-group');
            const color = AGE_GROUP_COLORS[ageGroup];
            if (color) {
                element.style.backgroundColor = color;
                element.style.color = 'white';
                element.classList.add('age-group-badge');
            }
        });
    }
    
    function styleVisitIndicators() {
        document.querySelectorAll('[data-visit]').forEach(element => {
            const visit = element.getAttribute('data-visit');
            const color = VISIT_COLORS[visit];
            if (color) {
                element.style.color = color;
                element.style.fontWeight = '600';
            }
        });
    }
    
    function styleBiomarkerCategories() {
        document.querySelectorAll('[data-biomarker-category]').forEach(element => {
            const category = element.getAttribute('data-biomarker-category');
            const color = BIOMARKER_COLORS[category];
            if (color) {
                element.style.borderLeft = `4px solid ${color}`;
                element.style.paddingLeft = '12px';
            }
        });
    }
    
    function initializeCharts() {
        // Age group distribution chart
        const ageGroupData = {
            labels: ['AG1 (20-30)', 'AG2 (31-40)', 'AG3 (41-50)', 'AG4 (51-60)', 'AG5 (61-70)'],
            datasets: [{
                data: [120, 135, 140, 125, 110],
                backgroundColor: Object.values(AGE_GROUP_COLORS),
                borderWidth: 0
            }]
        };
        
        // Visit completion chart
        const visitData = {
            labels: ['Baseline (V0)', '6 Months (V1)', '12 Months (V2)', '24 Months (V3)'],
            datasets: [{
                data: [630, 615, 580, 425],
                backgroundColor: Object.values(VISIT_COLORS),
                borderWidth: 0
            }]
        };
        
        // Initialize charts if Chart.js is available
        if (typeof Chart !== 'undefined') {
            const ageGroupCanvas = document.getElementById('age-group-chart');
            const visitCanvas = document.getElementById('visit-chart');
            
            if (ageGroupCanvas) {
                new Chart(ageGroupCanvas, {
                    type: 'doughnut',
                    data: ageGroupData,
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            },
                            title: {
                                display: true,
                                text: 'Participant Distribution by Age Group'
                            }
                        }
                    }
                });
            }
            
            if (visitCanvas) {
                new Chart(visitCanvas, {
                    type: 'bar',
                    data: visitData,
                    options: {
                        responsive: true,
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
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
        }
    }
    
    function addCustomQuickStats() {
        const quickStatsHtml = `
            <div class="row quick-stats-row" style="margin-bottom: 30px;">
                <div class="col-md-3">
                    <div class="card text-center" style="border-radius: 12px;">
                        <div class="card-body">
                            <div style="color: #4CAF50; font-size: 2.5rem; margin-bottom: 10px;">
                                <i class="fa fa-users"></i>
                            </div>
                            <h3 style="color: #4CAF50;">630</h3>
                            <p class="text-muted">Total Participants</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center" style="border-radius: 12px;">
                        <div class="card-body">
                            <div style="color: #2196F3; font-size: 2.5rem; margin-bottom: 10px;">
                                <i class="fa fa-vial"></i>
                            </div>
                            <h3 style="color: #2196F3;">2,847</h3>
                            <p class="text-muted">Samples Collected</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center" style="border-radius: 12px;">
                        <div class="card-body">
                            <div style="color: #FF9800; font-size: 2.5rem; margin-bottom: 10px;">
                                <i class="fa fa-microscope"></i>
                            </div>
                            <h3 style="color: #FF9800;">1,932</h3>
                            <p class="text-muted">Analyses Complete</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-center" style="border-radius: 12px;">
                        <div class="card-body">
                            <div style="color: #9C27B0; font-size: 2.5rem; margin-bottom: 10px;">
                                <i class="fa fa-calendar-check"></i>
                            </div>
                            <h3 style="color: #9C27B0;">2,250</h3>
                            <p class="text-muted">Visits Completed</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const mainContent = document.querySelector('.os-main-content') || document.querySelector('.main-content');
        if (mainContent) {
            const heroSection = mainContent.querySelector('.bharat-dashboard-hero');
            if (heroSection) {
                heroSection.insertAdjacentHTML('afterend', quickStatsHtml);
            }
        }
    }
    
    // Mobile responsive menu toggle
    function initializeMobileMenu() {
        const menuToggle = document.createElement('button');
        menuToggle.className = 'mobile-menu-toggle';
        menuToggle.innerHTML = '<i class="fa fa-bars"></i>';
        menuToggle.style.cssText = `
            display: none;
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            padding: 10px;
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
        `;
        
        const header = document.querySelector('.os-header') || document.querySelector('.navbar-header');
        if (header) {
            header.appendChild(menuToggle);
            header.style.position = 'relative';
        }
        
        // Show/hide on mobile
        const mediaQuery = window.matchMedia('(max-width: 768px)');
        function handleMobileView(e) {
            if (e.matches) {
                menuToggle.style.display = 'block';
            } else {
                menuToggle.style.display = 'none';
            }
        }
        
        mediaQuery.addListener(handleMobileView);
        handleMobileView(mediaQuery);
        
        // Toggle sidebar
        menuToggle.addEventListener('click', function() {
            const sidebar = document.querySelector('.os-left-nav') || document.querySelector('.sidebar');
            if (sidebar) {
                sidebar.classList.toggle('show');
            }
        });
    }
    
    // Update header logo to use Longevity India logo
    function updateHeaderLogo() {
        const logoElements = document.querySelectorAll('.navbar-brand img, .os-logo');
        logoElements.forEach(logo => {
            logo.src = '/images/longevity-india-logo.png';
            logo.alt = 'Longevity India - BHARAT Study';
            logo.style.height = '40px';
            logo.style.maxHeight = '40px';
        });
        
        // Update favicon
        const favicon = document.querySelector('link[rel="icon"], link[rel="shortcut icon"]');
        if (favicon) {
            favicon.href = '/images/longevity-india-favicon.ico';
        } else {
            const newFavicon = document.createElement('link');
            newFavicon.rel = 'icon';
            newFavicon.href = '/images/longevity-india-favicon.ico';
            document.head.appendChild(newFavicon);
        }
    }
    
    // Update page title
    function updatePageTitle() {
        document.title = 'BHARAT Study Portal - Longevity India';
        
        const titleElements = document.querySelectorAll('h1, .page-title, .navbar-brand');
        titleElements.forEach(el => {
            if (el.classList.contains('navbar-brand') && !el.querySelector('img')) {
                el.textContent = 'BHARAT Study Portal';
            }
        });
    }
    
    // Apply Longevity India color scheme to existing elements
    function applyLongevityColors() {
        // Update any existing primary color elements
        const primaryElements = document.querySelectorAll('.btn-primary, .bg-primary, .text-primary');
        primaryElements.forEach(el => {
            if (el.classList.contains('btn-primary')) {
                el.style.backgroundColor = LI_COLORS.primary;
                el.style.borderColor = LI_COLORS.primary;
            }
            if (el.classList.contains('bg-primary')) {
                el.style.backgroundColor = LI_COLORS.primary;
            }
            if (el.classList.contains('text-primary')) {
                el.style.color = LI_COLORS.primary;
            }
        });
        
        // Update header background
        const headers = document.querySelectorAll('.os-header, .navbar-header');
        headers.forEach(header => {
            header.style.backgroundColor = LI_COLORS.primary;
        });
    }
    
    // Initialize all customizations
    function init() {
        console.log('Initializing Longevity India - BHARAT Study customizations...');
        
        // Add custom styles
        const existingTheme = document.getElementById('longevity-india-theme');
        if (!existingTheme) {
            const link = document.createElement('link');
            link.id = 'longevity-india-theme';
            link.rel = 'stylesheet';
            link.href = '/longevity-india-theme.css';
            document.head.appendChild(link);
        }
        
        // Apply customizations
        setTimeout(() => {
            updateHeaderLogo();
            updatePageTitle();
            applyLongevityColors();
            addBharatHeroSection();
            addCustomQuickStats();
            styleAgeGroupBadges();
            styleVisitIndicators();
            styleBiomarkerCategories();
            initializeCharts();
            initializeMobileMenu();
        }, 1000);
    }
    
    // Run on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Re-run on navigation changes (for SPAs)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                setTimeout(init, 500);
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
})();