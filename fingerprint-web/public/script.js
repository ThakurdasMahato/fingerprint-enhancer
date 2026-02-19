// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const previewSection = document.getElementById('previewSection');
const originalImage = document.getElementById('originalImage');
const enhancedImage = document.getElementById('enhancedImage');
const loading = document.getElementById('loading');
const message = document.getElementById('message');
const resetBtn = document.getElementById('resetBtn');
const downloadBtn = document.getElementById('downloadBtn');

let currentFile = null;
let enhancedFileName = null;

// Event Listeners
selectBtn.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('click', () => fileInput.click());

uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

resetBtn.addEventListener('click', reset);

downloadBtn.addEventListener('click', downloadEnhancedImage);

// Functions
function handleFileSelect(file) {
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/bmp', 'image/jpg'];
    
    if (!allowedTypes.includes(file.type)) {
        showMessage('Please select a valid image file (JPEG, PNG, or BMP)', 'error');
        return;
    }

    currentFile = file;

    // Display original image
    const reader = new FileReader();
    reader.onload = (e) => {
        originalImage.src = e.target.result;
        previewSection.style.display = 'flex';
        enhancedImage.src = '';
        uploadBox.style.display = 'none';
        selectBtn.style.display = 'none';
        enhanceImage();
    };
    reader.readAsDataURL(file);
}

async function enhanceImage() {
    loading.style.display = 'flex';
    message.style.display = 'none';

    const formData = new FormData();
    formData.append('image', currentFile);

    try {
        const response = await fetch('/api/enhance', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        loading.style.display = 'none';

        if (!response.ok) {
            showMessage(`Enhancement failed: ${data.error || 'Unknown error'}`, 'error');
            reset();
            return;
        }

        enhancedImage.src = data.enhanced;
        enhancedFileName = data.fileName;
        showMessage('Fingerprint enhanced successfully!', 'success');

    } catch (error) {
        loading.style.display = 'none';
        showMessage(`Error: ${error.message}`, 'error');
        reset();
    }
}

function downloadEnhancedImage() {
    if (!enhancedFileName) {
        showMessage('No enhanced image available', 'error');
        return;
    }

    const link = document.createElement('a');
    link.href = `/api/download/${enhancedFileName}`;
    link.download = enhancedFileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showMessage('Image downloaded successfully!', 'success');
}

function reset() {
    currentFile = null;
    enhancedFileName = null;
    fileInput.value = '';
    previewSection.style.display = 'none';
    loading.style.display = 'none';
    message.style.display = 'none';
    originalImage.src = '';
    enhancedImage.src = '';
    uploadBox.style.display = 'block';
    selectBtn.style.display = 'block';
}

function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type}`;
    message.style.display = 'block';

    // Auto-hide success messages after 4 seconds
    if (type === 'success') {
        setTimeout(() => {
            message.style.display = 'none';
        }, 4000);
    }
}

// Initialize
console.log('Fingerprint Enhancer Web App loaded successfully!');
