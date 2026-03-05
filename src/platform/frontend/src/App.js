/**
 * Main App Component
 * Root component that manages view switching and layout
 */

import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Layout/Header';
import { healthCheck } from './services/api';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [apiStatus, setApiStatus] = useState('checking');

  // Check API health on mount
  useEffect(() => {
    const checkAPI = async () => {
      try {
        await healthCheck();
        setApiStatus('connected');
      } catch (error) {
        setApiStatus('disconnected');
      }
    };

    checkAPI();
    // Check every 30 seconds
    const interval = setInterval(checkAPI, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <Header currentView={currentView} onViewChange={setCurrentView} />
      
      <main className="main-content">
        <div className="container">
          {/* API Status Indicator */}
          <div className={`api-status ${apiStatus}`}>
            <span className="status-dot"></span>
            {apiStatus === 'checking' && 'Checking API connection...'}
            {apiStatus === 'connected' && 'Backend API Connected'}
            {apiStatus === 'disconnected' && 'Backend API Disconnected - Please start the backend server'}
          </div>

          {/* View Content */}
          <div className="view-content">
            {currentView === 'dashboard' && (
              <div className="view-placeholder">
                <h2>📊 Dashboard View</h2>
                <p>Dashboard components coming in Day 5</p>
                <p className="placeholder-note">
                  This will show: deployment history, recent deployments, quick stats
                </p>
              </div>
            )}

            {currentView === 'statistics' && (
              <div className="view-placeholder">
                <h2>📈 Statistical Analysis View</h2>
                <p>Statistical analysis components coming in Day 6</p>
                <p className="placeholder-note">
                  This will show: t-tests, chi-square, effect sizes, comparison charts
                </p>
              </div>
            )}

            {currentView === 'simulator' && (
              <div className="view-placeholder">
                <h2>🔄 Simulator View</h2>
                <p>Simulator components coming in Day 7</p>
                <p className="placeholder-note">
                  This will allow: running manual simulations, viewing simulation results
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>
          Deployment Metrics Platform - Week 7 | 
          Backend: <code>http://localhost:5001</code>
        </p>
      </footer>
    </div>
  );
}

export default App;