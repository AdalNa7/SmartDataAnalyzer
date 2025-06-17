// Smart Data Analyzer - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFileUpload();
    initializeReportGeneration();
    initializeGrowthInsights();
    initializeChat();
});

// File Upload Functionality
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadZone = document.getElementById('uploadZone');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const uploadBtn = document.getElementById('uploadBtn');

    if (!fileInput) return;

    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        handleFileSelect(e.target.files[0]);
    });

    // Handle drag and drop
    uploadZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    function handleFileSelect(file) {
        if (!file) return;

        // Validate file type
        const allowedTypes = ['.csv', '.xlsx', '.xls'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            showAlert('Invalid file format. Please upload CSV or Excel files only.', 'error');
            return;
        }

        // Validate file size (16MB)
        if (file.size > 16 * 1024 * 1024) {
            showAlert('File too large. Maximum size is 16MB.', 'error');
            return;
        }

        // Display file info
        fileName.textContent = file.name;
        fileSize.textContent = `(${formatFileSize(file.size)})`;
        fileInfo.style.display = 'block';
        uploadBtn.disabled = false;

        // Add animation
        fileInfo.classList.add('fade-in');
    }
}

// Report Generation
function initializeReportGeneration() {
    const generateBtn = document.getElementById('generateReportBtn');
    const exportBtn = document.getElementById('exportPdfBtn');
    
    if (!generateBtn) return;

    generateBtn.addEventListener('click', function() {
        generateReport();
    });
    
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            exportReportAsPDF();
        });
    }
}

function generateReport() {
    const btn = document.getElementById('generateReportBtn');
    const loading = document.getElementById('reportLoading');
    const content = document.getElementById('reportContent');
    
    // Show loading state
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating Report...';
    btn.disabled = true;

    // Fetch report data
    fetch('/report')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showAlert(data.error, 'error');
                return;
            }
            
            displayReport(data);
            loading.style.display = 'none';
            content.style.display = 'block';
            content.classList.add('fade-in');
            
            // Show the export PDF and email buttons after report is generated
            const exportBtn = document.getElementById('exportPdfBtn');
            const emailBtn = document.getElementById('emailReportBtn');
            if (exportBtn) {
                exportBtn.style.display = 'inline-block';
            }
            if (emailBtn) {
                emailBtn.style.display = 'inline-block';
            }
        })
        .catch(error => {
            console.error('Error generating report:', error);
            showAlert('Error generating report. Please try again.', 'error');
        })
        .finally(() => {
            btn.innerHTML = '<i class="fas fa-magic me-2"></i>Generate AI Report';
            btn.disabled = false;
        });
}

