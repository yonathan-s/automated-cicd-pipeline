/**
 * Header Component
 * Top navigation bar for the platform
 */

import React from 'react';
import './Header.css';

const Header = ({ currentView, onViewChange }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-title">
          <h1>📊 Deployment Metrics Platform</h1>
          <p className="header-subtitle">
            Quantitative Evaluation of CI/CD Automation
          </p>
        </div>
        
        <nav className="header-nav">
          <button
            className={`nav-button ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => onViewChange('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={`nav-button ${currentView === 'statistics' ? 'active' : ''}`}
            onClick={() => onViewChange('statistics')}
          >
            Statistical Analysis
          </button>
          <button
            className={`nav-button ${currentView === 'simulator' ? 'active' : ''}`}
            onClick={() => onViewChange('simulator')}
          >
            Simulator
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;