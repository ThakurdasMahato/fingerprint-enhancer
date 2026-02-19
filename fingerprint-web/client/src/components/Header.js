import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <svg width="50" height="50" viewBox="0 0 40 40" fill="none">
            <circle cx="20" cy="20" r="18" stroke="#6366f1" strokeWidth="2" />
            <path
              d="M15 20C15 17.2 17.2 15 20 15C22.8 15 25 17.2 25 20"
              stroke="#6366f1"
              strokeWidth="2"
              fill="none"
            />
            <circle cx="20" cy="20" r="3" fill="#6366f1" />
          </svg>
          <h1>Fingerprint Enhancer</h1>
        </div>
        <p className="subtitle">Advanced fingerprint image enhancement using Gabor filters</p>
      </div>
    </header>
  );
}

export default Header;
