import React from 'react';
import './PreviewSection.css';

function PreviewSection({ originalImage, enhancedImage, isEnhancing, onReset, onDownload, onEnhance }) {
  return (
    <div className="preview-section">
      <div className="image-comparison">
        <div className="image-wrapper original">
          <img src={originalImage} alt="Original" />
          <label>Original Image</label>
        </div>
        <div className="divider"></div>
        <div className="image-wrapper enhanced">
          {enhancedImage ? (
            <>
              <img src={enhancedImage} alt="Enhanced" />
              <label>Enhanced Image</label>
            </>
          ) : isEnhancing ? (
            <div className="placeholder">
              <div className="spinner-small"></div>
              <p>Processing...</p>
            </div>
          ) : (
            <div className="placeholder">
              <p>Click "Enhance Image" to start</p>
            </div>
          )}
        </div>
      </div>

      <div className="action-buttons">
        {!enhancedImage && (
          <button className="btn btn-primary" onClick={onEnhance}>
            Enhance Image
          </button>
        )}
        <button className="btn btn-secondary" onClick={onReset}>
          Reset
        </button>
        <button
          className="btn btn-success"
          onClick={onDownload}
          disabled={!enhancedImage}
        >
          Download Enhanced Image
        </button>
      </div>
    </div>
  );
}

export default PreviewSection;
