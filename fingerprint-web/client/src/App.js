import React, { useState } from 'react';
import Header from './components/Header';
import UploadSection from './components/UploadSection';
import PreviewSection from './components/PreviewSection';
import LoadingSpinner from './components/LoadingSpinner';
import Message from './components/Message';
import Footer from './components/Footer';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'https://fingerprint-enhancer-we.onrender.com';

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [enhancedImage, setEnhancedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [message, setMessage] = useState(null);
  const [currentFile, setCurrentFile] = useState(null);
  const [enhancedFileName, setEnhancedFileName] = useState(null);

  const showMessage = (text, type) => {
    setMessage({ text, type });
    if (type === 'success') {
      setTimeout(() => setMessage(null), 4000);
    }
  };

  const handleFileSelect = async (file) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/bmp', 'image/jpg'];

    if (!allowedTypes.includes(file.type)) {
      showMessage('Please select a valid image file (JPEG, PNG, or BMP)', 'error');
      return;
    }

    setCurrentFile(file);

    const reader = new FileReader();
    reader.onload = (e) => {
      setOriginalImage(e.target.result);
      setEnhancedImage(null);
    };
    reader.readAsDataURL(file);
  };

  const enhanceImage = async (file) => {
    setLoading(true);
    setIsEnhancing(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/api/enhance`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = response.data;
      setEnhancedImage(data.enhanced_image);
      setEnhancedFileName(data.file_name);
      showMessage('Fingerprint enhanced successfully!', 'success');
    } catch (error) {
      showMessage(
        `Enhancement failed: ${error.response?.data?.error || error.message}`,
        'error'
      );
      reset();
    } finally {
      setLoading(false);
      setIsEnhancing(false);
    }
  };

  const downloadEnhancedImage = () => {
    if (!enhancedFileName) {
      showMessage('No enhanced image available', 'error');
      return;
    }

    const link = document.createElement('a');
    link.href = `${API_URL}/api/download/${enhancedFileName}`;
    link.download = enhancedFileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showMessage('Image downloaded successfully!', 'success');
  };

  const reset = () => {
    setCurrentFile(null);
    setEnhancedFileName(null);
    setOriginalImage(null);
    setEnhancedImage(null);
    setMessage(null);
  };

  return (
    <div className="app-container">
      <Header />

      <main className="main-content">
        {message && <Message message={message} />}

        {loading && <LoadingSpinner />}

        {!originalImage && !loading && (
          <UploadSection onFileSelect={handleFileSelect} />
        )}

        {originalImage && !loading && (
          <PreviewSection
            originalImage={originalImage}
            enhancedImage={enhancedImage}
            isEnhancing={isEnhancing}
            onReset={reset}
            onDownload={downloadEnhancedImage}
            onEnhance={() => enhanceImage(currentFile)}
          />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
