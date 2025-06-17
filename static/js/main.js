// Smart Data Analyzer - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFileUpload();
    initializeReportGeneration();
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
