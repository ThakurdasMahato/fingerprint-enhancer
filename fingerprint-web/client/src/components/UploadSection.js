import React, { useState, useRef } from 'react';
import { Upload } from 'lucide-react';
import './UploadSection.css';

function UploadSection({ onFileSelect }) {
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onFileSelect(files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="card upload-card">
      <div className="upload-section">
        <div
          className={`upload-box ${dragOver ? 'dragover' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className="upload-icon" />
          <h2>Upload Fingerprint Image</h2>
          <p>Drag and drop your image or click to select</p>
          <p className="file-info">Supported: JPEG, PNG, BMP</p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".jpg,.jpeg,.png,.bmp"
            onChange={handleFileChange}
            hidden
          />
        </div>
        <button
          className="btn btn-primary"
          onClick={() => fileInputRef.current?.click()}
        >
          Select Image
        </button>
      </div>
    </div>
  );
}

export default UploadSection;
