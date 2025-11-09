// API Configuration
// Development: Uses localhost backend
// Production: Uses Render backend URL
// TODO: After deploying to Render, update the production URL below with your actual Render URL
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001'  // Local development
    : (window.BACKEND_URL || 'https://literature-assistant.onrender.com');  // Production - Replace YOUR-APP-NAME with your actual Render service name

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const clearFileBtn = document.getElementById('clearFileBtn');
const processBtn = document.getElementById('processBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const markdownOutput = document.getElementById('markdownOutput');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const downloadMarkdownBtn = document.getElementById('downloadMarkdown');
const downloadDocxBtn = document.getElementById('downloadDocx');

let selectedFile = null;
let analysisResult = null;

// Event Listeners
uploadBtn.addEventListener('click', (e) => {
    e.stopPropagation(); // Prevent event bubbling
    fileInput.click();
});
fileInput.addEventListener('change', handleFileSelection);
clearFileBtn.addEventListener('click', clearFileSelection);
processBtn.addEventListener('click', processDocument);
downloadMarkdownBtn.addEventListener('click', () => downloadFile('markdown'));
downloadDocxBtn.addEventListener('click', () => downloadFile('docx'));

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'application/pdf') {
        selectedFile = files[0];
        updateFileInfo();
    } else {
        showError('Please select a valid PDF file.');
    }
});

uploadArea.addEventListener('click', (e) => {
    // Only trigger if clicking the area itself, not the button
    if (e.target !== uploadBtn && !uploadBtn.contains(e.target)) {
        fileInput.click();
    }
});

function handleFileSelection(event) {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
        selectedFile = file;
        updateFileInfo();
        hideError();
    } else {
        showError('Please select a valid PDF file.');
    }
}

function updateFileInfo() {
    if (selectedFile) {
        fileName.textContent = selectedFile.name;
        fileInfo.style.display = 'block';
        processBtn.disabled = false;
    }
}

function clearFileSelection() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    processBtn.disabled = true;
    hideResults();
    hideError();
}

async function processDocument() {
    if (!selectedFile) {
        showError('Please select a PDF file first.');
        return;
    }


    // Show loading state
    processBtn.disabled = true;
    loading.style.display = 'block';
    hideResults();
    hideError();

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Send to backend
        const response = await fetch(`${API_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
            throw new Error(errorData.error || 'Failed to process document');
        }

        const result = await response.json();
        analysisResult = result;

        // Display results
        displayResults(result.markdown);

    } catch (error) {
        console.error('Processing error:', error);

        // Provide more specific error messages
        let errorMsg = error.message;

        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            errorMsg = `Cannot connect to backend server at ${API_URL}. Please ensure the backend is running.\n\nStart the backend with: docker-compose up`;
        } else if (error.message.includes('NetworkError') || error.message.includes('Failed to fetch')) {
            errorMsg = `Network error: Cannot reach backend server at ${API_URL}.\n\nMake sure:\n1. Backend is running (docker-compose up)\n2. No firewall blocking the connection`;
        }

        showError(errorMsg);
    } finally {
        loading.style.display = 'none';
        processBtn.disabled = false;
    }
}

function displayResults(markdown) {
    // Convert markdown to HTML using marked.js
    markdownOutput.innerHTML = marked.parse(markdown);
    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function hideResults() {
    resultsSection.style.display = 'none';
    analysisResult = null;
}

async function downloadFile(format) {
    if (!analysisResult) {
        showError('No analysis results to download.');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/download/${format}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: analysisResult.markdown,
                filename: getOutputFilename(format)
            })
        });

        if (!response.ok) {
            throw new Error('Failed to download file');
        }

        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = getOutputFilename(format);
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        console.error('Download error:', error);
        showError('Failed to download file. Please try again.');
    }
}

function getOutputFilename(format) {
    const timestamp = new Date().toISOString().split('T')[0];
    const baseName = selectedFile ? selectedFile.name.replace('.pdf', '') : 'analysis';
    return `${baseName}_analysis_${timestamp}.${format === 'markdown' ? 'md' : 'docx'}`;
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorSection.style.display = 'none';
}

// Initialize marked.js options
if (typeof marked !== 'undefined') {
    marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: true,
        mangle: false
    });
}
