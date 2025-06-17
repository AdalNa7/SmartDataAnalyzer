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
            
            // Show the export PDF button after report is generated
            const exportBtn = document.getElementById('exportPdfBtn');
            if (exportBtn) {
                exportBtn.style.display = 'inline-block';
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
