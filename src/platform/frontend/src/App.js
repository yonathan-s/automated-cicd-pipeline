import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Layout/Header';
import Dashboard from './components/Dashboard/Dashboard';
import StatisticalAnalysis from './components/Statistics/StatisticalAnalysis';
import Simulator from './components/Simulator/Simulator';
import { healthCheck } from './services/api';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [apiStatus, setApiStatus] = useState('checking');

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
    const interval = setInterval(checkAPI, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <Header currentView={currentView} onViewChange={setCurrentView} />
      
      <main className="main-content">
        <div className="container">
          <div className={`api-status ${apiStatus}`}>
            <span className="status-dot"></span>
            {apiStatus === 'checking' && 'Checking API connection...'}
            {apiStatus === 'connected' && 'Backend API Connected'}
            {apiStatus === 'disconnected' && 'Backend API Disconnected - Please start the backend server'}
          </div>


          <div className="view-content">
            {currentView === 'dashboard' && <Dashboard />}
            
            {currentView === 'statistics' && <StatisticalAnalysis />}

            {currentView === 'simulator' && <Simulator />}
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>
          Deployment Metrics Platform | 
          Backend: <code>http://localhost:5001</code>
        </p>
      </footer>
    </div>
  );
}

export default App;