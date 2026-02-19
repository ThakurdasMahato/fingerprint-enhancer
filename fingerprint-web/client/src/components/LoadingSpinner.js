import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading">
      <div className="spinner"></div>
      <p>Enhancing your fingerprint image...</p>
    </div>
  );
}

export default LoadingSpinner;