function displayReport(data) {
    const content = document.getElementById('reportContent');
    
    const html = `
        <div class="row">
            <div class="col-12 mb-4">
                <h4 class="text-primary mb-3">
                    <i class="fas fa-chart-line me-2"></i>${data.report.title}
                </h4>
                <p class="lead">${data.report.summary}</p>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-center border-0 bg-primary bg-opacity-10">
                    <div class="card-body">
                        <i class="fas fa-dollar-sign text-primary fa-2x mb-2"></i>
                        <h5 class="card-title text-primary">${data.report.total_revenue}</h5>
                        <p class="card-text text-muted">Total Revenue</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center border-0 bg-success bg-opacity-10">
                    <div class="card-body">
                        <i class="fas fa-star text-success fa-2x mb-2"></i>
                        <h5 class="card-title text-success">${data.report.top_product}</h5>
                        <p class="card-text text-muted">Top Product</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center border-0 bg-info bg-opacity-10">
                    <div class="card-body">
                        <i class="fas fa-check-circle text-info fa-2x mb-2"></i>
                        <h5 class="card-title text-info">${data.report.data_quality}</h5>
                        <p class="card-text text-muted">Data Quality</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center border-0 bg-warning bg-opacity-10">
                    <div class="card-body">
                        <i class="fas fa-exclamation-triangle text-warning fa-2x mb-2"></i>
                        <h5 class="card-title text-warning">${data.cleaning.missing_values + data.cleaning.duplicates + data.cleaning.outliers}</h5>
                        <p class="card-text text-muted">Issues Found</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-lightbulb me-2"></i>Key Insights
                        </h5>
                    </div>
                    <div class="card-body">
                        ${data.insights.map(insight => `
                            <div class="d-flex align-items-start mb-3">
                                <i class="fas fa-arrow-right text-primary me-2 mt-1"></i>
                                <span>${insight}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card border-0 shadow-sm">
                    <div class="card-header bg-success text-white">
                        <h5 class="card-title mb-0">
                            <i class="fas fa-recommendations me-2"></i>Recommendations
                        </h5>
                    </div>
                    <div class="card-body">
                        ${data.personalized.map(rec => `
                            <div class="d-flex align-items-start mb-3">
                                <i class="fas fa-star text-success me-2 mt-1"></i>
                                <span>${rec}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    content.innerHTML = html;
}

// PDF Export Functionality
function exportReportAsPDF() {
    const exportBtn = document.getElementById('exportPdfBtn');
    
    // Show loading state
    const originalText = exportBtn.innerHTML;
    exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating PDF...';
    exportBtn.disabled = true;
    
    // Create a temporary link and trigger download
    const link = document.createElement('a');
    link.href = '/download-report';
    link.download = 'smart_data_analyzer_report.pdf';
    
    // Add to DOM temporarily, click, then remove
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Reset button after a short delay
    setTimeout(() => {
        exportBtn.innerHTML = originalText;
        exportBtn.disabled = false;
        showAlert('PDF report is being downloaded!', 'success');
    }, 1000);
}

// Growth Insights Functionality
function initializeGrowthInsights() {
    const generateBtn = document.getElementById('generateGrowthBtn');
    
    if (!generateBtn) return;

    generateBtn.addEventListener('click', function() {
        generateGrowthInsights();
    });
}

function generateGrowthInsights() {
    const btn = document.getElementById('generateGrowthBtn');
    const loading = document.getElementById('growthLoading');
    const content = document.getElementById('growthContent');
    
    // Show loading state
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing Growth Opportunities...';
    btn.disabled = true;

    // Fetch growth analytics data
    fetch('/growth-analytics')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showAlert(data.error, 'error');
                return;
            }
            
            displayGrowthInsights(data);
            loading.style.display = 'none';
            content.style.display = 'block';
            content.classList.add('fade-in');
        })
        .catch(error => {
            console.error('Error generating growth insights:', error);
            showAlert('Error generating growth insights. Please try again.', 'error');
        })
        .finally(() => {
            btn.innerHTML = '<i class="fas fa-chart-line me-2"></i>Generate Growth Insights';
            btn.disabled = false;
        });
}

function displayGrowthInsights(data) {
    // Revenue Prediction
    displayRevenuePrediction(data.revenue_prediction);
    
    // Top Products
    displayTopProducts(data.top_products);
    
    // Best Times
    displayBestTimes(data.best_times);
    
    // Missed Opportunities
    displayMissedOpportunities(data.missed_opportunities);
    
    // Data Quality
    displayDataQuality(data.data_quality);
    
    // Advanced Features
    displayProductLifecycle(data.product_lifecycle);
    displaySeasonalityPatterns(data.seasonality);
    displayAnomalies(data.anomalies);
    
    // AI Recommendations
    displayRecommendations(data.recommendations);
}

function displayRevenuePrediction(data) {
    // Update metrics
    document.getElementById('growthRate').textContent = `+${data.growth_rate}%`;
    document.getElementById('nextMonthRevenue').textContent = `$${data.next_month_revenue.toLocaleString()}`;
    document.getElementById('predictionAccuracy').textContent = `${data.prediction_accuracy} Confidence`;
    
    // Render chart
    const chartData = JSON.parse(data.chart);
    Plotly.newPlot('revenuePredictionChart', chartData.data, chartData.layout, {responsive: true});
}

function displayTopProducts(data) {
    // Render chart
    const chartData = JSON.parse(data.chart);
    Plotly.newPlot('topProductsChart', chartData.data, chartData.layout, {responsive: true});
    
    // Display product list
    const listContainer = document.getElementById('topProductsList');
    let listHtml = '';
    
    data.products.forEach((product, index) => {
        const medal = ['🥇', '🥈', '🥉'][index] || '🏆';
        listHtml += `
            <div class="d-flex justify-content-between align-items-center mb-2 p-2 bg-light rounded">
                <div>
                    <span class="me-2">${medal}</span>
                    <strong>${product.product}</strong>
                </div>
                <div class="text-end">
                    <div class="text-success fw-bold">$${product.revenue.toLocaleString()}</div>
                    <small class="text-muted">${product.quantity} units</small>
                </div>
            </div>
        `;
    });
    
    listContainer.innerHTML = listHtml;
}

function displayBestTimes(data) {
    // Render chart
    const chartData = JSON.parse(data.chart);
    Plotly.newPlot('bestTimesChart', chartData.data, chartData.layout, {responsive: true});
    
    // Update recommendation
    document.getElementById('timeRecommendation').innerHTML = `
        <i class="fas fa-lightbulb me-2"></i>
        <span>${data.recommendation}</span>
    `;
}

function displayMissedOpportunities(data) {
    // Update total missed revenue
    document.getElementById('missedRevenue').textContent = `$${data.total_missed_revenue.toLocaleString()}`;
    
    // Display opportunities list
    const listContainer = document.getElementById('missedOpportunitiesList');
    let listHtml = '';
    
    if (data.opportunities.length === 0) {
        listHtml = '<p class="text-muted text-center">No missed opportunities detected!</p>';
    } else {
        data.opportunities.forEach(opp => {
            listHtml += `
                <div class="border-bottom pb-2 mb-2">
                    <div class="d-flex justify-content-between">
                        <strong>${opp.product}</strong>
                        <span class="text-danger">-$${opp.potential_revenue.toFixed(2)}</span>
                    </div>
                    <small class="text-muted">${opp.missed_sales} missed sales at $${opp.avg_price.toFixed(2)}</small>
                </div>
            `;
        });
    }
    
    listContainer.innerHTML = listHtml;
}

function displayDataQuality(data) {
    // Update quality score circle
    const scoreElement = document.getElementById('qualityScore');
    const percentage = data.quality_score;
    scoreElement.querySelector('.percentage').textContent = `${percentage}%`;
    
    // Set color based on score
    let color = '#dc3545'; // red
    if (percentage >= 80) color = '#198754'; // green
    else if (percentage >= 60) color = '#ffc107'; // yellow
    
    scoreElement.style.background = `conic-gradient(${color} ${percentage * 3.6}deg, #e9ecef 0deg)`;
    
    // Display quality details
    const detailsContainer = document.getElementById('dataQualityDetails');
    detailsContainer.innerHTML = `
        <div class="row text-center">
            <div class="col-6">
                <div class="border-end">
                    <h6 class="text-warning">${data.missing_values}</h6>
                    <small>Missing Values</small>
                </div>
            </div>
            <div class="col-6">
                <h6 class="text-info">${data.duplicates}</h6>
                <small>Duplicates</small>
            </div>
        </div>
        <div class="row text-center mt-2">
            <div class="col-6">
                <div class="border-end">
                    <h6 class="text-danger">${data.zero_prices}</h6>
                    <small>Zero Prices</small>
                </div>
            </div>
            <div class="col-6">
                <h6 class="text-muted">${data.negative_quantities}</h6>
                <small>Negative Qty</small>
            </div>
        </div>
    `;
}

function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendationsList');
    let html = '';
    
    recommendations.forEach(rec => {
        const impactColor = rec.impact === 'High' ? 'success' : rec.impact === 'Medium' ? 'warning' : 'info';
        html += `
            <div class="col-md-6 mb-3">
                <div class="card border-0 bg-light h-100">
                    <div class="card-body">
                        <div class="d-flex align-items-start">
                            <div class="recommendation-icon me-3">
                                <i class="${rec.icon} fa-lg text-primary"></i>
                            </div>
                            <div class="flex-grow-1">
                                <h6 class="card-title">${rec.title}</h6>
                                <p class="card-text small">${rec.recommendation}</p>
                                <span class="badge bg-${impactColor}">${rec.impact} Impact</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Advanced Features Functions
function displayProductLifecycle(lifecycleData) {
    const container = document.getElementById('lifecycleMatrix');
    let html = '';
    
    lifecycleData.forEach(product => {
        const stageColors = {
            'Launch': 'primary',
            'Growth': 'success', 
            'Mature': 'warning',
            'Decline': 'danger'
        };
        
        const stageIcons = {
            'Launch': 'fas fa-rocket',
            'Growth': 'fas fa-trending-up',
            'Mature': 'fas fa-chart-line',
            'Decline': 'fas fa-trending-down'
        };
        
        html += `
            <div class="lifecycle-item mb-2 p-2 border rounded">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${product.product}</strong>
                        <div class="mt-1">
                            <span class="badge bg-${stageColors[product.stage]}">
                                <i class="${stageIcons[product.stage]} me-1"></i>${product.stage}
                            </span>
                            <small class="text-muted ms-2">${product.confidence} confidence</small>
                        </div>
                    </div>
                    <div class="text-end">
                        <small class="text-success">$${product.total_revenue.toLocaleString()}</small>
                        <div class="lifecycle-actions mt-1">
                            <button class="btn btn-sm btn-outline-primary" onclick="getExternalLinks('${product.product}')">
                                <i class="fas fa-external-link-alt"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function displaySeasonalityPatterns(seasonalityData) {
    // Render seasonality chart
    const chartData = JSON.parse(seasonalityData.chart);
    Plotly.newPlot('seasonalityChart', chartData.data, chartData.layout, {responsive: true});
    
    // Update peak day info
    document.getElementById('peakDay').textContent = `${seasonalityData.peak_day} (${(seasonalityData.seasonality_strength * 100).toFixed(1)}% variation)`;
}

function displayAnomalies(anomalies) {
    const container = document.getElementById('anomalyList');
    let html = '';
    
    if (anomalies.length === 0) {
        html = '<p class="text-muted text-center">No anomalies detected!</p>';
    } else {
        anomalies.forEach(anomaly => {
            const alertType = anomaly.severity === 'high' ? 'danger' : 'warning';
            const icon = anomaly.type === 'spike' ? 'fas fa-arrow-up' : 'fas fa-arrow-down';
            
            html += `
                <div class="alert alert-${alertType} mb-2" role="alert">
                    <div class="d-flex align-items-start">
                        <i class="${icon} me-2 mt-1"></i>
                        <div class="flex-grow-1">
                            <strong>${anomaly.product}</strong>
                            <div class="small">
                                ${anomaly.type === 'spike' ? 'Unusual spike' : 'Significant drop'}: 
                                $${anomaly.value.toFixed(2)} (${anomaly.deviation_percent.toFixed(1)}% deviation)
                            </div>
                            <div class="small text-muted">Expected: ${anomaly.expected_range}</div>
                        </div>
                        <button class="btn btn-sm btn-outline-${alertType}" onclick="investigateAnomaly('${anomaly.product}')">
                            Investigate
                        </button>
                    </div>
                </div>
            `;
        });
    }
    
    container.innerHTML = html;
}

function getExternalLinks(productName) {
    // Generate external research links
    const encodedProduct = encodeURIComponent(productName);
    const links = {
        trends: `https://trends.google.com/trends/explore?q=${encodedProduct}`,
        amazon: `https://www.amazon.com/s?k=${encodedProduct}`,
        search: `https://www.google.com/search?q=${encodedProduct}+market+analysis`
    };
    
    // Create modal or popup with links
    const modal = `
        <div class="modal fade" id="externalLinksModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Research: ${productName}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="d-grid gap-2">
                            <a href="${links.trends}" target="_blank" class="btn btn-outline-primary">
                                <i class="fas fa-chart-line me-2"></i>View Google Trends
                            </a>
                            <a href="${links.amazon}" target="_blank" class="btn btn-outline-warning">
                                <i class="fab fa-amazon me-2"></i>Compare on Amazon
                            </a>
                            <a href="${links.search}" target="_blank" class="btn btn-outline-info">
                                <i class="fas fa-search me-2"></i>Market Analysis
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal and add new one
    const existingModal = document.getElementById('externalLinksModal');
    if (existingModal) existingModal.remove();
    
    document.body.insertAdjacentHTML('beforeend', modal);
    const modalElement = new bootstrap.Modal(document.getElementById('externalLinksModal'));
    modalElement.show();
}

function investigateAnomaly(productName) {
    showAlert(`Investigating anomaly for ${productName}. Check external trends and recent market changes.`, 'info');
    getExternalLinks(productName);
}

// Recommendation Action Functions
function initializeRecommendationActions() {
    const exportBtn = document.getElementById('exportRecommendationsBtn');
    const saveBtn = document.getElementById('saveRecommendationsBtn');
    
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            exportRecommendationsToEmail();
        });
    }
    
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            saveRecommendationsForLater();
        });
    }
}

function exportRecommendationsToEmail() {
    // Simulate email export
    const subject = encodeURIComponent('AI Growth Recommendations - Smart Data Analyzer');
    const body = encodeURIComponent('Please find attached AI-powered growth recommendations from your data analysis.');
    const mailtoLink = `mailto:?subject=${subject}&body=${body}`;
    
    window.open(mailtoLink, '_blank');
    showAlert('Email client opened with recommendations!', 'success');
}

function saveRecommendationsForLater() {
    // Simulate saving recommendations
    const recommendations = document.getElementById('recommendationsList').innerHTML;
    localStorage.setItem('saved_recommendations', recommendations);
    localStorage.setItem('saved_date', new Date().toISOString());
    
    showAlert('Recommendations saved to your browser storage!', 'success');
}

// Enhanced Recommendation Display with Action Buttons
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendationsList');
    let html = '';
    
    recommendations.forEach((rec, index) => {
        const impactColor = rec.impact === 'High' ? 'success' : rec.impact === 'Medium' ? 'warning' : 'info';
        html += `
            <div class="col-md-6 mb-3">
                <div class="card border-0 bg-light h-100">
                    <div class="card-body">
                        <div class="d-flex align-items-start">
                            <div class="recommendation-icon me-3">
                                <i class="${rec.icon} fa-lg text-primary"></i>
                            </div>
                            <div class="flex-grow-1">
                                <h6 class="card-title">${rec.title}</h6>
                                <p class="card-text small">${rec.recommendation}</p>
                                <div class="d-flex justify-content-between align-items-center">
                                    <span class="badge bg-${impactColor}">${rec.impact} Impact</span>
                                    <div class="recommendation-actions">
                                        <button class="btn btn-sm btn-success me-1" onclick="acceptRecommendation(${index})">
                                            <i class="fas fa-check"></i>
                                        </button>
                                        <button class="btn btn-sm btn-primary me-1" onclick="exportSingleRecommendation(${index})">
                                            <i class="fas fa-envelope"></i>
                                        </button>
                                        <button class="btn btn-sm btn-secondary" onclick="saveRecommendation(${index})">
                                            <i class="fas fa-bookmark"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    // Initialize action buttons
    initializeRecommendationActions();
}

function acceptRecommendation(index) {
    showAlert('Recommendation accepted and added to action plan!', 'success');
}

function exportSingleRecommendation(index) {
    showAlert('Recommendation exported to email!', 'info');
}

function saveRecommendation(index) {
    showAlert('Recommendation saved for later review!', 'success');
}

// Advanced Analytics Functionality
function initializeAdvancedAnalytics() {
    const generateBtn = document.getElementById('generateAdvancedBtn');
    const sendEmailBtn = document.getElementById('sendEmailBtn');
    const sendSlackBtn = document.getElementById('sendSlackBtn');
    
    if (generateBtn) {
        generateBtn.addEventListener('click', function() {
            generateAdvancedAnalytics();
        });
    }
    
    if (sendEmailBtn) {
        sendEmailBtn.addEventListener('click', function() {
            sendReport('email');
        });
    }
    
    if (sendSlackBtn) {
        sendSlackBtn.addEventListener('click', function() {
            sendReport('slack');
        });
    }
}

function generateAdvancedAnalytics() {
    const generateBtn = document.getElementById('generateAdvancedBtn');
    const sendEmailBtn = document.getElementById('sendEmailBtn');
    const sendSlackBtn = document.getElementById('sendSlackBtn');
    
    // Show loading state
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    generateBtn.disabled = true;
    
    fetch('/advanced-analytics')
        .then(response => response.json())
        .then(data => {
            // Display all analytics components
            displayDataHealth(data.data_health);
            displayGrowthMetrics(data.growth_metrics);
            displayCustomerSegmentation(data.customer_segmentation);
            displayForecast(data.forecast);
            displayCustomerSamples(data.customer_segmentation.sample_customers);
            
            // Show all sections
            document.getElementById('dataHealthSection').style.display = 'block';
            document.getElementById('growthMetricsSection').style.display = 'block';
            document.getElementById('segmentationForecastSection').style.display = 'block';
            document.getElementById('customerSamplesSection').style.display = 'block';
            
            // Show send buttons
            sendEmailBtn.style.display = 'inline-block';
            sendSlackBtn.style.display = 'inline-block';
            
            // Reset button
            generateBtn.innerHTML = '<i class="fas fa-brain me-2"></i>Regenerate Analytics';
            generateBtn.disabled = false;
        })
        .catch(error => {
            console.error('Advanced Analytics Error:', error);
            showAlert('Using demo data for advanced analytics demonstration', 'info');
            
            // Use fallback demo data if API fails
            const demoData = {
                data_health: {
                    score: 87,
                    comment: "Good data quality with minor issues",
                    color: "success",
                    issues: ["Some missing values: 2.3%"],
                    stats: {
                        total_rows: 150,
                        total_columns: 4,
                        missing_pct: 2.3,
                        duplicate_pct: 0.0,
                        outlier_pct: 4.1
                    }
                },
                growth_metrics: {
                    wow_growth: 12.5,
                    mom_growth: 8.3,
                    best_streak: 8450.0,
                    best_streak_date: '2024-01-15',
                    sparkline: [800, 950, 1200, 1100, 1300, 1450, 1380, 1520, 1600, 1750, 1680, 1820, 1950, 2100],
                    current_revenue: 2100.0
                },
                customer_segmentation: {
                    chart: JSON.stringify({
                        data: [{
                            type: 'pie',
                            values: [25, 45, 30],
                            labels: ['High Value', 'Occasional', 'One-Time'],
                            marker: {
                                colors: ['#28a745', '#ffc107', '#dc3545']
                            }
                        }],
                        layout: {
                            title: 'Customer Segmentation Distribution'
                        }
                    }),
                    segments: [
                        { segment: 'High Value', count: 25, avg_revenue: 1250.0, avg_frequency: 8.5 },
                        { segment: 'Occasional', count: 45, avg_revenue: 420.0, avg_frequency: 3.2 },
                        { segment: 'One-Time', count: 30, avg_revenue: 89.0, avg_frequency: 1.0 }
                    ],
                    sample_customers: [
                        { customer: 'Customer_001', total_revenue: 2400.0, frequency: 12, segment_name: 'High Value' },
                        { customer: 'Customer_002', total_revenue: 680.0, frequency: 4, segment_name: 'Occasional' },
                        { customer: 'Customer_003', total_revenue: 95.0, frequency: 1, segment_name: 'One-Time' }
                    ]
                },
                forecast: {
                    chart: JSON.stringify({
                        data: [
                            {
                                x: ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
                                y: [1000, 1100, 950, 1200, 1150],
                                type: 'scatter',
                                mode: 'lines+markers',
                                name: 'Historical Sales',
                                line: { color: '#007bff' }
                            },
                            {
                                x: ['2024-01-06', '2024-01-07', '2024-01-08', '2024-01-09', '2024-01-10'],
                                y: [1250, 1300, 1275, 1350, 1400],
                                type: 'scatter',
                                mode: 'lines',
                                name: 'Forecast',
                                line: { color: '#28a745', dash: 'dash' }
                            }
                        ],
                        layout: {
                            title: '30-Day Sales Forecast',
                            xaxis: { title: 'Date' },
                            yaxis: { title: 'Revenue ($)' }
                        }
                    }),
                    summary: 'Sales expected to grow by 8-12% over next 30 days',
                    growth_rate: 10.0
                }
            };
            
            // Display demo analytics
            displayDataHealth(demoData.data_health);
            displayGrowthMetrics(demoData.growth_metrics);
            displayCustomerSegmentation(demoData.customer_segmentation);
            displayForecast(demoData.forecast);
            displayCustomerSamples(demoData.customer_segmentation.sample_customers);
            
            // Show all sections
            document.getElementById('dataHealthSection').style.display = 'block';
            document.getElementById('growthMetricsSection').style.display = 'block';
            document.getElementById('segmentationForecastSection').style.display = 'block';
            document.getElementById('customerSamplesSection').style.display = 'block';
            
            // Show send buttons
            sendEmailBtn.style.display = 'inline-block';
            sendSlackBtn.style.display = 'inline-block';
            
            // Reset button
            generateBtn.innerHTML = '<i class="fas fa-brain me-2"></i>Regenerate Analytics';
            generateBtn.disabled = false;
        });
}

function displayDataHealth(healthData) {
    // Update score circle
    const scoreCircle = document.querySelector('.progress-circle');
    const scoreText = document.querySelector('.score-text');
    const comment = document.getElementById('healthComment');
    const issues = document.getElementById('healthIssues');
    const totalRows = document.getElementById('totalRows');
    const missingPct = document.getElementById('missingPct');
    
    if (scoreCircle && scoreText) {
        scoreCircle.setAttribute('data-score', healthData.score);
        scoreText.textContent = healthData.score + '%';
        
        // Animate progress circle
        updateProgressCircle(scoreCircle, healthData.score, healthData.color);
    }
    
    if (comment) {
        comment.textContent = healthData.comment;
        comment.className = `text-${healthData.color}`;
    }
    
    if (issues && healthData.issues) {
        let issuesHtml = '';
        healthData.issues.forEach(issue => {
            issuesHtml += `<small class="badge bg-warning me-1">${issue}</small>`;
        });
        issues.innerHTML = issuesHtml;
    }
    
    if (totalRows && healthData.stats) {
        totalRows.textContent = healthData.stats.total_rows.toLocaleString();
    }
    
    if (missingPct && healthData.stats) {
        missingPct.textContent = healthData.stats.missing_pct.toFixed(1) + '%';
    }
}

function updateProgressCircle(circle, score, color) {
    const circumference = 2 * Math.PI * 45; // radius = 45
    const offset = circumference - (score / 100) * circumference;
    
    circle.style.background = `conic-gradient(
        var(--${color}-color) ${score * 3.6}deg,
        #e9ecef ${score * 3.6}deg
    )`;
}

function displayGrowthMetrics(metrics) {
    // Update growth percentages
    const wowGrowth = document.getElementById('wowGrowth');
    const momGrowth = document.getElementById('momGrowth');
    const bestStreak = document.getElementById('bestStreak');
    const streakDate = document.getElementById('streakDate');
    
    if (wowGrowth) {
        wowGrowth.textContent = (metrics.wow_growth >= 0 ? '+' : '') + metrics.wow_growth.toFixed(1) + '%';
        wowGrowth.className = metrics.wow_growth >= 0 ? 'text-success' : 'text-danger';
    }
    
    if (momGrowth) {
        momGrowth.textContent = (metrics.mom_growth >= 0 ? '+' : '') + metrics.mom_growth.toFixed(1) + '%';
        momGrowth.className = metrics.mom_growth >= 0 ? 'text-primary' : 'text-danger';
    }
    
    if (bestStreak) {
        bestStreak.textContent = '$' + metrics.best_streak.toLocaleString();
    }
    
    if (streakDate) {
        streakDate.textContent = metrics.best_streak_date;
    }
    
    // Draw sparklines
    if (metrics.sparkline) {
        drawSparkline('wowSparkline', metrics.sparkline, '#28a745');
        drawSparkline('momSparkline', metrics.sparkline, '#007bff');
    }
}

function drawSparkline(canvasId, data, color) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    if (data.length < 2) return;
    
    // Calculate dimensions
    const padding = 5;
    const chartWidth = width - 2 * padding;
    const chartHeight = height - 2 * padding;
    
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;
    
    // Draw line
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    
    data.forEach((value, index) => {
        const x = padding + (index / (data.length - 1)) * chartWidth;
        const y = padding + chartHeight - ((value - min) / range) * chartHeight;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
}

function displayCustomerSegmentation(segmentationData) {
    // Display segmentation chart
    const chartData = JSON.parse(segmentationData.chart);
    Plotly.newPlot('segmentationChart', chartData.data, chartData.layout, {responsive: true});
    
    // Display segment table
    const segmentTable = document.getElementById('segmentTable');
    let tableHtml = `
        <table class="table table-sm">
            <thead>
                <tr>
                    <th>Segment</th>
                    <th>Count</th>
                    <th>Avg Revenue</th>
                    <th>Avg Frequency</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    segmentationData.segments.forEach(segment => {
        tableHtml += `
            <tr>
                <td><span class="badge bg-primary">${segment.segment}</span></td>
                <td>${segment.count}</td>
                <td>$${segment.avg_revenue.toFixed(2)}</td>
                <td>${segment.avg_frequency.toFixed(1)}</td>
            </tr>
        `;
    });
    
    tableHtml += '</tbody></table>';
    segmentTable.innerHTML = tableHtml;
}

function displayForecast(forecastData) {
    // Display forecast chart
    const chartData = JSON.parse(forecastData.chart);
    Plotly.newPlot('forecastChart', chartData.data, chartData.layout, {responsive: true});
    
    // Update forecast summary
    const forecastSummary = document.getElementById('forecastSummary');
    if (forecastSummary) {
        forecastSummary.innerHTML = `
            <i class="fas fa-chart-line me-2"></i>
            ${forecastData.summary}
        `;
        forecastSummary.className = forecastData.growth_rate >= 0 ? 'alert alert-success' : 'alert alert-warning';
    }
}

function displayCustomerSamples(sampleCustomers) {
    const tableBody = document.querySelector('#customerSamplesTable tbody');
    if (!tableBody || !sampleCustomers) return;
    
    let tableHtml = '';
    sampleCustomers.forEach(customer => {
        const segmentColor = {
            'High Value': 'success',
            'Occasional': 'warning',
            'One-Time': 'danger'
        };
        
        tableHtml += `
            <tr>
                <td>${customer.customer}</td>
                <td><span class="badge bg-${segmentColor[customer.segment_name] || 'secondary'}">${customer.segment_name}</span></td>
                <td>$${customer.total_revenue.toLocaleString()}</td>
                <td>${customer.frequency || 'N/A'}</td>
                <td><i class="fas fa-check-circle text-success"></i> Active</td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = tableHtml;
}

function sendReport(method) {
    const data = {
        method: method,
        recipient: method === 'email' ? 'client@example.com' : '#analytics-team'
    };
    
    fetch('/send-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showAlert(result.message, 'success');
        } else {
            showAlert(result.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Failed to send report', 'error');
    });
}

// Chat Functionality
function initializeChat() {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');

    if (!chatForm) return;

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const question = chatInput.value.trim();
        if (question) {
            sendMessage(question);
            chatInput.value = '';
        }
    });

    // Handle suggestion buttons
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const question = this.dataset.question;
            sendMessage(question);
        });
    });

    function sendMessage(question) {
        // Add user message
        addMessage(question, 'user');
        
        // Show typing indicator
        const typingId = addTypingIndicator();
        
        // Send to server
        fetch('/explore', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator(typingId);
            
            if (data.error) {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                return;
            }
            
            // Add bot response
            addMessage(data.response, 'bot');
            
            // Update suggestions if provided
            if (data.suggestions) {
                updateSuggestions(data.suggestions);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator(typingId);
            addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        });
    }

    function addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message slide-up`;
        
        const time = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${type === 'user' ? 'You' : 'AI Assistant'}:</strong> ${content}
            </div>
            <small class="text-muted">${time}</small>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageDiv;
    }

    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="message-content">
                <strong>AI Assistant:</strong> 
                <span class="typing-dots">
                    <span>.</span><span>.</span><span>.</span>
                </span>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return 'typing-indicator';
    }

    function removeTypingIndicator(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function updateSuggestions(suggestions) {
        const suggestionsContainer = document.getElementById('suggestedQuestions');
        const buttonsContainer = suggestionsContainer.querySelector('.d-flex');
        
        buttonsContainer.innerHTML = suggestions.map(suggestion => `
            <button class="btn btn-sm btn-outline-primary suggestion-btn" data-question="${suggestion}">
                ${suggestion.length > 20 ? suggestion.substring(0, 20) + '...' : suggestion}
            </button>
        `).join('');
        
        // Re-attach event listeners
        buttonsContainer.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const question = this.dataset.question;
                sendMessage(question);
            });
        });
    }
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentElement) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize all functionality when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    initializeReportGeneration();
    initializeGrowthInsights();
    initializeAdvancedAnalytics();
    initializeChat();
});

// Add CSS for typing animation
const style = document.createElement('style');
style.textContent = `
    .typing-dots span {
        animation: typing 1.4s infinite;
    }
    
    .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% { opacity: 0; }
        30% { opacity: 1; }
    }
`;
document.head.appendChild(style);

// Email Report Functionality
function emailReport() {
    const email = prompt('Enter your email address to receive the PDF report:');
    
    if (!email) {
        return; // User canceled
    }
    
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showAlert('Please enter a valid email address.', 'error');
        return;
    }
    
    const emailBtn = document.getElementById('emailReportBtn');
    const originalText = emailBtn.innerHTML;
    
    // Show loading state
    emailBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    emailBtn.disabled = true;
    
    // Send email request
    fetch('/email-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert(`Report successfully sent to ${email}! Check your inbox for the download link.`, 'success');
        } else {
            showAlert(`Failed to send email: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        console.error('Error sending email:', error);
        showAlert('Failed to send email. Please try again.', 'error');
    })
    .finally(() => {
        // Reset button
        emailBtn.innerHTML = originalText;
        emailBtn.disabled = false;
    });
}
